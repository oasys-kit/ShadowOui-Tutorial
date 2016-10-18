from matplotlib import pylab as plt
import Shadow

#beam = Shadow.Beam()
#beam.load("begin.dat")
beam = in_object_1._beam

h23 = beam.histo1(6,ref=23)
h24 = beam.histo1(6,ref=24)
h25 = beam.histo1(6,ref=25)
h33 = beam.histo1(6,ref=33)
#
plt.plot(h23["bin_path"],h23["histogram_path"], label="Total intensity")
plt.plot(h24["bin_path"],h24["histogram_path"], label="$\sigma$ intensity")
plt.plot(h25["bin_path"],h25["histogram_path"], label="$\pi$ intensity")
plt.plot(h33["bin_path"],h33["histogram_path"], label="Circular polarizatiion S3")
plt.legend(loc=3)
plt.xlabel("Z' [urad]")
plt.ylabel("Weigted Intensity [arbitrary units]")
#
plt.show()
