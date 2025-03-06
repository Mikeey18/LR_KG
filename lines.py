# ИСПОЛЬЗОВАТЬ ГЛОБАЛЬНЫЙ ИНТЕРПРИТАТОР, ИНАЧЕ ОН НЕ ВИДИТ БИБЛИОТЕКИ numpy и PIL

import numpy as np
import math

def bresenham_line(image, x0, y0, x1, y1, color):
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

# Наше изображение - система координат Х и У, где каждому центру пикселя соответствует целое значения int x0 и int y0. Для того, чтобы закрасить треугольник, нужно понять, где лежит центр пикселя относительно прямых, образующих этот треугольник. Для этого составляется 3 уравнения прямых по 3 точкам треугольника: (x - x0)(y1 - y0) - (x1 - x0)(y - y0), (x - x1)(y2 - y1) - (x2 - x1)(y - y1), (x - x2)(y0 - y2) - (x0 - x2)(y - y2), подставив в одно из этих уравнений прямой координаты произвольного пикселя (его центра) (x,y) можем получить 3 варианта значений: >0 если точка лежит выше прямой, <0 если ниже и 0 если на прямой. Введя новую систему координат (аффиную) слева направо снизу вверх зададим координаты вершин теругольника как (1, 0, 0), (0, 1, 0) и (0, 0, 1). Таким образом 3 уравнения прямых задают эту систему координат, причем, если точка лежит внутри или на границе треугольника, то все координаты будут >= 0.
def barycentric_coordinates(x0, y0, x1, y1, x2, y2, x, y): # Вычисляем барицентрические координаты для точки (x,y) с целочисленными координатами (точки на изображении) относительно вещественных вершин треугольника x0, y0, x1, y1, x2, y2
    lambda0 =  ((x - x2) * (y1 - y2) - (x1 - x2) * (y - y2)) / ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lambda1 = ((x0 - x2) * (y - y2) - (x - x2) * (y0 - y2)) / ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lambda2 = 1.0 - lambda0 - lambda1
    return lambda0, lambda1, lambda2

def draw_triangle(x0, y0, x1, y1, x2, y2, width, height, image, color):
    xmin = max(min(x0, x1, x2), 0)
    xmax = min(max(x0, x1, x2), width - 1)
    ymin = max(min(y0, y1, y2), 0)
    ymax = min(max(y0, y1, y2), height - 1)

    for x in range(int(xmin), int(xmax) + 1):
        for y in range(int(ymin), int(ymax) + 1):
            lambda0, lambda1, lambda2 = barycentric_coordinates(x0, y0, x1, y1, x2, y2, x, y)
            if (lambda0 >= 0 and lambda1 >= 0 and lambda2 >= 0): image[int(x), int(y)] = color