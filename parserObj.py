# ИСПОЛЬЗОВАТЬ ГЛОБАЛЬНЫЙ ИНТЕРПРИТАТОР, ИНАЧЕ ОН НЕ ВИДИТ БИБЛИОТЕКИ numpy и PIL

import numpy as np
from PIL import Image, ImageOps 
from lines import *

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

def drawObject(image, color, faces, polygonsDotAmount, pixelVertices):
    # ОТРИСОВКА ТОЧЕК
    for pixel in pixelVertices:
        image[int(pixel[1]), int(pixel[0])] = color

    # ОТРИСОВКА РЕБЕР
    usedVertices = 0
    for dotAmount in polygonsDotAmount:
        for i in range(1, dotAmount - 1):
            p0 = pixelVertices[faces[0 + usedVertices]-1]
            p1 = pixelVertices[faces[i + usedVertices]-1]
            p2 = pixelVertices[faces[i + 1 + usedVertices]-1]
            bresenham_line(image, p0[0], p0[1], p1[0], p1[1], color)
            bresenham_line(image, p1[0], p1[1], p2[0], p2[1], color)
            bresenham_line(image, p2[0], p2[1], p0[0], p0[1], color)
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
        x, y = vertice[0]*size + x_offset, vertice[1]*size + y_offset # Масштабируем и смещаем изображение. Если не масштабировать точки с маленькими занчениямия по типу (0.0033, 0.0055) и (0.0011, 0.0066) будут считаться одинаковыми при округлении
        pixelVertices.append((x, y))

    resultImage = drawObject(image=image, color=color, faces=faces, polygonsDotAmount=polygonsDotAmount, pixelVertices=pixelVertices)

    # Берем первые три вершины треугольника для отрисовки
    x0 = pixelVertices[faces[0] - 1][0]
    y0 = pixelVertices[faces[0] - 1][1]
    x1 = pixelVertices[faces[1] - 1][0]
    y1 = pixelVertices[faces[1] - 1][1]
    x2 = pixelVertices[faces[2] - 1][0]
    y2 = pixelVertices[faces[2] - 1][1]
    draw_triangle(x0, y0, x1, y1, x2, y2, width=width, height=height, image=image, color=color)

    image = Image.fromarray(resultImage)
    image = ImageOps.flip(image)
    image.show()

if __name__ == "__main__":
    main()