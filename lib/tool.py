
import sys
import inspect
import re
from types import ModuleType, FunctionType

admin_id = 'None'

ignore_methods = ['wraps', 'default', 'private']

sys_methods = {
    'private': 'module_docs',
    'docs': 'format_docs'
}

class Main(object):
    def __init__(self, module, request):
        self.module = module
        self.module.request = request

        if isinstance(module, ModuleType):
            self.methods = self.get_methods()
            self.decorators = self.module_decorators()
            self.docs = self.module_docs()

    def get_methods(self):

         # Get all the attributes of the module
        module_attrs = inspect.getmembers(self.module)

        # Filter the attributes to only include functions that were defined in the module
        module_functions = [attr for attr in module_attrs if callable(attr[1]) and attr[1].__module__ == self.module.__name__]

        # Extract only the function names from the filtered attributes
        function_names = [func[0] for func in module_functions]

        return function_names
    
    def format_docs(self):
        formatted = f'--- {self.module.__name__} ---\n'

        for key in self.docs:
            if key in ignore_methods or (key in self.decorators and 'private' in self.decorators[key]):
                continue
            
            docs = self.docs[key] or 'No description'
            docs = '\n  '.join(docs.split('\n'))

            formatted += f'# Method: {key}\n'
            formatted += f'# Description:\n'
            formatted += f'# Visit: https://api.robsweb.site/{self.module.__name__}/{key}\n'
            formatted += f"  {docs}\n\n"
    
        return {
            'raw': True,
            'data': formatted
        }
    
    def module_docs(self):
        docs = {}
        for key in self.methods:
            if key in ignore_methods or (key in self.decorators and 'private' in self.decorators[key]):
                continue
            func = getattr(self.module, key)
            docs[key] = inspect.getdoc(func)

        return docs
    
    def module_decorators(self):
        docs = {}
        for key in self.methods:
            if key in ignore_methods:
                continue
            func = getattr(self.module, key)
            
            try:
                source = inspect.getsource(func)
                decorators = re.findall(r'@(\w+)', source)
                docs[key] = decorators
            except:
                continue

        return docs
    
    def get_method_data(self, func):
        
        method = inspect.signature(func)
        method_data = method.parameters
        method_params = list(method_data.keys())
        required_params = list(filter(lambda x: method_data[x].default == inspect._empty, method_params))    

        return method, method_data, method_params, required_params

    def main(self, subpaths, args):

        if not isinstance(self.module, ModuleType):
            return {False: 'Invalid module.'}
        
        args = dict(args)
        for key in subpaths:
            
            # handle internally created methods like docs
            if key in sys_methods:
                return getattr(self, sys_methods[key])()
            
            # if a provided url parameter matches a method name
            if key in self.methods:
                
                # @private methods should not be called from outside the module
                if 'private' in self.decorators[key]:
                    continue

                # check the args of the function
                # if it has args, pass them if the request has them
                func = getattr(self.module, key)

                method, method_data, method_params, required_params = self.get_method_data(func)

                if len(method_params) == 0:
                    return getattr(self.module, key)()
                
                elif len(args) == 0 and len(required_params) > 0:
                    return {'error': 'No args provided.'}
                else: #if len(list(filter(lambda x: x in list(method_params), list(args)))) > 0:
                    
                    # strip any args that are not in the method params
                    for arg in list(args):
                        if arg not in method_params:
                            args.pop(arg)
                    
                    # first check if the key method requires admin access
                    if 'restricted' in method_params:
                        if 'key' not in args:
                            return {'error': 'Missing API key'}
                        elif args['key'] != admin_id:
                            return {'error': 'Invalid API key provided.'}

                    # get the type of each arg
                    #  convert the arg value if the param is: int, float, bool, list, dict
                    for param in method_params:
                        required = method_data[param].default == inspect.Parameter.empty
                        
                        if param not in args:
                            if required:
                                return {'error': 'Missing required arg: ' + param}
                            else:
                                continue

                        dtype = method_data[param].annotation
                        try:
                            if dtype == int:
                                args[param] = int(args[param])
                            elif dtype == float:
                                args[param] = float(args[param])
                            elif dtype == bool:
                                args[param] = bool(args[param])
                            elif dtype == list:
                                args[param] = list(args[param])
                            elif dtype == dict:
                                args[param] = dict(args[param])
                        except Exception as e:
                            print(e)
                            return {'error': str(e)}                             

                    return getattr(self.module, key)(**args)
        
        try:
            # Check if this module has a default function and check if it takes args
            func = getattr(self.module, 'default')

            _, _, method_params, required_params = self.get_method_data(func)
            
            if len(method_params) == 0:
                return getattr(self.module, 'default')()
            else:
                return getattr(self.module, 'default')(args)


        except Exception as e:
            print(e)
            return {
                'error': str(e)
            }