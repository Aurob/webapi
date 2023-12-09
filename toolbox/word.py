from nltk.corpus import words
import random
import requests

word_list = words.words()

def define(word):
    req = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
    if req.status_code == 200:
        return req.json()[0]['meanings'][0]['definitions'][0]['definition']
    return req.json()

def words(n:int=1):
    if n > 1000:
        n = 1000
        
    return [{'word': random.choice(word_list), 'definition': define(random.choice(word_list))} for i in range(n)]

def default(data:int=1):
    if 'n' in data and str(data['n']).isdigit():
        return words(int(data['n']))
    return words(1)
    
