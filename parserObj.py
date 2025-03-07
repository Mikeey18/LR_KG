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
                vertices.append((cords[0], cords[1], cords[2])) # Теперь добавляем и координату z, для определения нормалей и отрисовки света
            elif line.startswith('f '):
                parts = line.strip('\n').split(' ')[1:]
                dotAmount = len(parts)
                polygonsDotAmount.append(dotAmount)
                for line in parts:
                    part = list(map(int, line.split('/')))
                    faces.append(part[0])
    return vertices, faces, polygonsDotAmount

def drawObject(image, width, height, color, light, faces, polygonsDotAmount, pixelVertices, z_buffer):
    # ОТРИСОВКА ТРЕУГОЛЬНИКОВ
    usedVertices = 0
    for dotAmount in polygonsDotAmount:
        for i in range(1, dotAmount - 1):
            p0 = pixelVertices[faces[0 + usedVertices]-1]
            p1 = pixelVertices[faces[i + usedVertices]-1]
            p2 = pixelVertices[faces[i + 1 + usedVertices]-1]

            n = normal(p0[0], p0[1], p0[2], p1[0], p1[1], p1[2], p2[0], p2[1], p2[2])
            cos = (np.dot(n, light))/(np.linalg.norm(n)*np.linalg.norm(light)) # косинус угла между нормалью и камерой (из лин. алгебры), если полигон направлен в камеру, то косинус должен быть меньше нуля, т.к. векторы смотрятт в разные стороны и угол будет больше либо равен 90 градусов, т.е. косинус должен быть меньше либо равен 0.
            if (cos > 0): continue
            
            # Цвет теперь будет в оттенках серого
            TriangleColor = (-color[0]*cos, -color[1]*cos, -color[2]*cos)
            draw_triangle(p0[1], p0[0], p0[2], p1[1], p1[0], p1[2], p2[1], p2[0], p2[2], image=image, width=width, height=height, color=TriangleColor, z_buffer=z_buffer) # Раскрашиваем треугольники в разные цвета, координаты х и у поменяли местами, т.к. у нас матрица в ней строки - х а столбцы у, а в системе координат наоборот
        usedVertices += dotAmount
    return image

def main():
    objFilename = "Rabbit.obj"
    width = 1280 # Задаем разрешение
    height = 1280
    image = np.full((width, height, 3), (0, 0, 255), dtype=np.uint8) # Создаем массив под изображение
    z_buffer = np.full((width, height), 99999.99999) # z буфер, имеет такой же размер как и наше изображение, будет показывать расстояние от камеры то дочки на сцене (не перекрытой ничем другим)
    color = (255, 255, 255) # Выбираем цвет
    light = (0, 0, 1) # Направление света от центра координат (пока что там же где и камера, т.е. свет идет в сторону положительно нарпавления оси z, от камеры)

    vertices, faces, polygonsDotAmount = parseObj(objFilename)

    # Задаем сдвиг, глубину и размер для масштабирования. Если они будут слишком велики, то будет выход за границы изображения и ничего не будет видно
    x_offset = width//2
    y_offset = height//4
    z_offset = 0
    size= 5000 # Если значение будет слишком большим, моделька может выйти за рамки сцены (за рамки изображения) и ничего не будет видно
    pixelVertices = [] # Массив точек отмасштабированной картинки
    for vertice in vertices:
        x, y, z = vertice[0]*size + x_offset, vertice[1]*size + y_offset, vertice[2]*size + z_offset
        pixelVertices.append((x, y, z))

    resultImage = drawObject(image=image, width=width, height=height, color=color, light=light, faces=faces, polygonsDotAmount=polygonsDotAmount, pixelVertices=pixelVertices, z_buffer=z_buffer)

    image = Image.fromarray(resultImage)
    image = ImageOps.flip(image)
    image.show()

if __name__ == "__main__":
    main()