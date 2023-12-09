import cv2
import base64
import numpy as np
import io
import random
import math
import imageio
import noise
import time
import textwrap
# from lib.private import private
import os
'''
    Image generation only
    - make circle
    - make rectangle
    - make line
    - make text
    - make image
'''
def make_image(width = 128, height = 128, color = (0, 0, 0)):
    return np.zeros((height, width, 3), np.uint8)

#@private
def make_circle(img, x, y, radius, color, thickness):
    if img is None:
        img = make_image()
    return cv2.circle(img, (x, y), radius, color, thickness)

#@private
def rand_poly(img, x, y, radius, color, thickness):
    if img is None:
        img = make_image()
    points = [[random.randint(0, 2*radius) , random.randint(0, 2*radius)] for i in range(10)]
    pts = np.array(points, np.int32)
    cv2.polylines(img, [pts], True, (0,255,255))
    return img

def rand_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

#@private
def poly_circle(img, x, y, radius, color, thickness, step=0):
    if img is None:
        img = make_image()
    
    points = []
    for i in range(0, 360, 10):
        x1 = int(x + radius * math.cos(i * math.pi / 180)) + noise.snoise2(i, step) * 20
        y1 = int(y + radius * math.sin(i * math.pi / 180)) + noise.snoise2(i, step) * 20
        points.append([x1, y1])
    
    pts = np.array(points, np.int32)
    cv2.polylines(img, [pts], True, color)
    return img

#@private
def make_gif(frames, fps):
    stream = io.BytesIO()
    imageio.mimsave(stream, frames, format='gif', fps=fps, loop=0)
    stream.seek(0)
    return stream.getvalue()

def test_gif():
    frames = []
    color = rand_color()    
    for i in range(10):
        img = make_image()
        img = poly_circle(img, 64, 64, 50, color, 1, i)
        frames.append(img)
    
    gif = make_gif(frames, 6)
    return {'b64image': base64.b64encode(gif).decode('utf-8'), 'imgtype': 'image/gif'}

def rotate_image(img, angle):
    # get image height, width
    (h, w) = img.shape[:2]
    # define center of the image
    center = (w / 2, h / 2)
    
    # perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h))
    return rotated


def add_text(img=None, text='hello world', x=0, y=0, font=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(255,255,255), thickness=1):
    if img is None:
        img = make_image()
    
    # Split the text into lines
    lines = textwrap.wrap(text, width=20)
    
    y_text = y
    for line in lines:
        # Get text width and height
        (text_width, text_height) = cv2.getTextSize(line, font, fontScale=fontScale, thickness=thickness)[0]
        
        # If the text width or height exceeds the image width or height, scale down the font
        if text_width > img.shape[1] or text_height > img.shape[0]:
            scale_factor = min(img.shape[1] / text_width, img.shape[0] / text_height)
            fontScale *= scale_factor
            (text_width, text_height) = cv2.getTextSize(line, font, fontScale=fontScale, thickness=thickness)[0]
        
        y_text += text_height
        
        # Put text on image, shifted to the right by half of the text width
        img = cv2.putText(img, line, (x + text_width // 2, y_text), font, fontScale, color, thickness, cv2.LINE_AA)
    
    # Rotate the entire image 90 degrees to the right
    # img = rotate_image(img, 90)
    
    return format(img)

def testnoise():
    return {'result': noise.snoise2(random.randint(0, 100), 1)}

def testtext():
    return add_text(text='hello world')#

#@private
def format(img):
    if img is None:
        img = make_image()
    is_success, buffer = cv2.imencode(".jpg", img)
    io_buffer = io.BytesIO(buffer)
    
    return {'image': io_buffer.getvalue(), 'imgtype': 'image/jpeg'}

paths = os.listdir('/var/www/rau.dev/api/data/gpt/')
def portal_image():
    path = random.choice(paths)
    image = cv2.imread('/var/www/rau.dev/api/data/gpt/' + path)
    return format(image)

# one-time function to make a gif out of all the images in the gpt folder
def make_gif_temp():
    frames = []
    for path in paths:
        image = cv2.imread('/var/www/rau.dev/api/data/gpt/' + path)
        # fix color
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        frames.append(image)
    
    gif = make_gif(frames, .4)
    with open('/var/www/rau.dev/api/data/gpt.gif', 'wb') as f:
        f.write(gif)
    return format(image)
        
def default():
    img = rand_poly(make_image(), 64, 64, 50, (255, 255, 255), 1)
    # img = poly_circle(None, 64, 64, 50, (255, 255, 255), 1)
    return format(img)