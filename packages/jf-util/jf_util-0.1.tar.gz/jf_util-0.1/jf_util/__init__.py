def pprint(a_dict):
    '''
        Pretty prints a deep python dictionary with indent levels
    '''
    pretty_str = pprint_helper(a_dict)
    print(pretty_str)

def pprint_helper(d, indent=0):
    str_out = ""
    for key in sorted(d):
        value = d[key]

        str_out += '\t' * indent + str(key) + ': '
        if isinstance(value, dict):
            str_out += '\n' + pprint_helper(value, indent+1)
        else:
            str_out += str(value) + '\n'
    return str_out

def get_methods_of_object(obj):
    '''
        Returns list of object's method names
    '''
    return [method_name for method_name in dir(obj) if callable(getattr(obj, method_name))]

import subprocess 

def ping(host):
    """
        Returns True if host (str) responds to a ping request.
    """
    command = ['ping', '-c', '1', host]
    return subprocess.call(command) == 0