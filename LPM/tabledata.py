import pandas as pd
import sympy

from fractions import Fraction
import re, sys, os


def simplexTable():
    eq, basis = [], []
    #VARIANT = input('Вариант задания: ')
    print('Вводите уравнения. В конце введите end')
    equal = input()
    index = 1
    while equal != 'end':
        eq.append(equal)
        equal = input()
        index += 1

    for expr in eq:
        buffer = re.findall(r'x\d', expr)
        for elem in buffer:
            if elem not in basis:
                basis.append(elem)

    basisVar, counter, tableCoef = len(basis), len(eq), ['z']

    for i in range(len(eq)):
        if ('>' in eq[i] or ' = ' in eq[i]) and i != 0:
            print('Ошибка в уравнении')
            sys.exit(0)
        elif i == 0:
            eq[i] = eq[i].replace('*', ' ')
            eq[i] = eq[i].split(' ')
        elif ' <' in eq[i]:
            eq[i] = eq[i].replace('*', ' ')
            eq[i] = eq[i].replace('<=', '=')
            basisVar += 1
            eq[i] += f' + x{basisVar}'
            tableCoef.append(f'x{basisVar}')
            eq[i] = eq[i].split(' ')

    variable = ['z']
    for i in range(basisVar):
        variable.append(str(f'x{i + 1}'))
    variable.append('eq')

    tableData = pd.DataFrame(columns=variable, index=range(counter), dtype=object)
    tableData = tableData.fillna(0)

    index = 0
    for i in eq:
        for j in range(len(i)):
            if index == 0:
                tableData.loc[index]['z'] = 1
                if re.search(r'x\d', i[j]) is not None:
                    if i[j - 1] == '=' or i[j - 1] == '-' or i[j - 1] == '+':
                        if i[j - 1] == '=':
                            if re.search(r'-', i[j]) is not None:
                                tableData.loc[index][i[j]] = 1
                            else:
                                tableData.loc[index][i[j]] = -1
                        elif i[j - 1] == '-':
                            tableData.loc[index][i[j]] = 1
                        else:
                            tableData.loc[index][i[j]] = -1
                    if i[j - 2] == '=' or i[j - 2] == '-' or i[j - 2] == '+':
                        if i[j - 2] == '-':
                            tableData.loc[index][i[j]] = int(i[j - 1])
                        else:
                            tableData.loc[index][i[j]] = int(i[j - 1]) * (-1)
                elif re.search(r'\d+', i[j]) is not None:
                    if j == len(i) - 1 and re.search(r'x\d', i[j]) is None:
                        if i[j - 1] == '-':
                            tableData.loc[index]['eq'] = int(i[j]) * (-1)
                        else:
                            tableData.loc[index]['eq'] = int(i[j])
                    elif re.search(r'x\d', i[j + 1]) is None and re.search(r'x\d', i[j - 1]) is None:
                        if i[j - 1] == '-':
                            tableData.loc[index]['eq'] = int(i[j]) * (-1)
                        else:
                            tableData.loc[index]['eq'] = int(i[j])
            else:
                position = re.search(r'x\d', i[j])
                if position is not None:
                    pos = position[0]
                    if j == 0:
                        if re.search(r'-', i[j]) is not None:
                            tableData.loc[index][pos] = -1
                        else:
                            tableData.loc[index][pos] = 1
                    if j == 1:
                        tableData.loc[index][pos] = int(i[j - 1])
                    if j >= 1 and (i[j - 1] == '-' or i[j - 1] == '+'):
                        if i[j - 1] == '-':
                            tableData.loc[index][pos] = -1
                        else:
                            tableData.loc[index][pos] = 1
                    if j >= 2 and (i[j - 2] == '-' or i[j - 2] == '+'):
                        if i[j - 2] == '-':
                            tableData.loc[index][pos] = int(i[j - 1]) * (-1)
                        else:
                            tableData.iloc[index][pos] = int(i[j - 1])
                if re.search(r'=', i[j]) is not None:
                    length = len(i)
                    if j + 1 <= length and i[j + 1] != '+' and i[j + 1] != '-':
                        tableData.loc[index]['eq'] = int(i[j + 1])
                    if j + 2 <= length and i[j + 1] != '+' and i[j + 1] != '-':
                        if i[j + 1] == '-':
                            tableData.loc[index]['eq'] = int(i[j + 2]) * (-1)
                        if[j + 1] == '+':
                            tableData.loc[index]['eq'] = int(i[j + 2])
        index += 1

    tableData = tableData.set_index([pd.Index(tableCoef)])

    # printExprForLatex(VARIANT)

    return tableData


