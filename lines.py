# ИСПОЛЬЗОВАТЬ ГЛОБАЛЬНЫЙ ИНТЕРПРИТАТОР, ИНАЧЕ ОН НЕ ВИДИТ БИБЛИОТЕКИ numpy и PIL

import numpy as np
import math

def dotted_line(image, x0, y0, x1, y1, count, color): # Рисует пунктирную линию с заданым числом точек count между точками (x0,y0) и (x1,y1)
    step = 1.0/count
    for t in np.arange(0, 1, step): # np.arange(0,1,step) - массив с несколькими значениями от 0 до 1. Если step = 0.2 (т.е. count = 5), то массивы выглядит так: [0, 0.2, 0.4, 0.6, 0.8]. Т.е. длина массва равна count
        # Линейная интерполяция в параметрической форме в формулу y = y0 + ((y1-y0)*(x-x0))/(x1-x0) подставляем x = x0 + kt а потом y = y0 + mt, получим формулу линейной интерполяции для координат x и y в параметрической форме записи с направляющим вектором прямой (k,m)
        x = round((1.0 - t)*x0 + t*x1)
        y = round((1.0 - t)*y0 + t*y1)
        image[y, x] = color # [y, x], а не [x, y], т.к. в матрицах 1 координата - строки, втора - столбцы, а у нас по горизонтали (строки) - 1 координата, а по вертикали (столбцы) - 2 координата\

def dotted_line_v2(image, x0, y0, x1, y1, color): # Тоже рисует пунктирную линию, но параметр count не нужно вводить за него мы берем гипотенузу
    count = math.sqrt((x0-x1)**2 + (y0-y1)**2) # (x0-x1) и (y0-y1) - множество точек вокру начала координат, при достаточно большом кол-ве образуют окружность вокруг начала координат. Сумма (x0-x1)**2 + (y0-y1)**2 - квадрат гипотинузы прямоугольно треугольника (или обычной прямой если угол с осью х равен 0, 90, 180, 270, 360) достроенного от точек: (x0, y0), (x1, y0). Итог - count = hypotenuse в 23 строке файла main
    step = 1.0/count
    for t in np.arange(0, 1, step): 
        x = round((1.0 - t)*x0 + t*x1)
        y = round((1.0 - t)*y0 + t*y1)
        image[y, x] = color

def x_loop_line(image, x0, y0, x1, y1, color): # Новы подхол. Цикл по х. Первая проблема этого рещения что начальная точка может оказаться правее кнечной, такие линии отрисовываться не будут. Вторая - когда шаг по х меньше, чем по y, т.е. y растет быстрее x, то значения по x будет не хватать для отрисовки всех y. Появятся разрвы (как правило в случаях недостаточно острых углов, больше 60)
    for x in range(int(x0), int(x1)):
        t = (x - x0)/(x1 - x0) # Опять линейная интерполяция (делим на x1-x0, т.к. это серидина между x0 и x1)
        y = round ((1.0 - t)*y0 + t*y1)
        image[y, x] = color

def x_loop_line_hotfix1(image, x0, y0, x1, y1, color):  # Решение первой проблемы
    if (x0 > x1):
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    
    for x in range(int(x0), int(x1)):
        t = (x - x0)/(x1 - x0)
        y = round ((1.0 - t)*y0 + t*y1)
        image[y, x] = color

def x_loop_line_hotfix2(image, x0, y0, x1, y1, color): # Решение второй проблемы
    xChange= False
    if (abs(x1-x0) < abs(y1-y0)):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xChange = True

    for x in range(int(x0), int(x1)):
        t = (x - x0)/(x1 - x0)
        y = round ((1.0 - t)*y0 + t*y1)
        if (xChange):
            image[x, y] = color
        else:
            image[y, x] = color

def x_loop_line_v2(image, x0, y0, x1, y1, color): # Рабочий вариант отрисовки линий
    xChange= False
    if (abs(x1-x0) < abs(y1-y0)):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xChange = True
    
    if (x0 > x1):
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    
    for x in range(int(x0), int(x1)):
        t = (x - x0)/(x1 - x0)
        y = round ((1.0 - t)*y0 + t*y1)
        if (xChange):
            image[x, y] = color
        else:
            image[y, x] = color

def x_loop_line_no_y_calc(image, x0, y0, x1, y1, color): # Отрисовка линий без вычислений y
    xChange= False
    if (abs(x1-x0) < abs(y1-y0)):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xChange = True

    if (x0 > x1):
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    y = y0
    deltaX = abs(x1 - x0)
    deltaY = abs(y1 - y0)
    Speed = deltaY/deltaX # Скорость роста функция, константа, некоторая постоянная величина на которую увеличивается y при шаге икса
    derror = 0.0 # Накапливаем смещение по y за каждый шаг по х начиная от центра нулевого пикселя. Как только перейдет за 0.5, мы окажемся на границе нового пикселя. Счетчик нужно сброить но до -0.5, т.к. мы будем не в центре а под ним.
    y_update = 1 if y1 > y0 else -1 # Если линия идет вверх, т.е. то y надо будет увеличить на 1, иначе уменьшить на 1

    for x in range (int(x0), int(x1)):
        if (xChange):
            image[x,int(y)] = color
        else:
            image[int(y),x] = color
        
        derror += Speed # После раскраски пикселя прямая продолжает расти (убывать), увеличивам (уменьшаем) смещение
        if derror >= 0.5: # Случай когда смещение окажется выше (ниже) или на гранцие нового пикселя
            y += y_update # Тогда нужно обновить высоту
            derror -= 1 # И сбросить счетчик

def x_loop_line_no_y_calc_v2(image, x0, y0, x1, y1, color): # Отрисовка линий бзе вычислений y в целых числах, что быстрее
    xChange= False
    if (abs(x1-x0) < abs(y1-y0)):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xChange = True

    if (x0 > x1):
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    y = y0
    deltaX = abs(x1 - x0)
    deltaY = abs(y1 - y0)
    Speed = 2.0*deltaX*(deltaY/deltaX) # Домножили на 2*deltaX, упрощаем и сокращаем, в итоге получаем алгоритм Брезенхема
    derror = 0.0
    y_update = 1 if y1 > y0 else -1

    for x in range (int(x0), int(x1)):
        if (xChange):
            image[x,int(y)] = color
        else:
            image[int(y),x] = color
        
        derror += Speed
        if (derror >= 2.0*deltaX*0.5): # Аналогично
            y += y_update
            derror -= 2.0*deltaX*1.0 # Аналогично

def bresenham_line(image, x0, y0, x1, y1, color): # Проведя дейсвтия описанные в прошлой ф-ии, получили алгорит Брезенхема отрисовки линий
    xChange= False
    if (abs(x1-x0) < abs(y1-y0)):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xChange = True

    if (x0 > x1):
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    y = y0
    deltaX = abs(x1 - x0)
    deltaY = abs(y1 - y0)
    Speed = 2*deltaY
    derror = 0
    y_update = 1 if y1 > y0 else -1

    for x in range (int(x0), int(x1)):
        if (xChange):
            image[x,int(y)] = color
        else:
            image[int(y),x] = color
        
        derror += Speed
        if (derror >= deltaX):
            y += y_update
            derror -= 2*deltaX