import sys

from importlib import import_module

import json

def find_module_information(module_name:str,
                max_depth:int=2,
                _current_depth=0):
    if _current_depth>max_depth:
        return None

    current_module = import_module(module_name)
    ret = {d:getattr(current_module,d) for d in dir(current_module)}

    return ret

def find_module(module_name:str,hide_single_underscored:bool=True,
                hide_double_underscored:bool=True,max_depth:int=10,
                _current_depth=0):
    
    def _filter_underscore(current_all,single,double):
        if double:
            current_all = [a for a in current_all if not a.startswith('_')]
        if single:
            current_all = [a for a in current_all if not a.startswith('__')]
        return current_all

    if _current_depth>max_depth:
        return None

    current_module = import_module(module_name)
    try:
        current_all = getattr(current_module,'__all__')
    except:
        current_all = dir(current_module)
    
    current_all=_filter_underscore(current_all,hide_single_underscored,hide_double_underscored)

    #print(current_all)
    ret={}
    for module in current_all:

        try:
            
            ret[module] = find_module(module_name+'.'+module,hide_double_underscored,max_depth,_current_depth=_current_depth+1)

        except:
            pass
    if ret:
        ret['_c__v___dir___v__c_']=_filter_underscore(dir(current_module),hide_single_underscored,hide_double_underscored)

        return ret
    else:
        return current_all



r=find_module(sys.argv[1])
with open(f'{sys.argv[1]}.json','w') as json_file:
    json.dump(r,json_file)