def simplexTableDiphasic():
    eq = []
    #VARIANT = input('Вариант задания: ')
    print('Вводите уравнения. В конце введите end')
    targetEqual = input()
    equal = targetEqual
    index = 1
    while equal != 'end':
        eq.append(equal)
        equal = input()
        index += 1
    basis = []
    for expr in eq:
        buffer = re.findall(r'x\d', expr)
        for elem in buffer:
            if elem not in basis:
                basis.append(elem)

    basisVar = len(basis)

    grad = ''
    if 'max' in eq[0]:
        grad = 'max'
    elif 'min' in eq[0]:
        grad = 'min'

    freeVar = 0
    counter = len(eq)
    tableCoef, variable = ['z'], ['z']
    for i in range(len(eq)):
        if ' = ' in eq[i]:
            eq[i] = eq[i].replace('*', ' ')
            if i != 0:
                freeVar += 1
                eq[i] += f' + R{freeVar}'
                tableCoef.append(f'R{freeVar}')
            eq[i] = eq[i].split(' ')
        elif ' >' in eq[i]:
            eq[i] = eq[i].replace('*', ' ')
            eq[i] = eq[i].replace('>=', '=')
            basisVar += 1
            eq[i] += f' - x{basisVar}'
            freeVar += 1
            eq[i] += f' + R{freeVar}'
            tableCoef.append(f'R{freeVar}')
            eq[i] = eq[i].split(' ')
        elif ' <' in eq[i]:
            eq[i] = eq[i].replace('*', ' ')
            eq[i] = eq[i].replace('<=', '=')
            basisVar += 1
            eq[i] += f' + x{basisVar}'
            tableCoef.append(f'x{basisVar}')
            eq[i] = eq[i].split(' ')

    for i in range(basisVar):
        variable.append(str(f'x{i + 1}'))
    for i in range(freeVar):
        variable.append(str(f'R{i + 1}'))
    variable.append('eq')

    tableData = pd.DataFrame(columns=variable, index=range(counter), dtype=object)
    tableData = tableData.fillna(0)

    sign = 0
    for i in range(1, len(eq)):
        for j in range(len(eq[i])):
            if re.match(r'x', eq[i][j]) is not None or re.match(r'R', eq[i][j]):
                var = eq[i][j]
                if j == 0 or eq[i][j - 1] == '+' or eq[i][j - 1] == '-':
                    if j == 0:
                        if re.match(r'-', eq[i][j]) is None:
                            tableData.loc[i][var] = 1
                        else:
                            tableData.loc[i][var] = -1
                    else:
                        if eq[i][j - 1] == '-':
                            tableData.loc[i][var] = -1
                        else:
                            tableData.loc[i][var] = 1
                elif eq[i][j - 2] == '-' or eq[i][j - 2] == '+':
                    if eq[i][j - 2] == '-':
                        sign = -1
                    else:
                        sign = 1
                    tableData.loc[i][var] = int(eq[i][j - 1]) * sign
                else:
                    tableData.loc[i][var] = int(eq[i][j - 1])
            elif eq[i][j] == '=':
                tableData.loc[i]['eq'] = int(eq[i][j + 1])


    x1, x2, x3, x4, x5, x6, x7, R1, R2, R3 = sympy.symbols('x1 x2 x3 x4 x5 x6 x7 R1 R2 R3')
    expr = []

    for i in range(freeVar):
        r = f'R{i + 1}'
        expression = ''
        index = 0
        for j in range(1, tableData.shape[0]):
            if tableData.iloc[j][r] != 0:
                index = j
        if index != 0:
            for k in list(tableData):
                if k != 'eq' and k != r and tableData.iloc[index][k] != 0:
                    if float(tableData.iloc[index][k]) > 0:
                        expression += ' - ' + str(tableData.iloc[index][k]) + ' * ' + str(k)
                    else:
                        expression += ' + ' + str(tableData.iloc[index][k] * (-1)) + ' * ' + str(k)
                elif tableData.iloc[index][k] != 0 and k != r:
                    if float(tableData.iloc[index][k] > 0):
                        expression += ' + ' + str(tableData.iloc[index][k])
                    else:
                        expression += ' - ' + str(tableData.iloc[index][k] * (-1))
            expression = str(expression)
            expr.append(expression)

    zExpr = ''
    for i in expr:
        zExpr += i

    zExpr = sympy.simplify(zExpr)

    zExpr1 = str(zExpr)
    zExpr1 = zExpr1.replace('*', '=')
    zExpr1 = zExpr1.split(' ')
    masZ = []

    for i in zExpr1:
        k = i.split('=')
        for j in k:
            masZ.append(j)

    tableData.loc[0]['z'] = 1

    for i in range(len(masZ)):
        if re.search(r'x', masZ[i]) is not None:
            if i == 0:
                if re.match(r'-', masZ[i]) is None:
                    tableData.loc[0][masZ[i]] = 1
                    masZ[i] = 0
                else:
                    pos = re.search(r'x\d', masZ[i]).group(0)
                    tableData.loc[0][pos] = -1
                    masZ[i] = 0
            elif masZ[i - 1] == '+':
                tableData.loc[0][masZ[i]] = 1
                masZ[i - 1] = 0
                masZ[i] = 0
            elif masZ[i - 1] == '-':
                tableData.loc[0][masZ[i]] = -1
                masZ[i] = 0
                masZ[i - 1] = 0
            elif masZ[i - 2] == '-':
                tableData.loc[0][masZ[i]] = int(masZ[i - 1]) * (-1)
                masZ[i] = 0
                masZ[i - 1] = 0
                masZ[i - 2] = 0
            elif masZ[i - 2] == '+':
                tableData.loc[0][masZ[i]] = int(masZ[i - 1])
                masZ[i] = 0
                masZ[i - 1] = 0
                masZ[i - 2] = 0
            else:
                tableData.loc[0][masZ[i]] = int(masZ[i - 1])
                masZ[i] = 0
                masZ[i - 1] = 0

    for i in range(len(masZ)):
        if masZ[i] != 0:
            if masZ[i] == '-':
                tableData.loc[0]['eq'] = int(masZ[i + 1])
                break
            if masZ[i] == '+':
                tableData.loc[0]['eq'] = int(masZ[i + 1]) * (-1)
                break

    tableData = tableData.set_index([pd.Index(tableCoef)])
    print(tableData)

    print(f'\nПЕРВЫЙ ЭТАП')
    #printExprForLatex(VARIANT)

    return tableData, targetEqual, grad


