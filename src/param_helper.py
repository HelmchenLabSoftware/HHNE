import json
from datetime import datetime  # Note: param files can contain datetime.time() command

# Read params from param file
def loadparams(filename):
    with open(filename) as f:
        params = json.loads(f.read())

        # Sample current time if it is requested
        if params['file']['session_start_time'] == '#now':
            params['file']['session_start_time'] = datetime.now()

    return params



# def loadparams(filename):
#     f = open(filename, 'r')
#
#     param_order = ['file', 'epoch']
#
#     def_params = {}
#
#     flines = f.readlines()
#     tmplines = ''
#     pname_idx = 0
#     for line in flines:
#         if line == '\n':
#             exec('def_params["' + param_order[pname_idx] + '"]={' + tmplines[:-1] + '}')
#             pname_idx += 1
#             tmplines = ''
#         elif line[0] != '#':
#             tmplines += line + ','
#     if tmplines != '':
#         exec('def_params["' + param_order[pname_idx] + '"]={' + tmplines[:-1] + '}')
#
#     print("Loaded default parameters from " + filename)
#     return def_params