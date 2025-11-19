import numpy as np
from PIL import Image

def read_polygons():
    # Считывает вершины модели
    polygons = []
    with open("model_1.obj", 'r') as file:
        for line in file:
            parts = line.strip().split()
            if parts and parts[0] == 'v':
                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])
                polygons.append([x, y, z])
    return polygons

def read_faces():
    # Считывает полигоны 
    faces = []
    with open("model_1.obj", 'r') as file:
        for line in file:
            parts = line.strip().split()
            if parts and parts[0] == 'f':
                # Берём только номера вершин
                # f 3444/3647/3674 - Номера вершин
                face = [int(p.split('/')[0]) for p in parts[1:]]
                faces.append(face)
    return faces

def draw_line(image, x0, y0, x1, y1, color):
    # Рисует линию между двумя точками по Брезенхейму
    swapped = False
    if abs(x0 - x1) < abs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        swapped = True

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    dx = x1 - x0
    dy = abs(y1 - y0)
    error = 0
    y_step = 1 if y1 > y0 else -1

    for x in range(x0, x1 + 1):
        if swapped:
            image[x, y0] = color
        else:
            image[y0, x] = color

        error += dy * 2
        if error > dx * 2:
            error -= dx * 2
            y0 += y_step

# Загружаем данные
polygons = read_polygons()
faces = read_faces()

# Создаём изображение
img = np.zeros((2000, 2000), dtype=np.uint8)
color = 255
scale = 8000
offset = 900

# Рисуем все грани
for face in faces:
    # Получаем три вершины треугольника 
    v1_idx, v2_idx, v3_idx = face[0] - 1, face[1] - 1, face[2] - 1
    
    # Масштабируем и смещаем координаты
    x0, y0 = scale * polygons[v1_idx][0] + offset, scale * polygons[v1_idx][1] + offset
    x1, y1 = scale * polygons[v2_idx][0] + offset, scale * polygons[v2_idx][1] + offset
    x2, y2 = scale * polygons[v3_idx][0] + offset, scale * polygons[v3_idx][1] + offset

    # Рисуем три ребра треугольника
    draw_line(img, x0, y0, x1, y1, color)
    draw_line(img, x0, y0, x2, y2, color)
    draw_line(img, x2, y2, x1, y1, color)

# Сохраняем изображение
image = Image.fromarray(img, mode='L')
image.save('bunny.png')