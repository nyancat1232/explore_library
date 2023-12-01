from importlib import import_module
from types import ModuleType
import argparse
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
    
    def _filter_underscore(current_all,hide_single,hide_double):
        if hide_double:
            current_all = [a for a in current_all if not a.startswith('__')]
        if hide_single:
            current_all = [a for a in current_all if not a.startswith('_')]
        return current_all
    if _current_depth>max_depth:
        return None

    current_module = import_module(module_name)
    
    ret={}


    #in __all__
    try:
        current_all = getattr(current_module,'__all__')
    except:
        current_all = dir(current_module)

    current_all=_filter_underscore(current_all,hide_single=hide_single_underscored,hide_double=hide_double_underscored)

    ret={}
    for module in current_all:
        try:
            ret[module] = find_module(module_name+'.'+module,
                                      hide_single_underscored=hide_single_underscored,
                                      hide_double_underscored=hide_double_underscored,
                                      max_depth=max_depth,
                                      _current_depth=_current_depth+1)
        except:
            pass
    
    #sibling modules
    modules_in_dir=[elem for elem in dir(current_module) if type(getattr(current_module,elem)) == ModuleType]
    modules_in_dir=_filter_underscore(modules_in_dir,hide_single=hide_single_underscored,hide_double=hide_double_underscored)
    for module in modules_in_dir:
        try:
            ret[module] = find_module(module_name+'.'+module,
                                      hide_single_underscored=hide_single_underscored,
                                      hide_double_underscored=hide_double_underscored,
                                      max_depth=max_depth,
                                      _current_depth=_current_depth+1)
        except:
            pass
    #print(modules_in_dir)

    
    #sibling values
    ret['_c__v___dir___v__c_']=_filter_underscore(dir(current_module),hide_single=hide_single_underscored,hide_double=hide_double_underscored)
    ret['_c__v___dir___v__c_']=[v for v in ret['_c__v___dir___v__c_'] if v not in ret]

    return ret


parser = argparse.ArgumentParser()
parser.add_argument('module',help='a python module for inspecting',type=str)
parser.add_argument('-nhs',help='not hide single underscore(_)',action="store_false" )
parser.add_argument('-nhd',help='not hide double underscore(__)',action="store_false" )
args = parser.parse_args()
print(args.nhd)
r=find_module(args.module,hide_double_underscored=args.nhd,hide_single_underscored=args.nhs)
with open(f'{args.module}.json','w') as json_file:
    json.dump(r,json_file)