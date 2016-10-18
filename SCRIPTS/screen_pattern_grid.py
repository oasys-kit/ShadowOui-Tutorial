#
# creates grid.pol
#
import numpy 


corners = numpy.array([-3.0,-1.5,3,1.5]) # x_leftbottom,y_leftbottom,x_rightup,y_roghtup
t = numpy.array([9.0,4.5])               # translation vector (i.e., horiz. and V preiods)
n = numpy.array([2,3])                   # number of translation (H,V)


file_out = "grid.pol"
f = open(file_out,'w') 
nn = (2*n[0]+1)*(2*n[1]+1)
f.write("%d\n"%nn)

#pay attention that the last element is not included...
n0 = numpy.arange(-n[0],n[0]+1)
n1 = numpy.arange(-n[1],n[1]+1)
for i in n0:
   for j in n1:
       f.write("%d\n"%4)
       f.write(  "%f  %f  \n"%(corners[0]+i*t[0],  corners[1]+j*t[1]) )
       f.write(  "%f  %f  \n"%(corners[0]+i*t[0],  corners[3]+j*t[1]) )
       f.write(  "%f  %f  \n"%(corners[2]+i*t[0],  corners[3]+j*t[1]) )
       f.write(  "%f  %f  \n"%(corners[2]+i*t[0],  corners[1]+j*t[1]) )
f.close()
print('file %s written to disk.'%file_out)
