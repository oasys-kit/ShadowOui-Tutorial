import numpy


data = numpy.loadtxt("tmp.traj",skiprows=15)
from matplotlib import pylab as plt

print(">>>shape: ",data.shape)

fig = plt.figure(1)

fig.add_subplot(221)
plt.plot(data[:,1],data[:,0])
plt.title("Electron trajectory")
plt.xlabel("Y [m]")
plt.ylabel("X [m]")

fig.add_subplot(222)
plt.plot(data[:,1],data[:,3])
plt.title("Electron velocity")
plt.xlabel("Y [m]")
plt.ylabel("betaX")

fig.add_subplot(223)
plt.plot(data[:,1],data[:,6])
plt.title("Electron curvature")
plt.xlabel("Y [m]")
plt.ylabel("curvature [m^-1]")

fig.add_subplot(224)
plt.plot(data[:,1],data[:,7])
plt.title("Magnetic Field")
plt.xlabel("Y [m]")
plt.ylabel("B [T]")




plt.show()