def findMinCheckElement(length, mas):
    minElement = 10000
    index = 0
    for i in range(1, length):
        if Fraction(mas[i]) < minElement and Fraction(mas[i]) >= 0:
            minElement = Fraction(mas[i])
            index = i
    return(index)


def beforeTargetString(table, iteration):
    length = table.shape[1]
    masM = table.iloc[0][1:length - 1]
    minimal = 10000
    for j in range(len(masM)):
        if Fraction(masM[j]) < minimal:
            minimal = Fraction(masM[j])

    if minimal >= 0:
        return table, 0
    else:
        print("\nШАГ", iteration)

    length = len(table)

    targetColumn = 0
    minimal = f'{minimal}'

    for i in list(table):
        if f'{table.iloc[0][i]}' == minimal:
            targetColumn = i
            break
    masCheck = []
    for i in range(length):
        eq = Fraction(table.iloc[i]['eq'])
        target = Fraction(table.iloc[i][targetColumn])
        if eq < 0 or target < 0:
            check = -1
        elif target != 0:
            check = Fraction(eq / target)
        else:
            check = -1
        masCheck.append(str(check))

    targetString = findMinCheckElement(length, masCheck)
    index = table.index
    masIndex = []
    for i in index:
        masIndex.append(i)
    masIndex[targetString] = targetColumn
    table = table.set_index([pd.Index(masIndex)])

    print(f'Минимальное значение: {minimal}, целевая столбец: {targetColumn}, целевая строка: {targetString}')
    #printTableForLatex(table, iteration, targetColumn, targetString)

    table = createNewTable(table, targetString, targetColumn)
    print(table)

    return table, 1


