from lib.verify import *
import lib.data
import lib.d1

rauuid = '787c1b16-97f0-578d-b93a-1a620be4016f'
test_notes = lib.data.file('admin_notes.json')

def notes(uuid):
    # user_notes = [note for note in test_notes.get(uuid, [])]
    user_notes = lib.d1.query('user', uuid)
    return user_notes

def add():
    validated = validate()
    if not validated:
        return {'template': 'login.html'}

    uuid = validated.get('user_uuid')
    # user_notes = notes(uuid)
    # note = {"id": len(user_notes), "title": request.args.get('title'), "content": request.args.get('content')}
    # test_notes[uuid].append(note)
    
    # lib.data.upsert('admin_notes.json', test_notes)
    
    note = lib.d1.query('insert', uuid, request.args.get('title'), request.args.get('content'))
    
    return note

def home():
    validated = validate()
    if not validated:
       return {'template': 'login.html'}

    if request.method == 'POST':
        return {'redirect': 'https://rau.dev/dev'}
    else:
        uuid = validated.get('user_uuid')
        return {'template': 'dev.html', 'args': {'notes': notes(uuid)}}

def test():
    # return lib.d1.query('all')
    # return lib.d1.query('insert', rauuid, 'd1-raudev-test', 'Testing upload over API')
    return lib.d1.query('user', rauuid)

def all_():
    return lib.d1.query('all')

def default():
    isvalid = validate()
    if isvalid:
        uuid = isvalid.get('user_uuid')
        if uuid == rauuid:
            return 'Welcome, admin'
        return 'Welcome, ' + str((isvalid.get('name') or isvalid.get('email')))
    return 'Not logged in'