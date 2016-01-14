import numpy
#
# creates twoslits.pol
#
corners = numpy.array([-1.0,-1.0,1,1])*1e-4 # x_leftbottom,y_leftbottom,x_rightup,y_roghtup

t = numpy.array([0,11.3e-4])/2  # translation vector (i.e., horiz. and V preiods)
n = numpy.array([0,1])  # number of translation (H,V)


file_name = 'twoslits.pol'
f = open(file_name,'w')

nn = (2*n[0]+1)*(2*n[1]+1)

f.write("%d\n"%(nn-1))
for i in range(-n[0],n[0]+1,1):
    for j in range(-n[1],n[1]+1,1):
        if not((i == 0) and (j == 0)):
            f.write("4\n")
            f.write("%f %f\n"%(corners[0]+i*t[0],  corners[1]+j*t[1]))
            f.write("%f %f\n"%(corners[0]+i*t[0],  corners[3]+j*t[1]))
            f.write("%f %f\n"%(corners[2]+i*t[0],  corners[3]+j*t[1]))
            f.write("%f %f\n"%(corners[2]+i*t[0],  corners[1]+j*t[1]))
f.close()
print('File written to disk: ',file_name)
