import numpy as np
from scipy import interpolate


def write_shadowSurface(s,xx,yy,outFile='presurface.dat'):
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
        # for each x element, the x value and the corresponding z(y) profile
        for i in range(xx.size): 
            tmps = ""
            for j in range(yy.size): 
                tmps = tmps + "  " + repr(s[j,i])
            fs.write(' ' + repr(xx[i]) + " " + tmps )
            fs.write("\n")
        fs.close()
        print ("File for SHADOW "+outFile+" written to disk.")



#
# inputs
#
lengthY = 10.02
nDices = 100
nPoints = nDices*5
R=100.276845


#
# arrays
#
lengthX = lengthY

x = np.linspace(-lengthX/2,lengthX/2, nDices)
y = np.linspace(-lengthY/2,lengthY/2, nDices)
x1 = np.linspace(-lengthX/2,lengthX/2, nPoints)
y1 = np.linspace(-lengthY/2,lengthY/2, nPoints)

xx, yy = np.meshgrid(x, y)
xx1, yy1 = np.meshgrid(x1, y1)

#
#surface
#
zz = R - np.sqrt(R**2 - xx**2 - yy**2)
f = interpolate.interp2d(x, y, zz, kind='linear')

zz1 = f(x1, y1)  # linearly interpolated surface

#
# write SHADPW/PRESURFACE files
#
tmp = write_shadowSurface(zz,x,y,outFile='diced_original.dat')
tmp = write_shadowSurface(zz1,x1,y1,outFile='diced_interpolated.dat')

#
# plots
# 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

#
# original data
#
#fig = plt.figure(0)
#ax = fig.gca(projection='3d')
#ax.set_title('original')
#surf = ax.plot_surface(xx, yy, zz, rstride=1, cstride=1, cmap=cm.coolwarm,
#        linewidth=0, antialiased=False)

#
#interpolated data
#
#fig1 = plt.figure(1)
#ax1 = fig1.gca(projection='3d')
#ax1.set_title('more points')
#surf1 = ax1.plot_surface(xx1, yy1, zz1, rstride=1, cstride=1, cmap=cm.coolwarm,
#        linewidth=0, antialiased=False)

#
#central profile
#
fig2 = plt.figure(2)
# plt.plot(x, zz[nDices/2, :], 'ro-', x1, zz1[nPoints/2, :], 'b-')
plt.plot(x, zz[nDices/2, :], 'ro-',label="original")
plt.plot(x1, zz1[nPoints/2, :], 'b-',label="interpolated")
plt.legend()
plt.title("Crystal central profile")
plt.xlabel("Y [cm]")
plt.ylabel("Z [cm]")


plt.show()
