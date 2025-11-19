import numpy as np
from PIL import Image

def pars():
    pars_mass = []
    with open("model_1.obj", 'r') as file:
        for line in file:
            mass = line.strip().split()
            if mass[0] == 'v':
                x = float(mass[1])
                y = float(mass[2])
                z = float(mass[3])
                pars_mass.append([x, y, z])
    return pars_mass

# Читаем вершины
v_arr = pars()

# Создаём изображение
img = np.zeros((1000, 1000), dtype=np.uint8)

# Масштабируем
if len(v_arr) > 0:
    coords = np.array(v_arr)
    min_x, max_x = np.min(coords[:, 0]), np.max(coords[:, 0])
    min_y, max_y = np.min(coords[:, 1]), np.max(coords[:, 1])
    
    scale_x = 999 / (max_x - min_x) if max_x != min_x else 1
    scale_y = 999 / (max_y - min_y) if max_y != min_y else 1
    
    for v in v_arr:
        newX = int((v[0] - min_x) * scale_x)
        newY = int((v[1] - min_y) * scale_y)
        # Проверяем, что координаты в пределах изображения
        if 0 <= newX < 1000 and 0 <= newY < 1000:
            img[newY, newX] = 255

image = Image.fromarray(img, mode='L')
image.save("High_points.png")