import numpy as np

#
#
#
r = 30.0
theta_deg = 88.2 

d0 = 1.0/800
E0 = 1600.0
m = -1


#
# inputs
#
theta = theta_deg * np.pi / 180


print("------------- INPUTS ----------------------")
print("theta = %f deg = %f rad"%(theta_deg,theta))
print("1/d0 = %f lines/mm"%(1/d0))
print("r = %f m"%(r))
print("order = %d m"%(m))
print("photon energy = %f eV"%(E0))
#
# calculations
#


lambda_A = 12398.0/E0 
lambda_mm = lambda_A * 1e-7
lambda_1000_mm = 12398.0/1000.0 * 1e-7

beta_1000 = np.arcsin(m*lambda_1000_mm/2/d0/np.cos(theta)) - theta
alpha_1000 = 2*theta + beta_1000

beta = np.arcsin(m*lambda_mm/2/d0/np.cos(theta)) - theta
alpha = 2*theta + beta


R = r / np.cos(alpha_1000)
rp = R * np.cos(beta_1000)

#
# results
#

print("------------- OUTPUTS ----------------------")
print("Lambda = %f A = %g mm "%(lambda_A,lambda_mm))
print("alpha=%f deg, beta=%f deg"%(alpha*180/np.pi,beta*180/np.pi))
print("R=%f, r=%f, r'=%f"%(R,r,rp))

deltaLambda = d0/m*35e-3/(rp*1e3)*np.cos(beta)
print("estimated Delta Lambda = %f A"%(deltaLambda*1e7))
print("Resolving power = %f "%(lambda_mm/deltaLambda))
print("estimated focal size FWHM = %f um"%(2.35*15.4*np.cos(alpha)/np.cos(beta)*rp/r))