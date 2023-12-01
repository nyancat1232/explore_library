import sys

from importlib import import_module
import pprint

def find_module_information(module_name:str,
                max_depth:int=2,
                _current_depth=0):
    if _current_depth>max_depth:
        return None

    current_module = import_module(module_name)
    ret = {d:getattr(current_module,d) for d in dir(current_module)}

    return ret

def find_module(module_name:str,
                hide_double_underscored:bool=False,max_depth:int=2,
                _current_depth=0):
    if _current_depth>max_depth:
        return None

    current_module = import_module(module_name)
    try:
        current_all = getattr(current_module,'__all__')
    except:
        current_all = dir(current_module)
    #print(current_all)
    ret={}
    for module in current_all:

        try:
            
            ret[module] = find_module(module_name+'.'+module,hide_double_underscored,max_depth,_current_depth=_current_depth+1)

        except:
            pass
    if ret:
        return ret
    else:
        return current_all



r=find_module(sys.argv[1],max_depth=3)
pprint.pprint(r)
