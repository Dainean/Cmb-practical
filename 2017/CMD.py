#!/usr/bin/env python
# Fitting of cmb measurements
from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as plt

#Load data set
Angle, Power = np.loadtxt('data1.txt', skiprows=3, comments='#', unpack=True)
Pcold = -23.240 #mdB +- 0.002
Phot = -20.460 #mdB +- 0.002
Thot = 5.6+273.16 #K +-0.05?
Tcold = 77.355 #k
Z_Angle = Angle-90
Phot2 = 10**(Phot/10)/1000  # From db to watt
Pcold2 = 10**(Pcold/10)/1000  # From db to watt
Power_watt = 10**(Power/10)/1000

#constants
Delta_nu = 1*10**9
T_R = 145.93
k = 1.3806*10**(-23)
Tau_zen = 0.01 

#Calculated values
y = (10**(Phot/10))/(10**(Pcold/10))  # y factor
print('y =',y)
Trcvr = (Thot-(Tcold*y))/(y-1)
print('Trcvr =',Trcvr, 'K')


Gain = Phot2 / ((Thot+Trcvr)*k*Delta_nu)
print(Gain,'Gain in watts')
Gain_Dbm = 10*np.log10(1000*Gain) #From watt to db
print(Gain_Dbm, 'gain in Dbm')

Tsys = Power_watt/(k*Delta_nu*Gain)
#Gain_c = Pcold / ((Tcold+Trcvr)*k*delta_nu)
#print(Gain_c)

#Ptot = 10**((Power-30)/10) #Watts


fig = plt.figure()
frame1 = fig.add_subplot(1,1,1)

frame1.set_title("System temperature as a function of Zenith temperature")    
frame1.set_xlabel('# Angle (deg)')
frame1.set_ylabel('Power (dBm)')

frame1.plot(Z_Angle,Tsys, c='r', label='Measurements')
frame1.axhline(Trcvr, c='b', label='Receiver Temperature')

leg = frame1.legend()

plt.show()

#"""
#Gain Directivity = 4*pi / d ohm) 
#Fit guassian, Find Gain of the horn
#"""
