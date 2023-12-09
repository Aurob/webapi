import os
import json
import re

data_folder = '/var/www/rau.dev/api/data/'

def file(filename):
    try:
        with open(data_folder + filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        return None
    
def upsert(filename, data):
    try:
        with open(data_folder + filename, 'w') as f:
            json.dump(data, f)
        return True
    except Exception as e:
        return False