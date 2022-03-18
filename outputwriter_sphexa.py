import sys
import numpy as np
import h5py
from parser_working import eat_snapshot
from numba import njit

src = sys.argv[1] #filepath to binary input file
header, gas, dm = eat_snapshot(src)
out = src + "_sphexa.h5"
gas.remove_columns(['id', 'rhom', 'rho', 'u', 'Bx', 'By', 'Bz'])
gas.add_column(0.0, name='u', index=7)
gas.add_column(1/len(gas), name='m', index=11)

print(gas)

gas['x'] = gas['x'] - 1
gas['y'] = gas['y'] - 1
gas['z'] = gas['z'] - 1
gas['hsml'] = gas['hsml'] / 3 

print(gas)

gas.write(out+".txt", format='ascii', overwrite=True)

h5f = h5py.File(out, 'w')
step0 = h5f.create_group("Step#0") 
#write data
step0.create_dataset('x', data=gas['x'])
step0.create_dataset('y', data=gas['y'])
step0.create_dataset('z', data=gas['z'])
step0.create_dataset('h', data=gas['hsml'])
step0.create_dataset('u', data=gas['u'])
step0.create_dataset('m', data=gas['m'])
#set attributes
step0.attrs["box"] = 	[0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
step0.attrs["minDt"] = 	[1.0e-4]
step0.attrs["pbc"] = 	[0, 0, 0]
step0.attrs["step"] = 	[0]
step0.attrs["time"] =	[0.0]
h5f.close()