def createNewTable(exTable, string, column):
    newTable = exTable.copy()
    newTable = newTable.astype(object)

    exTargetElement = Fraction(exTable.iloc[string][column])
    targetElement = Fraction(1)

    length = exTable.shape[0]
    values = list(exTable)

    for i in range(length):
        newTable.iloc[i][column] = str(0)

    newTable.iloc[string][column] = str(targetElement)

    for i in values:
        if i != column and i != 'z':
            last = Fraction(exTable.iloc[string][i])
            newTable.iloc[string][i] = str(Fraction(last, exTargetElement))

    for i in range(length):
        for j in values:
            if i != string and i != 'z':
                last = Fraction(exTable.iloc[i][j])
                lastColumn = Fraction(exTable.iloc[i][column])
                newString = Fraction(newTable.iloc[string][j])
                x = last - lastColumn * newString
                newTable.iloc[i][j] = str(x)

    return(newTable)


def transferDiphasic(table, target):
    #file.write('\n\nЭТАП ВТОРОЙ\n\n\n')
    x1, x2, x3, x4, x5, x6, x7, R1, R2, R3 = sympy.symbols('x1 x2 x3 x4 x5 x6 x7 R1 R2 R3')
    newTable = table.copy()
    tableCoef = list(newTable)

    column, index = [], []
    for i in tableCoef:
        if re.match(r'R', i) is not None:
            column.append(i)

    newTable = newTable.drop(columns=column)
    newTable = newTable.astype(object)

    freeCoef = list(newTable)
    freeCoef.remove('z')
    freeCoef.remove('eq')

    for i in table.index:
        index.append(i)
        if i in freeCoef:
            freeCoef.remove(i)

    targetCoef = re.findall(r'x\d', target)
    sumCoef = targetCoef + freeCoef

    basisCoef = []
    for i in targetCoef:
        if i in freeCoef:
            basisCoef.append(i)
            freeCoef.remove(i)

    eqZ, grad = '', ''

    if 'min' in target:
        grad = 'min'
    if 'max' in target:
        grad = 'max'

    for i in target.split(' '):
        if i != 'z' and i != '=' and i != '->' and i != 'min' and i != 'max':
            eqZ += i
    eqZ = sympy.simplify(eqZ)

    if len(basisCoef) != len(targetCoef):
        equation = {}
        for i in targetCoef:
            equation[i] = ''

        for i in range(1, newTable.shape[0]):
            str = ''
            if index[i] in targetCoef:
                for j in list(newTable):
                    if j in sumCoef or j == 'eq':
                        val = newTable.iloc[i][j]
                        val = Fraction(val)
                        if val != 0 and j != 'z' and j != 'eq':
                            if val < 0:
                                str += f'{val}*{j}'
                            else:
                                str += f'+{val}*{j}'
                        if j == 'eq':
                            if val < 0:
                                str += f'+{val}'
                            else:
                                str += f'-{val}'
                equation[index[i]] = str

        for i in targetCoef:
            if i not in basisCoef:
                expr = sympy.solve(equation.get(i), i)
                eqZ = eqZ.subs(i, expr[0])

    if grad == 'max':
        eqZ *= -1

    print(f'z = {eqZ}')

    masZ = f'{eqZ}'.split(' ')
    sign = 0
    for i in range(len(masZ)):
        m = masZ[i]
        if m == '-':
            sign = -1
        elif m == '+':
            sign = 1
        elif m != '-' and m != '+':
            buffer = m.replace('/', ' ').split(' ')
            nom = buffer[0]
            if len(buffer) > 1:
                denom = buffer[1]
            else:
                denom = 1
            frac = 0
            pos = ''
            if 'x' in nom:
                bufNom = nom.replace('*', ' ').split(' ')
                if len(bufNom) > 1:
                    for j in range(len(bufNom)):
                        if 'x' in bufNom[j]:
                            pos = bufNom[j]
                        else:
                            if sign == 0:
                                frac = Fraction(int(bufNom[j]), int(denom))
                            else:
                                frac = Fraction(int(bufNom[j]) * sign, int(denom))
                                sign = 0
                else:
                    if '-' in bufNom[0]:
                        frac = Fraction(-1, int(denom))
                        pos = re.search(r'x\d', bufNom[0]).group(0)
                    elif sign != 0:
                        frac = Fraction(1 * sign, int(denom))
                        pos = bufNom[0]
                        sign = 0
                    else:
                        frac = Fraction(1, int(denom))
                        pos = bufNom[0]
            else:
                pos = 'eq'
                if sign != 0:
                    frac = Fraction(int(nom) * sign * (-1), int(denom))
                    sign = 0
                else:
                    frac = Fraction(int(nom) * (-1), int(denom))
        newTable.iloc[0][pos] = f'{frac}'

    print('\nВТОРОЙ ЭТАП')
    print(newTable)

    return newTable, targetCoef


