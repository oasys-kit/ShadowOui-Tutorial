#
# works with polynomial (linear) fit
#
"""

        functions: 
             goFromTo: calculates the phase shift matrix

"""
__author__ = "Manuel Sanchez del Rio"
__contact__ = "srio@esrf.eu"
__copyright = "ESRF, 2012"

import numpy, math
#from scipy import stats
import Shadow as sh
import Shadow.ShadowTools as st

def goFromTo(source,image,distance=1.0,lensF=None,wavelength=1e-10):
    #distance = numpy.array(distance)
    x1 = numpy.outer(source,numpy.ones(image.size))
    x2 = numpy.outer(numpy.ones(source.size),image)
    r = numpy.sqrt( numpy.power(x1-x2,2) + numpy.power(distance,2) ) - distance
    # add lens at the image plane
    if lensF != None:
      x10 = numpy.outer(source*0,numpy.ones(image.size))
      #print 'r: ',r
      # exact value
      rf = numpy.sqrt( numpy.power(x1-x2,2) + numpy.power(lensF,2) ) - lensF
      # approx value
      #rf = numpy.power(x10-x2,2)/(2*lensF)
      r = r - rf 
      #print 'rf: ',rf
      #print 'rnew: ',r

    wavenumber = numpy.pi*2/wavelength
    return numpy.exp(1.j * wavenumber *  r)


def goFromToShadow(source,image,distance=1.0,lensF=None,wavelength=1e-10):
    #distance = numpy.array(distance)
    x1 = numpy.outer(source,numpy.ones(image.size))
    x2 = numpy.outer(numpy.ones(source.size),image)
    r0 = numpy.sqrt( numpy.power(x1-x2,2) + numpy.power(distance,2) ) #- distance
    # add lens at the image plane
    if lensF != None:
        print('r0: ',r0)
        useshadowlocal = 1
        if useshadowlocal == 1:
            #rf = -0.5*numpy.outer(numpy.ones(source.size),lensF)

            # using fit alla mirone...
            #rf = (-2.5144013e-07*x2 -0.0012614668/2*x2*x2)
            #fit:  [ -1.25898614e-03  -5.97183893e-08]
  
            #print 'shapes image lensF: ',image.shape,lensF.shape
            zz = numpy.polyfit(image, lensF, 1)
            rf = zz[1]*x2 +zz[0]/2*x2*x2
            #print 'fit: ',zx
            
            #rf = -0.5*numpy.outer(numpy.ones(source.size),lensF)
        else:
            # applying phase change
            focal = distance/2
            # exact
            #rf = -numpy.sqrt( numpy.power(x1-x2,2) + numpy.power(focal,2) ) - focal 
            # paraxial
            rf = -numpy.power(x2,2)/(2*focal)

        r = r0 + rf 
        print('rf: ',rf)
        print('r: ',r)
    else:
     r = r0

    wavenumber = numpy.pi*2/wavelength
    return numpy.exp(1.j * wavenumber *  r)

