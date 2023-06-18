import pandas as pd
from tabledata import simplexTable, simplexTableDiphasic, beforeTargetString,\
    transferDiphasic, printResult, printDiphasicResult, printTableForLatex
import sys

if __name__ == '__main__':
    #variant = int(input('Симплекс метод, двухфазный симплекс метод или двойственная задача? 1 / 2 / 3: '))
    variant = int(input('Симплекс, двухфазный? 1 / 2: '))
    if variant == 1 or variant == 2:
        grad, targetEqual, tableExVersion = None, None, []
        if variant == 1:
            tableExVersion = simplexTable()
        if variant == 2:
            tableExVersion, targetEqual, grad = simplexTableDiphasic()

        i, min = 1, 1
        while min == 1:
            tableExVersion, min = beforeTargetString(tableExVersion, i)
            if min == 0:
                break
            i += 1

        #printTableForLatex(tableExVersion, i, None, None)
        printResult(variant, tableExVersion, grad)

        if variant == 1:
            sys.exit(0)
        elif variant == 2:
            tableExVersion, targetCoef = transferDiphasic(tableExVersion, targetEqual)

            i, min = 1, 1
            while min == 1:
                tableExVersion, min = beforeTargetString(tableExVersion, i)
                if min == 0:
                    break
                i += 1

            #printTableForLatex(tableExVersion, i, None, None)
            printDiphasicResult(tableExVersion, targetCoef, grad)

    elif variant == 3:
        print('Введите коэффициенты через запятую и пробел. Первым введите главное уравнение. В конце напишите end: ')
        equation = input().split(', ')
        n = len(equation)
        mas = [equation]

        equation = (input().split(', '))
        if n < len(equation):
            n = len(equation)

        while 'end' not in equation:
            mas.append(equation)
            equation = (input().split(', '))
            if n < len(equation):
                n = len(equation)

        names = ['Q']
        for i in range(1, len(mas)):
            names.append(f'y{i}')

        names.append('eq')

        tableData = pd.DataFrame(columns=names, index=range(n), dtype=object)

        tableData.loc[0]['Q'] = 1
        tableData.loc[0]['eq'] = 0
        for j in list(tableData):
            if j != 'Q' and j != 'eq':
                index = tableData.columns.get_loc(j)
                tableData.loc[0][j] = mas[index][len(mas[index]) - 1]
                tableData.loc[0][j] = mas[index][len(mas[index]) - 1]

        for i in range(1, tableData.shape[0]):
            for j in list(tableData):
                if j == 'Q':
                    tableData.loc[i][j] = 0
                elif j == 'eq':
                    tableData.loc[i][j] = mas[0][i - 1]
                else:
                    index = tableData.columns.get_loc(j)
                    tableData.loc[i][j] = mas[index][i - 1]

        print(tableData)
        
