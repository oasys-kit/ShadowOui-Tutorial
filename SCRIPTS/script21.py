import numpy


def write_shadow_surface(s,xx,yy,outFile='presurface.dat'):
    """
      write_shadowSurface: writes a mesh in the SHADOW/presurface format
      SYNTAX: 
           out = write_shadowSurface(z,x,y,outFile=outFile)
      INPUTS:
           z - 2D array of heights
           x - 1D array of spatial coordinates along mirror width.
           y - 1D array of spatial coordinates along mirror length.
     
      OUTPUTS:
           out - 1=Success, 0=Failure
           outFile - output file in SHADOW format. If undefined, the
                     file is names "presurface.dat"
     
    """
    out = 1

    try:
       fs = open(outFile, 'w')
    except IOError:
       out = 0
       print ("Error: can\'t open file: "+outFile)
       return 
    else:
        # dimensions
        fs.write( repr(xx.size)+" "+repr(yy.size)+" \n" ) 
        # y array
        for i in range(yy.size): 
            fs.write(' ' + repr(yy[i]) )
        fs.write("\n")
        # for each x element, the x value and the corresponding z(y)
        # profile
        for i in range(xx.size): 
            tmps = ""
            for j in range(yy.size): 
                tmps = tmps + "  " + repr(s[j,i])
            fs.write(' ' + repr(xx[i]) + " " + tmps )
            fs.write("\n")
        fs.close()
        print ("write_shadow_surface: File for SHADOW "+outFile+" written to disk.")



# calculate a Gaussian bump
# create an array of 2 cm length
npoints = 51
length = 2.0

x = numpy.linspace(-0.5*length,0.5*length,npoints)
y = numpy.linspace(-0.5*length,0.5*length,npoints)

# create a surface with pixel value its distance to the center

x1 = numpy.outer(x,numpy.ones(y.size))
y1 = numpy.outer(numpy.ones(x.size),x)

r = numpy.sqrt( (x1)**2 + (y1)**2 )

# define bump FWHM
bump_fwhm = 0.5 # cm

#pizel sizes
pixel = length / (npoints-1)

# sigma value corresponding to FWHM
sigma = (bump_fwhm / pixel) / ( 2*numpy.sqrt(2*numpy.log(2)) )
print("sigma: ",sigma)

# evaluate the 2D Gaussian
z = numpy.exp(-((r/pixel)/2/sigma)**2)
# give a heigth of 1 microns
z = z * 1e-4

#write file for SHADOW
write_shadow_surface(z,x,y,outFile='bump.dat')


#
#plot
#
from matplotlib import pylab as plt
plt.figure(1)
plt4 = plt.imshow(z.T*1e4,extent=[-0.5*length,0.5*length,-0.5*length,0.5*length])
plt.title('Gaussian Bump')
plt.xlabel('H [cm]')
plt.ylabel('V [cm]')
cbar = plt.colorbar(plt4 , format="%.2f")
cbar.ax.set_ylabel('Deformation [um]')

plt.show()
