import sys 
from math import pi
import numpy as np
from numba import jit 

src = sys.argv[1]
npart = int(sys.argv[2])
mpart = 1/npart
nneighbours = 100

data = np.fromfile(src)
data = data.reshape(11, npart)
print(data)

#cut sphere out of the block
def cut(data):
	a = np.empty((11, 0))
	print(a)
	for i in range(npart):
		radius = (data[0,i]**2 + data[1,i]**2 + data[2,i]**2) ** 0.5
		
		#print(radius)
		if radius <= 1:
			h = ((2*pi*radius*mpart*nneighbours)/((4/3)*pi*8))**(1/3)
			#print(data[:,i])
			b = np.empty(([11,1]))
			b[0] = data[0,i] * radius**(3/2)
			b[1] = data[1,i] * radius**(3/2)
			b[2] = data[2,i] * radius**(3/2)
			b[3] = 0.0
			b[4] = 0.0
			b[5] = 0.0
			b[6] = 1.0
			b[7] = 5.000000000000000278e-2
			b[8] = data[8,i]
			b[9] = h
			#print(b[9])
			b[10] = 1.52285e-5
			#print(b)
			#print("------------")
			#b = b.reshape(11,1)
			#print(a.shape)
			#print(b.shape)
			a = np.c_[a, b]
	return a
		
a = cut(data)
print(a)
print(a.shape)
a.tofile(src+"_evrard")
b = a.transpose()
np.savetxt(src+"_evrard.txt", b)