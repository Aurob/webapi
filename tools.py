import time
import sys
import os
import importlib
import inspect

from lib import tool as _tool

start = time.time()
TOOLBOX = 'toolbox'

sys_modules = {
    'describe': 'list_modules'
}
    
sys_methods = {
    'private': 'module_docs',
    'docs': 'module_docs',
    '__debug__': 'format_docs'
}

ignore_files = ['__init__.py']
def running_time():
    return int(time.time() - start)

def format_time(t):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))

def system_time():
    return int(time.time())

def echo(message):
    return message  

def validate_tool(tool):
    if tool.endswith('.py'):
        if tool not in ignore_files:
            return True
    return False

def get_tools():
    return [t.split('.')[0] for t in os.listdir(TOOLBOX) if validate_tool(t)]

def is_tool(tool):
    valid_tool = tool in get_tools()
    
    if valid_tool:
        if tool not in sys.modules:
            import_tool(tool)
    
    return valid_tool

def import_tool(tool):

    if tool not in sys.modules:
        module = importlib.import_module(f'{TOOLBOX}.' + tool)
        sys.modules[tool] = module

def api(path, args, request):

    subpaths = path.split('/')
    path = subpaths[0]
    subpaths = subpaths[1:]
    res = {}
    
    print(path)
    if is_tool(path):

        main = _tool.Main(sys.modules[path], request)
        res['result'] = main.main(subpaths, args)

    elif path in sys_modules:
        if path == 'describe':
            output = []
            for tool in get_tools():
                doc_url = f'https://api.robsweb.site/{tool}/docs'
                output.append(f'{doc_url}')
            res['result'] = output
    else:
        res['result'] = False
        
    return res