#!/usr/bin/env python
# Fitting of cmb measurements
# Introduction to Radio Astronomy 2017, By Sander Verdult
#Datasets 1, 7 , 10
import numpy as np
import matplotlib.pyplot as plt
import lmfit
from lmfit import Model

#Load data set
Angle, Power = np.loadtxt('data1.txt', skiprows=1, comments='#', unpack=True)
#Powers
Pcold = (Power[0]+Power[-1])/2   # mdB +- 0.002
Phot = (Power[1]+Power[-2])/2    # mdB +- 0.002  +/- 0.02/np.sqrt(8)
Phot2 = 10**(Phot/10)            # Convert from db to mw 
Pcold2 = 10**(Pcold/10)          # Convert from db to mw
Power_watt = 10**(Power/10)      # Convert frm db to mw
#Errors
P_error = 0.02/np.sqrt(8) #dBm
T_error = 0.1 #K
#temperatures
Thot = 4.5+273.16 #K sigma = 0.1 K
Tcold = 77.355 #k sigma = 0.1 K
Tatm = 4.5+273.16 #K
#angle
Z_Angle = Angle-90

#constants
Delta_nu = 1*10**9             #Bandwidth (1 Ghz)
T_R = 145.93                   #?
k = 1.38064852*10**(-23)     #Boltzmann constant 1.38064852(79)×10−23	J⋅K−1
Tau_zen = 0.01               #Tau at Zenith (assumed)

#Calculated receiver temperature
y = (10**(Phot/10))/(10**(Pcold/10))  # y factor
print('y =',y)
Trcvr = (Thot-(Tcold*y))/(y-1)  #receiver temperature in K
print('Trcvr =',Trcvr, 'K')

#calculate Gain
GainHOT = Phot2 / ((Thot+Trcvr)*k*Delta_nu)
print(GainHOT,'Gain in milli watts')
GainCOLD = Pcold2 / ((Tcold+Trcvr)*k*Delta_nu)
print(GainCOLD, 'Gain in milli watts, should be identical')
Gain = GainHOT
Tsys = Power_watt/(k*Delta_nu*Gain)
GaindBm = 10*np.log10(GainHOT)
print(GaindBm, 'Gain in dBm')
GaindBW = GaindBm - 30
print(GaindBW, 'Gain in DbW')
print(Gain)

#### Start fitting https://lmfit.github.io/lmfit-py/model.html ####
def background(x, Tcmb, Tau0,Tatm,Trcvr):
    return Tcmb*np.exp(-Tau0 / (np.cos(x))) + Tatm*(1-np.exp(-Tau0 / (np.cos(x)))) + Trcvr

gmod = Model(background)
print(gmod.param_names, gmod.independent_vars) #show parameters and independant variables
#gmod.guess()
result = gmod.fit(Z_Angle[2:-20], x=Z_Angle[2:-20], Tcmb=1, Tau0=1, Tatm=Tatm, Trcvr = Trcvr )

print(result.fit_report())
##########################

############# Plot things ################################
fig = plt.figure()
frame1 = fig.add_subplot(1,1,1)

#lables and titles
frame1.set_title("System temperature as a function of Zenith temperature")    
frame1.set_xlabel('# Angle (deg from Zenith)')
frame1.set_ylabel('Temperature (Kelvin)')
plt.ylim((0,200))


#plot lines
frame1.plot(Z_Angle[2:-20],Tsys[2:-20], c='r', label='Measurements')
frame1.axhline(Trcvr, c='b', label='Receiver Temperature')

#Show legend
leg = frame1.legend()
#execute
plt.show()
###################################################


#"""
#Gain Directivity = 4*pi / d ohm) 
#Fit guassian, Find Gain of the horn
#"""