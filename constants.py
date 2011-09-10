#!/usr/bin/env python2

#AstroTools constants. All units are CGS unless otherwise stated.

#General Conversion Factors
day = 24.0 * 3600.0 #s

#Astronomy Constants

#Thompson scattering coefficient
sigma_T = 6.65e-25 #cm^2


#Atomic
amu = 1.6605402e-24	 #g
#Mass of Hydrogen Atom
m_H = 1.6733e-24 #g

#Planetary
M_sun = 1.99e33 #g

M_earth = 5.9736e27 #g
R_earth = 6.378136e8 #cm
P_earth = 0.997271* day #s

M_mercury = 0.05528 * M_earth #g
R_mercury = 0.3825 * R_earth #cm
P_mercury = 58.6462 * day #s

M_venus = 0.81500 * M_earth #g
R_venus = 0.9488 * R_earth #cm
P_venus = 243.018 * day #s

#TODO: add the rest of the planetary constants

#Physical Constants
h = 6.626068e-27 #cm^2 g s^-1
h_bar = 1.05457148e-17 #cm^2 g s^-1
c = 2.99792458e10 #cm s^-1
k = 1.3806504e-16 #erg K^-1
G = 6.67259e-8 #cm3 g-1 s-2

#Conversion factors
pc = 3.0856776e18 #cm
AU = 1.4959787066e13 #cm
