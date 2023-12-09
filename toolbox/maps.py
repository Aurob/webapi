import cv2
import numpy as np
import requests
import random
import imageio
import io
import base64

base_url = 'https://maps.googleapis.com/maps/api/streetview?'
key = 'BING_API_KEY'
size = '640x640'


import os

fetched = {}
def fetch_image(lat, lon, heading, pitch, fov=90):
    
    param_hash = hash((lat, lon, heading, pitch, fov))
    image_path = f"../data/maps/images/{param_hash}.png"
    
    if param_hash in fetched:
        return fetched[param_hash]
    
    query = f"{base_url}size={size}&radius=4000&location={lat},{lon}&fov={fov}&heading={heading}&pitch={pitch}&key={key}"
    response = requests.get(query)
    image = np.array(bytearray(response.content), dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    
    return image

def create_skybox(lat, lon):
    # Define headings and pitches for the six faces of the cube
    faces = {
        "front": 0,
        "back": 180,
        "left": 270,
        "right": 90,
        "top": -90,
        "bottom": 90
    }
    
    # Dictionary to store the skybox textures
    skybox_textures = {}
    
    # Set pitch to 0 for normal cube faces; override for top and bottom faces
    default_pitch = 0

    # Loop through each face and fetch the corresponding image
    for face_name, heading in faces.items():
        pitch = default_pitch
        if face_name in ["top", "bottom"]:
            # Use fov=180 for the top and bottom to get the full sky/ground image
            pitch = faces[face_name]
            image = fetch_image(lat, lon, heading, pitch, fov=180)
            # image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            image = fetch_image(lat, lon, heading, pitch)
        
        # Save or process the image as needed
        skybox_textures[face_name] = image
    
    return skybox_textures

def skybox(lat=0, lon=0, face='front'):
    skybox_images = create_skybox(lat, lon)
    for face_name, image in skybox_images.items():
        if face_name == face:
            _, img_encoded = cv2.imencode('.png', image)
            return {'image': img_encoded, 'imgtype': 'image/png'}
    return {'image': 'no image', 'imgtype': 'text/plain'}

def make_gif(frames, fps):
    stream = io.BytesIO()
    imageio.mimsave(stream, frames, format='gif', fps=fps, loop=0)
    stream.seek(0)
    return stream.getvalue()

def spin():
    # return a gif of a random location 
    # with a random heading and pitch
    h = 0 #random.randint(0, 360)
    p = 0 # Keep pitch at 0 for a level horizon
    # Latitude range for land-heavy areas, avoiding polar extremes
    lat = random.randint(0,90)
    # Longitude range for land-heavy areas, avoiding excessive ocean coverage
    lon = random.randint(-90, 90)
    print(f'lat: {lat}, lon: {lon}')
    images = []
    
    for i in range(0, 360, 10):
        image = fetch_image(lat, lon, h + i, p)
        images.append(image)
    
    gif = make_gif(images, 6)
    
    return {'b64image': base64.b64encode(gif).decode('utf-8'), 'imgtype': 'image/gif'}


    
    
def default():
    return base_url


#'47.5763831,-112.4211769'