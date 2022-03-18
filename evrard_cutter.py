import sys 
from copy import copy
import numpy as np
import h5py 
from numba import jit 

src = sys.argv[1]
out = src[:-3]
nneighbours = 100
h5f = h5py.File(src, 'r')
x = h5f["Step#0/x"][:]
y = h5f["Step#0/y"][:]
z = h5f["Step#0/z"][:]
npart = len(h5f["Step#0/x"])
mpart = 1/npart

#cut sphere out of the block
def cut(h5f):
	a = np.empty((6, 0))
	print(a)
	for i in range(npart):
		
		radius = (x[i]**2 + y[i]**2 + z[i]**2) ** 0.5
		
		#print(radius)
		if radius <= 1:
			h = ((2*radius*mpart*nneighbours)/((4/3)*8))**(1/3)
			#print(data[:,i])
			b = np.empty(([6,1]))
			b[0] = x[i] * radius**(1/2)
			b[1] = y[i] * radius**(1/2)
			b[2] = z[i] * radius**(1/2)
			b[3] = 5.000000000000000278e-2
			if h < 0.02:
				b[4] = 0.02 #constant value for now, should be a function of npart and box size
			else: 
				b[4] = h

			b[5] = 0.0

			a = np.c_[a, b]
	return a
		
a = cut(h5f)
a[5,:] = 1/a.shape[1]
print(a)

h5f = h5py.File(out+"_evrard.h5", 'w')
step0 = h5f.create_group("Step#0") 
#write data
step0.create_dataset('x', data=a[0])
step0.create_dataset('y', data=a[1])
step0.create_dataset('z', data=a[2])
step0.create_dataset('h', data=a[4])
step0.create_dataset('u', data=a[3])
step0.create_dataset('m', data=a[5])
#set attributes
step0.attrs["gravConstant"] = [-1.0]
step0.attrs["box"] = 	[0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
step0.attrs["minDt"] = 	[1.0e-4]
step0.attrs["pbc"] = 	[0, 0, 0]
step0.attrs["step"] = 	[0]
step0.attrs["time"] =	[0.0]
#a.tofile(src+"_evrard")
h5f.close()
b = a.transpose()
np.savetxt(src+"_evrard.txt", b)