import requests
import json
import lib.verify
import os

account_id = os.getenv('CF_ACCOUNT_ID')
database_id = os.getenv('CF_DATABASE_ID')
read_token = os.getenv('CF_READ_TOKEN')
edit_token = os.getenv('CF_EDIT_TOKEN')
url = 'https://api.cloudflare.com/client/v4/accounts/' + account_id + '/d1/database/' + database_id + '/query'

options = {
    'all': 'SELECT * FROM note',
    'user': 'SELECT * FROM note WHERE uuid = ?',
    'title': 'SELECT * FROM note WHERE title = ?',
    'title_fuzzy': 'SELECT * FROM note WHERE title LIKE ?',
    'body_fuzzy': 'SELECT * FROM note WHERE body LIKE ?',
    'insert': 'INSERT INTO note (uuid, title, body) VALUES (?, ?, ?)',
    'update': 'UPDATE note SET title = ?, body = ? WHERE uuid = ? AND title = ?',
    'delete': 'DELETE FROM note WHERE uuid = ? AND title = ?'
}

def query(option, *kwargs):
    headers = {
        'Authorization': 'Bearer ' + edit_token,
        'body-Type': 'application/json'
    }
    
    if option not in options:
        return False
    
    if option == 'user':
        requesting_user = lib.verify.validate()
        if not requesting_user:
            return False
        kwargs = (requesting_user['user_uuid'],)
    
    data = {
        'sql': options[option]
    }

    if '?' in options[option]:
        data['params'] = [*kwargs]
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()
    
    return [r['results'] for r in result['result']][0]
