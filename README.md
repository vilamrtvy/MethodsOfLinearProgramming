## LINEAR PROGRAMMING METHODS /// МЕТОДЫ ЛИНЕЙНОГО ПРОГРАММИРОВАНИЯ

## ENGLISH DOCUMENTATION

At first you need to install the necessary libraries:    
* ```pandas```
* ```sympy```
____
After, run the project and select the appropriate work option:
* ```1``` for simplex method
* ```2``` for two-phase simplex method
____
Then you need to enter the equations, according to the rules   

### INPUT RULES

Put a multiplication sign between the coefficient and the variable
```
✅ 4*x1
❌ 4x1
```

Put a space between polynomials and signs
```
✅ 4*x1 + 5*x2
❌ 4*x1+5*x2
```

Signs **equal** / **greater than or equal** / **less than or equal**
```
4*x1 + 5*x2 = 10
4*x1 + 5*x2 >= 10
4*x1 + 5*x2 <= 10
```

The main function is written according to the same rules
```
z = x1 + 2*x2
```

For **two-phase** simplex method, it is **obligatory** to indicate the type of problem (min / max)
```
z = x1 + 2*x2 -> max
z = x1 - 2*x2 -> min
```

Type **end** in the end)
```
z = x1 - 2*x2 -> max
2*x1 + 3*x2 <= 15
x1 + 2*x2 >= 6
x1 + x2 <= 8
end
```

### GOOD LUCK AND SUCCESS

____


## РУССКАЯ ДОКУМЕНТАЦИЯ

Для начала установите необходимые библиотеки:  
* ```pandas```
* ```sympy```
____
Затем, после запуска проекта, выберите нужный вариант работы:
* ```1``` для симплекс метода
* ```2``` для двухфазного симплекс метода
____
После этого нужно ввести уровнения, исходя из правил

### ПРАВИЛА ВВОДА

Между коэффициентом и переменной ставится знак умножения
```
✅ 4*x1
❌ 4x1
```

Между полиномами и знаками ставится знак пробела
```
✅ 4*x1 + 5*x2
❌ 4*x1+5*x2
```

Знаки **равно** / **больше либо равно** / **меньше либо равно**
```
4*x1 + 5*x2 = 10
4*x1 + 5*x2 >= 10
4*x1 + 5*x2 <= 10
```

Основная функция пишется по тем же правилам
```
z = x1 + 2*x2
```

Для **двухфазного** симплекс метода **необходимо** указывать вид задачи (min / max)
```
z = x1 + 2*x2 -> max
z = x1 - 2*x2 -> min
```

Ставьте **end** в конце)
```
z = x1 - 2*x2 -> max
2*x1 + 3*x2 <= 15
x1 + 2*x2 >= 6
x1 + x2 <= 8
end
```

### УДАЧИ И УСПЕХОВ
