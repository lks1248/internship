import sys
import h5py
import numpy as np
import math

src1 = sys.argv[1] #low-density glass block
src2 = sys.argv[2] #high-density glass block
ld = h5py.File(src1, 'r')
hd = h5py.File(src2, 'r')
npart1 = len(ld["Step#0/x"])
npart2 = len(hd["Step#0/x"])
npartout = 128*(npart1 + npart2)
offset = 1/16
mpart = 0.01625/npartout
#using p=(gamma-1)*rho*u with gamma = 5/3 and p = 2.5, u = 2.5/((5/3-1)*rho)
hd_u = 2.5/((5/3-1)*(npart2/npart1))
ld_u = 2.5/((5/3-1)*1)
print(hd_u, ld_u)
omega_0 = 0.01

print("Creating Kelvin-Helmholtz ICs with a density ratio of", npart2/npart1)
print("Total number of particles:", npartout)

ld_x = (ld["Step#0/x"][:] + 0.5) / 16
ld_y = (ld["Step#0/y"][:] + 0.5) / 16
ld_z = (ld["Step#0/z"][:] + 0.5) / 16
ld_h = (ld["Step#0/h"][:]) / 16 * 0.9 #0.5*(3*mpart*100/4/math.pi/1)**(1/3)#

hd_x = (hd["Step#0/x"][:] + 0.5) / 16
hd_y = (hd["Step#0/y"][:] + 0.5) / 16
hd_z = (hd["Step#0/z"][:] + 0.5) / 16
hd_h = (hd["Step#0/h"][:]) / 16 * 0.75 #0.5*(3*mpart*100/4/math.pi/2)**(1/3)#

out_x = np.empty(npartout)
out_y = np.empty(npartout)
out_z = np.empty(npartout)
out_vx = np.empty(npartout)
out_vy = np.empty(npartout)
out_vz = np.full(npartout, 0.0)
out_h = np.empty(npartout)
out_m = np.full(npartout, mpart)
out_u = np.empty(npartout)

#filling particles 
index = 0
for i in range(16):
	for j in range(16):
		#print(index)
		if( i > 3 and i < 12):
			out_x[index:(index + npart2)] = hd_x + (offset * j)
			out_y[index:(index + npart2)] = hd_y + (offset * i)
			out_z[index:(index + npart2)] = hd_z
			out_vx[index:(index + npart2)] = 0.5
			out_h[index:(index + npart2)] = hd_h
			out_u[index:(index + npart2)] = hd_u
			index += npart2
		else:
			out_x[index:(index + npart1)] = ld_x + (offset * j)
			out_y[index:(index + npart1)] = ld_y + (offset * i)
			out_z[index:(index + npart1)] = ld_z
			out_vx[index:(index + npart1)] = -0.5
			out_h[index:(index + npart1)] = ld_h
			out_u[index:(index + npart1)] = ld_u
			index += npart1

for i in range(npartout):
	out_vy[i] = omega_0 * math.sin(4 * math.pi * out_x[i])

print(out_u)
output = h5py.File("IC_kelvin-helmholtz.h5", 'w')
step0 = output.create_group("Step#0")
step0.create_dataset('x', data=out_x)
step0.create_dataset('y', data=out_y)
step0.create_dataset('z', data=out_z)
step0.create_dataset('vx', data=out_vx)
step0.create_dataset('vy', data=out_vy)
step0.create_dataset('vz', data=out_vz)
step0.create_dataset('h', data=out_h)
step0.create_dataset('u', data=out_u)
step0.create_dataset('m', data=out_m)
step0.attrs["gravConstant"] = [-1.0]
step0.attrs["box"] = 	[0.0, 1.0, 0.0, 1.0, 0.0, 0.0625]
step0.attrs["minDt"] = 	[1.0e-4]
step0.attrs.create('pbc',[1, 1, 1], dtype=np.intc)
step0.attrs["step"] = 	[0]
step0.attrs["time"] =	[0.0]
output.attrs["KelvinHelmholtzGrowthRate"] = [1]
output.close()
