
from websocket import create_connection
from lib.verify import verify_token
from lib.private import private
import json

@verify_token
def ws_test():
    
    data = {'test': ''}
    data_json = json.dumps(data)    
    ws = create_connection("wss://ws.rau-6fb.workers.dev")
    ws.send(data_json)
    result =  ws.recv()
    ws.close()
    
    return result

def default():
    result = ws_test()
    return result