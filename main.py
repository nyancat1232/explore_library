import sys

from importlib import import_module
import pprint

def find_module(module_name:str,hide_double_underscored:bool=False,max_depth:int=2,_current_depth=0):
    if _current_depth>max_depth:
        return None

    current_module = import_module(module_name)
    result={}
    for lib in dir(current_module):
        if lib.startswith('__') and hide_double_underscored:
            continue
            
        try:
            result[lib]=find_module(f'{module_name}.{lib}',hide_double_underscored=hide_double_underscored,_current_depth=_current_depth+1)
        except:
            result[lib]=getattr(current_module,lib)
    return result

r=find_module(sys.argv[1],max_depth=3,hide_double_underscored=False)
pprint.pprint(r)