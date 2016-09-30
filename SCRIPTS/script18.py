#
#
# Shadow3 python script to scan a variable
#
#
# It uses the currently defined Shadow system (files start.00...start.03)
#
# It scans a list of variables, e.g., the distances T_SOURCE and T_IMAGE of 
# the first and second o.e., respectively. 
# It also sets the o.e.2 radius accordingly.
#
# Output: a file ex18b.spec
#
#
# Author: Manuel Sanchew del Rio
#         ESRF (c) 2013-2015
#
# Modifications: 
#         srio@esrf.eu 20140108 Adapted for python3
#

#
# import block
#

import numpy 
import Shadow 
import copy

do_intermediate_plots = 0
horizontal_divergence_in_mrad = 5.0

#
# initialize shadow3 source (oe0) and beam
#
beam = Shadow.Beam()
oe0 = Shadow.Source()
oe1 = Shadow.OE()
oe2 = Shadow.OE()

oe0.BENER = 6.03999996
oe0.EPSI_X = 3.89999997e-07
oe0.EPSI_Z = 3.89999988e-09
oe0.FDISTR = 4
oe0.FSOURCE_DEPTH = 4
oe0.F_COLOR = 3
oe0.F_PHOT = 0
oe0.HDIV1 = 0.05*1e-3*horizontal_divergence_in_mrad
oe0.HDIV2 = 0.05*1e-3*horizontal_divergence_in_mrad
oe0.ISTAR1 = 567656675
oe0.NCOL = 0
oe0.NPOINT = 25000
oe0.N_COLOR = 0
oe0.PH1 = 19970.0
oe0.PH2 = 20030.0
oe0.POL_DEG = 0.0
oe0.R_ALADDIN = 2517.72003
oe0.R_MAGNET = 25.1772003
oe0.SIGDIX = 0.0
oe0.SIGDIZ = 0.0
oe0.SIGMAX = 0.0395000018
oe0.SIGMAY = 0.0
oe0.SIGMAZ = 0.00368999992
oe0.VDIV1 = 1.0
oe0.VDIV2 = 1.0
oe0.WXSOU = 0.0
oe0.WYSOU = 0.0
oe0.WZSOU = 0.0

oe1.FILE_REFL = b'si5_55.111'
oe1.F_CENTRAL = 1
oe1.F_CRYSTAL = 1
oe1.PHOT_CENT = 20000.0
oe1.R_LAMBDA = 5000.0
oe1.T_IMAGE = 0.0
oe1.T_INCIDENCE = 45.0
oe1.T_REFLECTION = 45.0
oe1.T_SOURCE = 3000.0

oe2.ALPHA = 180.0
oe2.CIL_ANG = 90.0
oe2.FCYL = 1
oe2.FILE_REFL = b'si5_55.111'
oe2.FMIRR = 1
oe2.F_CENTRAL = 1
oe2.F_CRYSTAL = 1
oe2.F_EXT = 1
oe2.PHOT_CENT = 20000.0
oe2.RMIRR = 148.298614
oe2.R_LAMBDA = 5000.0
oe2.T_IMAGE = 1000.0
oe2.T_INCIDENCE = 45.0
oe2.T_REFLECTION = 45.0
oe2.T_SOURCE = 0.0


#
# >>>>>>>>>>>  inputs <<<<<<<<<<<<<
#

#
# flags
#
write  = 0         # 0=No     1=Yes (write shadow binary files)

#
# scanning magnification M: 
#
npts = 51
scan = numpy.linspace(0.1,1.0,npts) # from, to, npoints   

#
# >>>>>>>>>>>  calculations <<<<<<<<<<<<<
#

#
# define array to store results
#
nout = 8                                # number of variables to store
out  = numpy.zeros( (nout,scan.size) )  # creates the array to store results


#
# open output file
#
f = open('ex18b.spec', 'wb')
header="#F ex18b.py\n"
f.write( header.encode('utf-8') )


#
# run source with horizontal divergence: HDIV1+HDIV2duplicate
#
oe0.HDIV1 = 5e-3/2
oe0.HDIV2 = 5e-3/2
beam.genSource(oe0)

if write:
    beam.write("begin.dat")

#
# start loop on scanned variable
#
for i in range(scan.size):
    print("\n>>>>>>>>>> tracing item %d of %d. \n"%(i+1,scan.size))
    oe1i = oe1.duplicate()
    oe2i = oe2.duplicate()

    pp = 3000.0 
    qq = pp*scan[i]
    theta = (90.0e0 - 84.32614)*numpy.pi/180e0
    rsag=2.0e0*numpy.sin(theta)/(1.0e0/pp+1.0e0/qq)
    oe1i.T_SOURCE = pp
    oe2i.T_IMAGE = qq
    oe2i.RMIRR = rsag

    if write:
        oe1i.FWRITE=0 # write(0) or not(3) binary files
        oe2i.FWRITE=0 # write(0) or not(3) binary files
        oe1i.write("start.01")
        oe2i.write("start.02")
    else:
        oe1i.FWRITE=3 # write(0) or not(3) binary files
        oe2i.FWRITE=3 # write(0) or not(3) binary files


    beami = None
    beami = beam.duplicate()

    # run trace
    beami.traceOE(oe1i,1)
    beami.traceOE(oe2i,2)

    if write:
        oe1i.write("end.01")
        oe2i.write("end.02")

    # score results
    g1 = beami.histo2(1,3,nolost=1,nbins=100)
    g2 = beami.histo1(11,nolost=1,nbins=31,ref=23)

    #plots
    if do_intermediate_plots:
        Shadow.ShadowTools.plotxy(beami,1,3,nolost=1,nbins=100)


    # store scored results
    out[0,i] = scan[i]
    out[1,i] = pp
    out[2,i] = qq
    out[3,i] = rsag
    #if g1 != None:
    #    fw1 = numpy.array([g1.fwhmx,g1.fwhmy])
    out[4,i] = g1['fwhm_h']*1e4  # in um
    out[5,i] = g1['fwhm_v']*1e4
#
#    if g2 != None:
    out[6,i] = g2['fwhm']
    out[7,i] = beami.intensity(nolost=1)

labels="#L  Magnification  p [cm]  q [cm]  Rsag [cm]  "+ \
    "fwhm_h [um]  fwhm_v [um]  DE [eV]  Intensity [a.u.]"
#
# >>>>>>>>>>>> outputs <<<<<<<<<<<<<<<<
#

#write spec formatted file

tmp = range(out.shape[0])
tmp =  (str( tmp  ).strip('[]')).split()

header="\n#S 1 Magnification\n#N "+ \
    str(out.shape[0])+"\n"+labels+"\n"
f.write(header.encode('utf-8') )

for i in range(out.shape[1]):
   tmps = ("%20.11e "*out.shape[0]+"\n") % tuple( out[:,i].tolist())
   f.write( tmps.encode('utf-8') )
   print( ("%20.11e "*out.shape[0]+"\n") % tuple( out[:,i].tolist())  )

f.close()
print ("File written to disk: ex18b.spec")


#
#plot results with matplotlib
#
from matplotlib import pylab as plt
plt.plot(out[0,:],out[7,:])
plt.xlabel('Magnification factor')
plt.ylabel('Intensity')
plt.show()
