import Shadow
#for plot
from matplotlib import pylab as plt
import numpy


beam = in_object._beam

tkt2 = Shadow.ShadowTools.focnew(beam,nolost=1,mode=1)
print(tkt2["text"])


# now the focnew scans
f1 = plt.figure(1)
ymin = -100.0
ymax = 100.0
npoints = 101
y = numpy.linspace(ymin,ymax,npoints)
plt.plot(y,2.35*Shadow.ShadowTools.focnew_scan(tkt2["AX"],y),label="x (tangential)")
plt.plot(y,2.35*Shadow.ShadowTools.focnew_scan(tkt2["AZ"],y),label="z (sagittal)")
plt.plot(y,2.35*Shadow.ShadowTools.focnew_scan(tkt2["AT"],y),label="combined x,z")
plt.legend()
plt.title("focnew")
plt.xlabel("Y [cm]")
plt.ylabel("2.35*<coor> [cm]")
plt.show()