def main():
    # inputs (working in m)
    useshadow = 1
    slitdistance =     30.9   # m
    detdistance  =     1.38   # m
    detsize      =     200e-6 # m
    energy       =     14.0    # keV
    realisations    =  1000
    lensF = None # detdistance/2 # focal distance
    shadowunits2m = 1e-2

    wavelength   =   12.398/(energy)*1e-10  # m
    #wavelength   =   500.0e-6 # mm
    # open output file
    f = open('twoslitsLeitenberger.spec', 'w')
    header="#F twoslitsLeitenberger.spec \n"
    f.write(header)


     
    # read shadow files
    #
    flag=st.getshcol("star.01",10)
    igood = numpy.where(flag >= 0)
    igood = numpy.array(igood)
    igood.shape = -1
    print(flag.size)
    print('igood: ',igood.size)
    print('--------------')

    # use shadow's number of points
    #sourcepoints = 200
    sourcepoints = igood.size
    slitpoints = sourcepoints/2
    detpoints = sourcepoints

    if useshadow == 1:
        #shadow
        position1x = st.getshcol("begin.dat",3) * shadowunits2m
        position1x = position1x[igood]
        position1x.shape = -1
    else:
        #grid
        sourcesize = 140e-6
        position1x = numpy.linspace(-sourcesize/2,sourcesize/2,sourcepoints)

    #position1x = st.getshcol("begin.dat",3) # * shadowunits2m
    #position1x = position1x[igood]
    #position1x.shape = -1
    #sourcesize = 140e-6
    #position1x = numpy.linspace(-sourcesize/2,sourcesize/2,sourcepoints)
    print('>>> maxmin: ',position1x.min(), position1x.max())
    

    if useshadow == 1:
        #shadow
        position2x = st.getshcol("screen.0101",3) * shadowunits2m
        position2x = position2x[igood]
        position2x.shape = -1
    else:
        #grid
        slitsize = 2e-6
        slitgap = 11.3e-6
        tmp = numpy.linspace(-slitsize/2,slitsize/2,slitpoints)
        position2x = numpy.concatenate((tmp-slitgap/2,tmp+slitgap/2))


    #position3x = st.getshcol("star.02",3)
    #position3x = position3x[igood]
    #position3x.shape = -1
    #direction3x = st.getshcol("star.02",6)
    #direction3x = direction3x[igood]
    #direction3x.shape = -1
    #vz0101 = st.getshcol("screen.0101",6)
    #vz0201 = st.getshcol("screen.0201",6)

    # working with angles...
    #tmp3 = -numpy.cos(numpy.arcsin(vz0201 -vz0101))
    #tmp3 = (tmp3-tmp3.min()) * 1590.0
    #tmp3 = tmp3[igood]
    #tmp3.shape = -1

    # working with differences
    #tmp3 = (vz0201 -vz0101)
    #tmp3 = tmp3[igood]
    #tmp3.shape = -1

    position3x = numpy.linspace(-detsize/2,detsize/2,igood.size)


    print('igood: ',igood.size,position1x.size,position2x.size,position3x.size)
    print('shape: ',igood.shape)
    #for j in range(detpoints):
    #    print j,igood[j],position1x[j],position2x[j],position3x[j]
    

    #direction3x = None
    if useshadow == 0:
        fields12 = goFromToShadow(position1x,position2x,slitdistance, lensF=None,wavelength=wavelength)
        fields23 = goFromToShadow(position2x,position3x,detdistance, lensF=None,wavelength=wavelength)
    else:
        fields12 = goFromTo(position1x,position2x,slitdistance, lensF=None,wavelength=wavelength)
        fields23 = goFromTo(position2x,position3x,detdistance, lensF=None,wavelength=wavelength)

    # from 1 to 3, matrix multiplication
    fields13 = numpy.dot(fields12,fields23)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #fields13 = fields23
    
    print('shape 12: ',fields12.shape)
    print('shape 23: ',fields23.shape)
    print('shape 13: ',fields23.shape)
    #sourcepoints = igood.size
    fieldComplexAmplitude = numpy.dot(numpy.ones(sourcepoints),fields13)
    fieldIntensity = numpy.power(numpy.abs(fieldComplexAmplitude),2)
    fieldPhase = numpy.arctan2(numpy.real(fieldComplexAmplitude), numpy.imag(fieldComplexAmplitude))
 

    print('fields: ',fields12.shape, fields23.shape)


    # do the ensemble average
    tmpSource = numpy.exp(1.j*2*numpy.pi* numpy.random.mtrand.rand(sourcepoints))
    fieldSource=tmpSource
    fieldIntensityEA = numpy.power(numpy.abs(fieldComplexAmplitude),2)
    for i in range(realisations-1): 
      #tmpSource = numpy.exp(1.j*2* numpy.pi*numpy.random.mtrand.rand(sourcepoints))
      #fieldComplexAmplitude = numpy.dot( tmpSource, fields13)
      #fieldIntensityEA = fieldIntensityEA + numpy.power(numpy.abs(fieldComplexAmplitude),2)

      tmpSource = numpy.exp(1.j*2* \
          numpy.pi*numpy.random.mtrand.rand(sourcepoints))
      fieldComplexAmplitude = numpy.dot( tmpSource, fields13)
      fieldIntensityEA = fieldIntensityEA + \
          numpy.power(numpy.abs(fieldComplexAmplitude),2)
    
    header="\n#S  1 2h=??\n"
    f.write(header)
    header="#N 4 \n#L Z[um]  intensityCoh  phaseCoh  intensityEnsemble\n"
    f.write(header)
    
    for i in range(igood.size):
       out = numpy.array((position3x[i]*1e6,  fieldIntensity[i], fieldPhase[i], fieldIntensityEA[i]))
       f.write( ("%20.11e "*out.size+"\n") % tuple( out.tolist())  )

    f.close()
    print("File written to disk: twoslitsLeitenberger.spec")
    return position3x,fieldIntensity,fieldIntensityEA

#print 'directions: ',direction3x
out_object = main()
