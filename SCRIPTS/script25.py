import Shadow
"""
fresnel: 
        functions: 
             goFromTo: calculates the phase shift matrix
 
"""

__author__ = "Manuel Sanchez del Rio"
__contact__ = "srio@esrf.eu"
__copyright = "ESRF, 2012"

import numpy, math

def goFromTo(source,image,distance=1.0,lensF=None,wavelength=1e-10):
    distance = numpy.array(distance)
    x1 = numpy.outer(source,numpy.ones(image.size))
    x2 = numpy.outer(numpy.ones(source.size),image)
    r = numpy.sqrt( numpy.power(x1-x2,2) + numpy.power(distance,2) )
    # add lens at the image plane
    if lensF != None:
      r = r - numpy.power(x1-x2,2)/lensF
    wavenumber = numpy.pi*2/wavelength
    return numpy.exp(1.j * wavenumber *  r)

def main():

    wavelength = 12398.419 / 11000.0 * 1e-10 # 11 keV in m
    detector_size = 200e-6
    distance = 5.50
    use_shadow_file = 1


    detpoints =  500
    lensF        =   None
    shadowunits2m = 1e-2


    if use_shadow_file:
        #screen0101 = Shadow.Beam()
        #screen0101.load("screen.0101")
        screen0101 = in_object_1._beam
        position1x = screen0101.getshcol(3) * shadowunits2m
        flag=screen0101.getshcol(10)
        igood = numpy.where(flag >= 0)
        igood = numpy.array(igood)
        igood.shape = -1
        sourcepoints = igood.size
        print (flag.size)
        print ('igood: ',igood.size)
        print ('--------------')
        position1x = position1x[igood]
        position1x.shape = -1
    else:
        position1x = numpy.linspace(-50e-6,50e-6,201)
        sourcepoints = position1x.size

    position2x = numpy.linspace(-detector_size/2,detector_size/2,detpoints)
    
    fields12 = goFromTo(position1x,position2x,distance, \
        lensF=lensF,wavelength=wavelength)
    print ("Shape of fields12: ",fields12.shape)

    #prepare results
    fieldComplexAmplitude = numpy.dot(numpy.ones(sourcepoints),fields12)
    print ("Shape of Complex U: ",fieldComplexAmplitude.shape)
    print ("Shape of position1x: ",position1x.shape)
    fieldIntensity = numpy.power(numpy.abs(fieldComplexAmplitude),2)
    fieldPhase = numpy.arctan2(numpy.real(fieldComplexAmplitude), \
                               numpy.imag(fieldComplexAmplitude))


    #
    # write spec formatted file
    #
    out_file = "fresnel.spec"
    f = open(out_file, 'w')
    header="#F %s \n\n#S  1 fresnel-kirchhoff diffraction integral\n#N 3 \n#L X[m]  intensity  phase\n"%out_file

    f.write(header)
    
    for i in range(detpoints):
       out = numpy.array((position2x[i], fieldIntensity[i],
fieldPhase[i]))
       f.write( ("%20.11e "*out.size+"\n") % tuple( out.tolist())  )
    
    f.close()
    print ("File written to disk: %s"%out_file)

    #
    #plots
    #
    from matplotlib import pylab as plt

    plt.figure(1)
    plt.plot(position2x*1e6,fieldIntensity)
    plt.title("Fresnel-Kirchhoff Diffraction")
    plt.xlabel("X [um]")
    plt.ylabel("Intensity [a.u.]")
    plt.show()


main()
