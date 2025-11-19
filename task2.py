import numpy as np
from PIL import Image
import math

H, W = 200, 200
R = 95  

# Все 9 алгоритмов 
def dotted_line(image, x0, y0, x1, y1, count, color):
    step = 1.0 / count
    t_vals = np.arange(0, 1, step)
    for t in t_vals:
        x = int(round((1 - t) * x0 + t * x1))
        y = int(round((1 - t) * y0 + t * y1))
        if 0 <= x < W and 0 <= y < H:
            image[y, x] = color
    return image

def dotted_line_2(image, x0, y0, x1, y1, color):
    dist = math.hypot(x1 - x0, y1 - y0)
    if dist == 0:
        return image
    count = max(1, int(dist))
    return dotted_line(image, x0, y0, x1, y1, count, color)

def x_loop_line(image, x0, y0, x1, y1, color):
    if x0 > x1:
        return x_loop_line(image, x1, y1, x0, y0, color)
    x0, x1 = int(x0), int(x1)
    if x0 == x1:
        return image
    for x in range(x0, x1 + 1):
        t = (x - x0) / (x1 - x0)
        y = int(round((1 - t) * y0 + t * y1))
        if 0 <= x < W and 0 <= y < H:
            image[y, x] = color
    return image

def x_loop_line_2(image, x0, y0, x1, y1, color):
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    return x_loop_line(image, x0, y0, x1, y1, color)

def x_loop_line_3(image, x0, y0, x1, y1, color):
    step = abs(y1 - y0) > abs(x1 - x0)
    if step:
        x0, y0, x1, y1 = y0, x0, y1, x1
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    x0, x1 = int(x0), int(x1)
    if x0 == x1:
        return image
    for x in range(x0, x1 + 1):
        t = (x - x0) / (x1 - x0)
        y = int(round((1 - t) * y0 + t * y1))
        px, py = (y, x) if step else (x, y)
        if 0 <= px < W and 0 <= py < H:
            image[py, px] = color
    return image

def x_loop_line_4(image, x0, y0, x1, y1, color):
    return x_loop_line_3(image, x0, y0, x1, y1, color) 

def x_loop_line_with_error(image, x0, y0, x1, y1, color):
    step = abs(y1 - y0) > abs(x1 - x0)
    if step:
        x0, y0, x1, y1 = y0, x0, y1, x1
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    x0, x1, y0 = int(x0), int(x1), int(y0)
    if x0 == x1:
        return image
    dx = x1 - x0
    dy = abs(y1 - y0)
    y = y0
    y_step = 1 if y1 > y0 else -1
    error = 0.0
    for x in range(x0, x1 + 1):
        px, py = (y, x) if step else (x, y)
        if 0 <= px < W and 0 <= py < H:
            image[py, px] = color
        error += dy / dx
        if error > 0.5:
            y += y_step
            error -= 1.0
    return image

def line_loop_eight_algorhythm(image, x0, y0, x1, y1, color):
    step = abs(y1 - y0) > abs(x1 - x0)
    if step:
        x0, y0, x1, y1 = y0, x0, y1, x1
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    x0, x1, y0 = int(x0), int(x1), int(y0)
    if x0 == x1:
        return image
    dx = x1 - x0
    dy = abs(y1 - y0)
    y = y0
    y_step = 1 if y1 > y0 else -1
    error = 0
    for x in range(x0, x1 + 1):
        px, py = (y, x) if step else (x, y)
        if 0 <= px < W and 0 <= py < H:
            image[py, px] = color
        error += 2 * dy
        if error > dx:
            y += y_step
            error -= 2 * dx
    return image

def bresenhem_algorighm(image, x0, y0, x1, y1, color):
    return line_loop_eight_algorhythm(image, x0, y0, x1, y1, color)

algorithms = [
    lambda img, x0, y0, x1, y1, c: dotted_line(img, x0, y0, x1, y1, 100, c),
    dotted_line_2,
    x_loop_line,
    x_loop_line_2,
    x_loop_line_3,
    x_loop_line_4,
    x_loop_line_with_error,
    line_loop_eight_algorhythm,
    bresenhem_algorighm
]

color = [255, 255, 255]

for idx, algo in enumerate(algorithms, 1):
    img = np.zeros((H, W, 3), dtype=np.uint8)
    for i in range(13):
        x0, y0 = 100, 100
        angle = 2 * np.pi * i / 13
        x1 = 100 + R * np.cos(angle)
        y1 = 100 + R * np.sin(angle)
        algo(img, x0, y0, x1, y1, color)
    Image.fromarray(img, mode='RGB').save(f"star{idx}.png")