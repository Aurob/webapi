import requests


def default(data):
    d = None
    if 'd' in data:
        d = data['d']
    else:
        return False
    
    response = requests.get(f'http://api.conceptnet.io/query?start=/c/en/{d}&rel=/r/ExternalURL&limit=1000')
    obj = response.json()
    return [edge['end']['@id'] for edge in obj['edges']]