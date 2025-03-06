# ИСПОЛЬЗОВАТЬ ГЛОБАЛЬНЫЙ ИНТЕРПРИТАТОР, ИНАЧЕ ОН НЕ ВИДИТ БИБЛИОТЕКИ numpy и PIL

import math
import numpy as np
from PIL import Image, ImageOps

import lines

def main():
    width, height = 512, 512 # ЗДЕСЬ МЕНЯТЬ РАЗРЕШЕНИЕ ИЗОБРАЖЕНИЯ

    center_x = width/2
    center_y = height/2

    image = np.full((width, height, 3), 255, dtype = np.uint8) # Создаем массив width*height заполненный значениями 0, тип данных - uint8 (базовый целочисленный тип с размером 8 бит). Поставив вместо нуля 255, получим что все пиксели будут иметь 255 красног, зеленого и синего, т.е. белый, т.к. вся матрица заполнится максимальными значениями цветового пространства RGB

    # for i in range(width):
    #     for j in range(height):
    #         image[i, j, 2] = 255    # Этот цикл пробегают всю матрицу и заполняет 2 канал значениями 255, в итоге будет синяя картинка, красная если канал под номеро 0, и зеленая если канал под номером 1

    # for i in range(width):
    #     for j in range (height):
    #         image[i, j] = (i + j) % 256 # Заменяет все пиксели на сумму их координат по модулю 256, в итоге получится своего рода градиент

    hypotenuse = 150
    color = (0, 0, 255)
    line_amount = 20
    for i in range(1, line_amount + 1): # Задаем число прямых, которые будут делить окружность на n частей с равными центральными углами
        x0, y0 = center_x, center_y
        x1, y1 = math.cos(2*math.pi*i/line_amount)*hypotenuse + x0, math.sin(2*math.pi*i/line_amount)*hypotenuse + y0 # Координаты второй точки прямой. Число 2*pi/line_amount делит окружность на столько частей, сколько прямых, а i позволяет задать угол каждой прямой. Тут формула переводим из полярных координат в декартовы. x1 = P cos(a) + x0, y1 = P sin(a) + y0. Угол a = 2*pi/line_amoun, но это угол в 1 четверти, его нужно провернть по всей окружности, чтобы поделить ее, поэтому домножили на счетчик отрисованных прямых i

        if (abs(x1-x0) < 0.0000001): x1 = x0 # На случай, когда прямых становится много (например когда их 20, у 15 прямой (i = 15) x1 и x0 отличаются на 3*10^-14) x1 и x0 могу отличаться на очень малую велчину из за чего в ф-ии x_loop_line_hotfix1 случается краш без той апроксимации

        # см. lines.py
        #count = 50
        #lines.dotted_line(image, x0, y0, x1, y1, count, color)
        #lines.dotted_line_v2(image, x0, y0, x1, y1, color)
        #lines.x_loop_line(image, x0, y0, x1, y1, color)
        #lines.x_loop_line_hotfix1(image, x0, y0, x1, y1, color)
        #lines.x_loop_line_hotfix2(image, x0, y0, x1, y1, color)
        #lines.x_loop_line_v2(image, x0, y0, x1, y1, color)
        #lines.x_loop_line_no_y_calc(image, x0, y0, x1, y1, color)
        #lines.x_loop_line_no_y_calc_v2(image, x0, y0, x1, y1, color)
        lines.bresenham_line(image, x0, y0, x1, y1, color)

    img = Image.fromarray(image)
    #img = Image.fromarray(image, mode = 'RGB') - так выглядит в случае RGB цветового пространства, но тогда в 10 строке скобка (width, height) заменится на скобку: (width, height, 3), последняя цифра число цветовых каналов, 3х мерная, сборная матрица
    
    img.show()

if __name__ == '__main__':
    main()