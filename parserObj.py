# ИСПОЛЬЗОВАТЬ ГЛОБАЛЬНЫЙ ИНТЕРПРИТАТОР, ИНАЧЕ ОН НЕ ВИДИТ БИБЛИОТЕКИ numpy и PIL

import numpy as np
from PIL import Image, ImageOps 
from lines import *
import random

def parseObj(filename):
    vertices = [] # Массив под все вершины по порядку. len = число вершин
    faces = [] # Массив под номера вершин, образующих полигоны, грани. len = число вершин
    polygonsDotAmount = [] # Число вершин в каждом полигоне. len = число полигонов
    with open(filename, 'r') as file:
        for line in file:
            if (line.startswith('v ')):
                dot = line.strip('\n').split(' ')[1:]
                cords = list(map(float, dot))
                vertices.append((cords[0], cords[1]))
            elif line.startswith('f '):
                parts = line.strip('\n').split(' ')[1:]
                dotAmount = len(parts)
                polygonsDotAmount.append(dotAmount)
                for line in parts:
                    part = list(map(int, line.split('//')))
                    faces.append(part[0])
    return vertices, faces, polygonsDotAmount

def drawObject(image, width, height, color, faces, polygonsDotAmount, pixelVertices):
    # ОТРИСОВКА ТОЧЕК
    for pixel in pixelVertices:
        image[int(pixel[1]), int(pixel[0])] = color

    # ОТРИСОВКА РЕБЕР И ТРЕУГОЛЬНИКОВ
    usedVertices = 0
    for dotAmount in polygonsDotAmount:
        for i in range(1, dotAmount - 1):
            p0 = pixelVertices[faces[0 + usedVertices]-1]
            p1 = pixelVertices[faces[i + usedVertices]-1]
            p2 = pixelVertices[faces[i + 1 + usedVertices]-1]
            bresenham_line(image, p0[0], p0[1], p1[0], p1[1], color)
            bresenham_line(image, p1[0], p1[1], p2[0], p2[1], color)
            bresenham_line(image, p2[0], p2[1], p0[0], p0[1], color)

            randomColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            draw_triangle(p0[1], p0[0], p1[1], p1[0], p2[1], p2[0], image=image, width=width, height=height, color=randomColor) # Раскрашиваем треугольники в разные цвета, координаты х и у поменяли местами, т.к. у нас матрица в ней строки - х а столбцы у, а в системе координат наоборот
        usedVertices += dotAmount
    return image

def main():
    objFilename = "PlatonicSolids.obj"
    width = 1280 # Задаем разрешение
    height = 720
    image = np.full((height, width, 3), 255, dtype=np.uint8) # Создаем массив под изображение
    color = (0, 0, 255) # Выбираем цвет

    vertices, faces, polygonsDotAmount = parseObj(objFilename)

    # Задаем сдвиг и размер для масштабирования
    x_offset= width//2
    y_offset= 0
    size= 30
    pixelVertices = [] # Массив точек отмасштабированной картинки
    for vertice in vertices:
        x, y = vertice[0]*size + x_offset, vertice[1]*size + y_offset
        pixelVertices.append((x, y))

    resultImage = drawObject(image=image, width=width, height=height, color=color, faces=faces, polygonsDotAmount=polygonsDotAmount, pixelVertices=pixelVertices)

    image = Image.fromarray(resultImage)
    image = ImageOps.flip(image)
    image.show()

if __name__ == "__main__":
    main()