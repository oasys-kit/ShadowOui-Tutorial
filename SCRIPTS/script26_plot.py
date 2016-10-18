from matplotlib import pylab as plt

(x,y,yEA) = in_object
print(in_object)

plt.plot(x,y/y.max(),label="Fully coherent")
plt.plot(x,yEA/yEA.max(),label="Partial coherent")
plt.xlabel("Z [um]")
plt.ylabel("Intensity [Arbitrary Units]")
plt.legend()

plt.show()