def printResult(var, tableExVersion, grad):
    if var == 1:
        print('\nОптимальное решение')
        r = 'eq'
        masIndex = tableExVersion.index

        string = f"z* = {tableExVersion.iloc[0][r]}; "

        for i in range(1, len(masIndex)):
            string += f'{masIndex[i]}* = {tableExVersion.iloc[i]["eq"]}; '
        for i in list(tableExVersion):
            if i not in masIndex and i != 'eq':
                string += f'{i}* = 0; '
        print(f'{string}')

    if var == 2:
        mode = 0
        print('\nРезультаты первого этапа:')
        r = 'eq'
        masIndex = tableExVersion.index

        for i in masIndex:
            if re.match(r'R', i):
                print(f'Условие R = 0 не выполнилось')
                mode = 1


        if grad == 'min':
            string = f"{grad} z' = {Fraction(tableExVersion.iloc[0][r]) * (-1)}; "
        else:
            string = f"{grad} z' = {tableExVersion.iloc[0][r]}; "

        for i in range(1, len(masIndex)):
            string += f'{masIndex[i]} = {tableExVersion.iloc[i]["eq"]}; '
        for i in list(tableExVersion):
            if i not in masIndex and i != 'eq':
                string += f'{i} = 0; '
        print(f'{string}')

        if mode == 1:
            sys.exit(0)


def printDiphasicResult(tableExVersion, targetCoef, grad):
    print('\nОптимальное решение:')
    r = 'eq'
    masIndex = []
    for i in tableExVersion.index:
        masIndex.append(i)

    if grad == 'min':
        string = f"{grad} z* = {Fraction(tableExVersion.iloc[0][r]) * (-1)}; "
    else:
        string = f"{grad} z* = {tableExVersion.iloc[0][r]}; "

    for i in list(tableExVersion):
        if i != 'eq' and i != 'z':
            if i in targetCoef:
                if i in masIndex:
                    index = masIndex.index(i)
                    string += f'{i}* = {tableExVersion.iloc[index]["eq"]}; '
                else:
                    string += f'{i}* = 0; '
            else:
                string += f'{i}* = 0; '
    print(f'{string}')


def printTableForLatex(table, iteration, column, string):
    str = '\\begin{table}[!ht]\n'
    str += '    \centering\n'
    str += '    \\begin{tabular}{|'
    length = table.shape[1]

    for i in range(length + 1):
        str += 'c|'

    str += '}\n    \\hline \n       '

    for i in list(table):
        varX = re.search(r'x\d', i)
        varR = re.search(r'R\d', i)
        if i == 'eq':
            str += f' & = \\\\ \\hline \n'
        elif i == 'z':
            str += f' & z'
        elif varX is not None:
            letter = []
            for s in varX[0]:
                letter.append(s)
            str += f' & $x_{letter[1]}$'
        elif varR is not None:
            letter = []
            for s in varR[0]:
                letter.append(s)
            str += f' & $R_{letter[1]}$'

    buffer = table.index
    indexes = []

    for i in buffer:
        varX = re.search(r'x\d', i)
        varR = re.search(r'R\D', i)
        if varX is not None:
            letter = []
            for s in varX[0]:
                letter.append(s)
            indexes.append(f'$x_{letter[1]}$')
        elif varR is not None:
            letter = []
            for s in varR[0]:
                letter.append(s)
            indexes.append(f'$R_{letter[1]}$')
        else:
            indexes.append(i)

    for i in range(table.shape[0]):
        str += f'       {indexes[i]}'
        for j in list(table):
            if j == column and i == string:
                str += f' & {table.iloc[i][j]}*'
            else:
                str += f' & {table.iloc[i][j]}'
        str += '\\\\ \\hline \n'

    str += '    \\end {tabular}\n'
    str += '    \\medskip\n'
    str += '    \\caption{Итерация' + f'{iteration}' + '}\n'
    str += '\\end{table}\n'

    file.write(str)


def printExprForLatex(variant):
    os.chdir('/Users/enifen/PycharmProjects/MIO_LABS/SIMPLEX')
    fileName = f'var{variant}.txt'
    global file
    file = open(fileName, "w")