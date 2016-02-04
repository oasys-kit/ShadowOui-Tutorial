import Shadow
#for plot
from matplotlib import pylab as plt
import numpy

ymin = -100.0
ymax = 100.0
ypoints = 101

beam = in_object._beam

tkt = Shadow.ShadowTools.ray_prop(beam,nolost=1,ymin=ymin,ymax=ymax,ypoints=ypoints,xbins=61,zbins=61)

# ray_prop results
f1 = plt.figure(1)
plt.plot(tkt["y"],2.35*tkt["x_sd"],label="x (tangential)")
plt.plot(tkt["y"],2.35*tkt["x_wsd"],label="x weighted (tangential)")
plt.plot(tkt["y"],2.35*tkt["z_sd"],label="z (sagittal)")
plt.plot(tkt["y"],2.35*tkt["z_wsd"],label="z weighted (sagittal)")
plt.legend()
plt.title("ray_prop")
plt.xlabel("Y [cm]")
plt.ylabel("2.35*SD [cm]")

# data from ray_prop histograms

f2 = plt.figure(2)
if tkt["x_fwhm"] is None:
    pass
else:
    plt.plot(tkt["y"],tkt["x_fwhm"],label="x (histo)")
    plt.plot(tkt["y"],tkt["x_wfwhm"],label="x (weighted histo)")
if tkt["z_fwhm"] is None:
    pass
else:
    plt.plot(tkt["y"],tkt["z_fwhm"],label="z (histo)")
    plt.plot(tkt["y"],tkt["z_wfwhm"],label="z (weighted histo)")
plt.legend()
plt.title("ray_prop (from histograms)")
plt.xlabel("Y [cm]")
plt.ylabel("FWHM [cm]")

plt.show()