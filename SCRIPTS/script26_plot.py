from matplotlib import pylab as plt

(x,y,yEA) = in_object
print(in_object)

plt.plot(x,y/y.max())
plt.plot(x,yEA/yEA.max())
plt.xlabel("Z [um]")
plt.ylabel("Intensity Ensemple Average")

plt.show()