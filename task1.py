import numpy as np
from PIL import Image 

H, W = 500, 500

def create_black():
    img = np.zeros((H, W), dtype=np.uint8)
    image = Image.fromarray(img, mode='L') 
    image.save("hue1.png") 

def create_white():
    img = np.zeros((H, W), dtype=np.uint8)
    img[:, :] = 255
    image = Image.fromarray(img, mode='L')
    image.save("hue2.png")

def create_red():
    img = np.zeros((H, W, 3), dtype=np.uint8)
    img[...] = (255, 0, 0) 
    image = Image.fromarray(img, mode='RGB')
    image.save("hue3.png")

def create_gradient():
    i, j = np.meshgrid(np.arange(H), np.arange(W), indexing='ij')
    color = (i + j) % 256
    img = np.stack([color, color, color], axis=-1).astype(np.uint8)
    image = Image.fromarray(img, mode='RGB')
    image.save("hue4.png")

create_black()
create_white()
create_red()
create_gradient()