import scipy.io as sio

mat_contents = sio.loadmat('../examples/test.mat')
header_keys = ['__globals__', '__version__', '__header__']
mat_header = {k : v for k, v in mat_contents.items() if k in header_keys}
mat_data = {k : v for k, v in mat_contents.items() if k not in header_keys}

print(mat_header)
print(mat_data)