import sys
import copy
import numpy as np


src = sys.argv[1]
npart = int(sys.argv[2])
n = int(sys.argv[3])
ncube = n ** 3
offset = 0.5/n

data = np.fromfile(src)
data = data.reshape(11, npart)

data[0] = data[0] / n - (0.5 - offset)
data[1] = data[1] / n - (0.5 - offset)
data[2] = data[2] / n - (0.5 - offset)
data[9] = data[9] / n
	
data2 = np.empty((11,npart * ncube))
print(data2.shape)
l = 0
for i in range(n):
	for j in range(n):
		for k in range(n):
			index = l * npart
			index2 = (l+1) * npart
			vec = np.array([i, j, k])
			vec = vec * offset * 2
			#print(vec)
			tmpdata = copy.deepcopy(data)
			tmpdata[0] = data[0] + vec[0]
			tmpdata[1] = data[1] + vec[1]
			tmpdata[2] = data[2] + vec[2]
			#print(tmpdata[2])
			data2[0:11, index:index2] = tmpdata
			#print(data2[0])
			l = l + 1

			

print("---------------------")
print(data2)
data2.tofile(src+"_"+str(ncube)+"x")

	
		