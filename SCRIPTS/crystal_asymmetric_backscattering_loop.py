#
#
# Shadow3 python script to ...
#
#
#

#
# import block
#

import numpy 
import Shadow as sh
import Shadow.ShadowTools as st


#
# initialize Shadow containers and load existing system
#

oe0 = sh.Source()
oe1= sh.OE()
oe2= sh.OE()
oe3= sh.OE()



#
# >>>>>>>>>>>  inputs <<<<<<<<<<<<<
#

#
#flags
#
write  = 0    # 0=No     1=Yes (write shadow binary and start.xx end.xx  files)

#
#scanning: 
#
npts = 10
scan_urad = numpy.linspace(-500.0,0.0,npts) # from, to, npoints
scan_deg = scan_urad * 1e-6 * 180.0 / numpy.pi

#
# >>>>>>>>>>>  calculations <<<<<<<<<<<<<
#


out   = numpy.zeros( (2,scan_deg.size) ) 

for i in range(npts):
    beam = None
    beam = sh.Beam()

    oe0.FDISTR = 1
    oe0.FSOUR = 0
    oe0.FSOURCE_DEPTH = 0
    oe0.F_COLOR = 3
    oe0.F_PHOT = 0
    oe0.HDIV1 = 5e-08
    oe0.HDIV2 = 5e-08
    oe0.ISTAR1 = 67754319
    oe0.NPOINT = 250000
    oe0.PH1 = 9130.0
    oe0.PH2 = 9135.0
    oe0.VDIV1 = 7.5e-06
    oe0.VDIV2 = 7.5e-06

    
    oe1.A_BRAGG = -19.0
    oe1.DUMMY = 1.0
    oe1.FILE_REFL = b'/users/srio/Oasys/OasysRun/Si5_15.220'
    oe1.F_BRAGG_A = 1
    oe1.F_CENTRAL = 1
    oe1.F_CRYSTAL = 1
    oe1.PHOT_CENT = 9132.15
    oe1.R_LAMBDA = 5000.0
    oe1.THICKNESS = 5.0
    oe1.T_IMAGE = 500.0
    oe1.T_INCIDENCE = 88.282
    oe1.T_REFLECTION = 50.293
    oe1.T_SOURCE = 500.0
    
    oe2.A_BRAGG = -88.5
    oe2.DUMMY = 1.0
    oe2.FILE_REFL = b'/users/srio/Oasys/OasysRun/Si5_15.008'
    oe2.F_BRAGG_A = 1
    oe2.F_CRYSTAL = 1
    oe2.T_IMAGE = 0.0
    oe2.T_SOURCE = 0.0
    # these are the scanned variables....
    #oe2.T_INCIDENCE = 88.5
    #oe2.T_REFLECTION = -88.5
    oe2.T_INCIDENCE  =  88.5 + scan_deg[i]
    oe2.T_REFLECTION = -oe2.T_INCIDENCE

    
    oe3.ALPHA = 180.0
    oe3.A_BRAGG = 19.0
    oe3.DUMMY = 1.0
    oe3.FILE_REFL = b'/users/srio/Oasys/OasysRun/Si5_15.220'
    oe3.F_BRAGG_A = 1
    oe3.F_CENTRAL = 1
    oe3.F_CRYSTAL = 1
    oe3.PHOT_CENT = 9132.15
    oe3.R_LAMBDA = 5000.0
    oe3.THICKNESS = 5.0
    oe3.T_IMAGE = 500.0
    oe3.T_INCIDENCE = 50.295
    oe3.T_REFLECTION = 88.284
    oe3.T_SOURCE = 500.0
    

    #
    # get Shadow source 
    #
    if write:
        e0.write("start.00")
        e1.write("start.01")
        e2.write("start.02")
        e3.write("start.03")

    # run source
    beam.genSource(oe0)

    if write:
        e0.write("end.00")
        beam.write("begin.dat")
    
    if write:
        oe1.FWRITE=0 # write(0) or not(3) binary files
        oe2.FWRITE=0 # write(0) or not(3) binary files
        oe3.FWRITE=0 # write(0) or not(3) binary files
    else:
        oe1.FWRITE=3 # write(0) or not(3) binary files
        oe2.FWRITE=3 # write(0) or not(3) binary files
        oe3.FWRITE=3 # write(0) or not(3) binary files

    print("==================================Tracing index %d of %d"%(i,npts-1))
    print("===========================Tracing oe 1...")
    beam.traceOE(oe1,1)
    print("===========================Tracing oe 2...")
    beam.traceOE(oe2,2)
    print("===========================Tracing oe 3...")
    beam.traceOE(oe3,3)

    if write:
        e1.write("end.01")
        e2.write("end.02")
        e3.write("end.03")

    #analysis: get intensity from an histogram
    intensity = beam.intensity(nolost=1)

    print ("------------------------------------")
    print ("index: %d" % i)
    print ("intensity: %f" % intensity)
    print ("------------------------------------")
    # store results
    out[0,i] = scan_urad[i]
    out[1,i] = intensity

#
# >>>>>>>>>>>> outputs <<<<<<<<<<<<<<<<
#

#
# open output file: write spec formatted file
#
file_out = 'crystal_asymmetric_backscattering.spec'
f = open(file_out, 'w')
header="#F %s\n"%file_out
f.write(header)

header="\n#S 1 Fig4 in Shvydko paper\n"
f.write(header)
f.write("#N 2\n")
labels="#L  Theta_urad  Intensity_au\n"
f.write(labels)

for i in range(out.shape[1]):
   f.write( ("%20.11e "*out.shape[0]+"\n") % tuple( out[:,i].tolist())  )
   print( ("%20.11e "*out.shape[0]+"\n") % tuple( out[:,i].tolist())  )
    
f.close()
print ("File written to disk: %s"%file_out)
print ("All done.")


#
# plot
#

from matplotlib import pylab as plt

fig = plt.figure(1)
plt.plot(out[0,:],out[1,:])
plt.title("Scanned intensity")
plt.xlabel("Angle [urad]")
plt.ylabel("Intensity [a.u.]")
plt.show()
