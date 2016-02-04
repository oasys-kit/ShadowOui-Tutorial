#
# script to calculate tangential and sagittal focusing radii for crystals
# and Rowland condition for gratings and asymmetric crystals
#
import xraylib 
import numpy

import scipy.constants.codata
codata = scipy.constants.codata.physical_constants
codata_c, tmp1, tmp2 = codata["speed of light in vacuum"]
codata_h, tmp1, tmp2 = codata["Planck constant"]
codata_ec, tmp1, tmp2 = codata["elementary charge"]
tocm = codata_h*codata_c/codata_ec*1e2

#
# define miller indices, distances and photon energy in eV
#
hh = 1
kk = 1
ll = 1
d1 = 3000.0
d2 = 3000.0
alpha = 5.0 * numpy.pi / 180.0 # asymmetry angle in rad
crystal_name = "Si"
photon_energy_ev = 10000.0

#
# get crystal info from xraylib
#
cryst = xraylib.Crystal_GetCrystal(crystal_name)
dspacing = xraylib.Crystal_dSpacing(cryst,hh,kk,ll )

#sin_theta = (tocm/(photon_energy_ev*2.0*dspacing*1e-8));

#rt=2*p*q/(p+q)/sin_theta;
#rs=2*p*q*sin_theta/(p+q);

theta=numpy.arcsin(tocm/(photon_energy_ev*2.0*dspacing*1e-8))
t1 = theta + alpha
t2 = theta - alpha

#calculations

s1 = numpy.sin(t1)
s2 = numpy.sin(t2)
s1_2 = s1*s1
s2_2 = s2*s2
r = s1_2/d1 + s2_2/d2
r = (s1+s2)/r
rs = (s1+s2)/(1.0/d1 + 1.0/d2)

print("Using crystal: %s %d%d%d at E=%.3f eV"%(crystal_name,hh,kk,ll,photon_energy_ev))
print("               dspacing: %f A"%dspacing)
print("               initial p=%.3f, q=%.3f"%(d1,d1))
print("Results: ")
print("               BraggAngle=%.3f deg"%(theta*180/numpy.pi))
print("               IncAngle=%.3f deg, RefAngle=%.3f deg"%(t1*180/numpy.pi,t2*180/numpy.pi))
print("               Rtangential = %f, Rsagittal=%f"%(r,rs))
print("           ROWLAND condition: ")
print("               rowland p=R1=%.3f, q=R2=%.3f"%(r*s1,r*s1))
print("           For p=R1=%.3f the ROWLAND condition is: "%(d1))
print("               q=R2=%.3f, R=%.3f"%(d1*s2/s1,d1/s1))
