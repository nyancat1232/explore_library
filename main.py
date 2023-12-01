#input
import sklearn

#source
import pprint
def find_module(module,hide_double_underscored=False,_current_depth=0):
    if _current_depth>2:
        return None
    result={}
    for lib in dir(module):
        if lib.startswith('__') and hide_double_underscored:
            continue
        
        result[lib]=find_module(module,hide_double_underscored=hide_double_underscored,_current_depth=_current_depth+1)
    return result

r=find_module(sklearn,hide_double_underscored=True)
pprint.pprint(r)