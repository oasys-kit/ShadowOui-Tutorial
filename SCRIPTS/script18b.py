#
# script to calculate tangential and sagittal radii for crystals
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
p = 3000.0
q = 1000.0
crystal_name = "Si"
photon_energy_ev = 20000.0

#
# get crystal info from xraylib
#
cryst = xraylib.Crystal_GetCrystal(crystal_name)
dspacing = xraylib.Crystal_dSpacing(cryst,hh,kk,ll )
print("dspacing: %f A \n"%dspacing)

sin_theta = (tocm/(photon_energy_ev*2.0*dspacing*1e-8));

rt=2*p*q/(p+q)/sin_theta;
rs=2*p*q*sin_theta/(p+q);

print("Using crystal: %s %d%d%d at E=%.3f eV"%(crystal_name,hh,kk,ll,photon_energy_ev))
print("               p=%.3f, q=%.3f"%(p,q))
print("Rtangential = %f, Rsagittal=%f"%(rt,rs))