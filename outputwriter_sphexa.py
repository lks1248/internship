import sys
import numpy as np
from parser_working import eat_snapshot

src = sys.argv[1] #filepath to binary input file
header, gas, dm = eat_snapshot(src)
out = src + "_sphexa"
gas.remove_columns(['id', 'rhom', 'rho', 'u', 'Bx', 'By', 'Bz'])
gas.add_column(1.0, name='ro', index=6)
gas.add_column(0.0, name='u', index=7)
gas.add_column(0.0, name='p', index=8)
gas.add_column(0.0, name='m', index=11)

print(gas)

for i in range(len(gas)):
	gas['x'][i] = gas['x'][i] - 0.5
	gas['y'][i] = gas['y'][i] - 0.5
	gas['z'][i] = gas['z'][i] - 0.5
	gas['hsml'][i] = gas['hsml'][i] / 3 

print(gas)

gas.write(out+".txt", format='ascii', overwrite=True)
data = np.loadtxt(out+".txt", skiprows=1)
data2 = np.transpose(data)
data2.tofile(out)
