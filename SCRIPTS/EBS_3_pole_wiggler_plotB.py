import numpy
from matplotlib import pylab as plt


data = numpy.loadtxt(in_object_1)
print(data.shape)
fig = plt.figure(1)
plt.plot(data[:,0],data[:,1])
plt.title("Magnetic Field")
plt.xlabel("Y [m]")
plt.ylabel("B [T]")
plt.show()