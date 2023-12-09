import string
import random
import os
import string
import time
from lib.private import private

root = '/var/www/rau.dev/api/data/zk/'

cache = {}

def list():
    return os.listdir(root)

@private
def write(title, data):
    
    try:
        with open(root + title, 'w') as f:
            f.write(data)
            cache[title] = data
            return True
    except:
        return False

def content(title):
    if title in cache:
        return cache[title]
    
    try:
        with open(root + title, 'r') as f:
            data = f.read()
            cache[title] = data
            return data
    except:
        return ''

def add(title, data):
    if title in cache:
        return False
    
    write(title, data)

def update(title, data):
    return title, data
    if title not in cache:
        return False
    
    write(title, data)

def get(title):
    if title in cache:
        return cache[title]
    
    return content(title)

def default(data):
    if 't' in data or 'title' in data:
        title = data['t'] or data['title']
        return content(title)
    
    return list()