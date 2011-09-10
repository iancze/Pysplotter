#!/usr/bin/env python2

#import matplotlib
#matplotlib.use("tkagg")
#import matplotlib.pyplot as plt
import numpy as np
from constants import *
import asciitable

'''Photometry is used to obtain information about the brightness of an object.
Conversions between the various photometric systems.
The Landolt photometric system is defined as the Johnson UBV bands plus the Cousins RI bands.
References are: Malcom Hickam:

Output from Kepler Photometry Pipeline
When you convert them to the standard system they are in the Landolt
system (which is approximately Vega) for BV and to the Smith paper for
u'r'i' (which are approximately AB:
http://www.sdss.org/dr5/algorithms/fluxcal.html#sdss2ab
http://www.sdss.org/dr5/algorithms/sdssUBVRITransform.html  )

When not in the standard system the colors differ by a factor of the
color terms.

Smith 2002, 

All flux should be returned in Janskys. It's an intuitive unit. Use it.

'''

#Effective wavelength of filters, in angstroms
#Data from Hale Bradt, Astronomy Methods pg 228
filter_wheel =  {"U":3670, #Violet Light
"B":4360, #Blue Light
"V":5450, #Green Light
"R":6380, #Red Light
"I":7970, #Infrared Light
#SLOAN Set from Fukugita 1996
"u":3557, #Violet Light
"g":4825, #Cyan Light
"r":6261, #Red Light 
"i":7672, #Very Red Light
"z":9097} #Infrared Light

#Load filter transmission/response curves (which?)
base = "/home/ian/Grad/Programming/Python/AstroTools/Filter_Data/"
#Load the SLOAN transmission curves
u_trans = asciitable.read(base + "u'_transmission.dat")
g_trans = asciitable.read(base + "g'_transmission.dat")
r_trans = asciitable.read(base + "r'_transmission.dat")
i_trans = asciitable.read(base + "i'_transmission.dat")
z_trans = asciitable.read(base + "z'_transmission.dat")
#Load Morgan-Johnsons Cousins curves
U_trans = asciitable.read(base + "U_transmission.dat")
B_trans = asciitable.read(base + "B_transmission.dat")
V_trans = asciitable.read(base + "V_transmission.dat")
R_trans = asciitable.read(base + "R_transmission.dat")
I_trans = asciitable.read(base + "I_transmission.dat")

#Load the response curves
# Johnson-Cousins
U_response = asciitable.read(base + "bessel_UX_response.dat")
B_response = asciitable.read(base + "bessel_B_response.dat")
V_response = asciitable.read(base + "bessel_V_response.dat")
R_response = asciitable.read(base + "bessel_R_response.dat")
I_response = asciitable.read(base + "bessel_I_response.dat")

#Sloan Response curves
u_response = asciitable.read(base + "usno_u.res")
g_response = asciitable.read(base + "usno_g.res")
r_response = asciitable.read(base + "usno_r.res")
i_response = asciitable.read(base + "usno_i.res")
z_response = asciitable.read(base + "usno_z.res")

responses = {"U":U_response,"B":B_response,"V":V_response,"R":R_response,"I":I_response,
        "u":u_response,"g":g_response,"r":r_response,"i":i_response,"z":z_response}

#Load Reddening Tables for Landolt and Sloan
#"filter":[lambda_eff, A/A(V), A/E(B-V)]
SFD = {"U":[3372.,1.664,5.434],
"B":[4404.,1.321,4.315],	
"V":[5428.,1.015,3.315],	
"R":[6509.,0.819,2.673],	
"I":[8090.,0.594,1.940],	
"u":[3546.,1.579,5.155],
"g":[4925.,1.161,3.793],
"r":[6335.,0.843,2.751],
"i":[7799.,0.639,2.086],
"z":[9294.,0.453,1.479]}

#Filter conversions from Bessel 1979
filter_zero = 	{#"Filter": [central \lambda, flux (Jy)]
"U":[3600.,1810.],
"B":[4400.,4260.],
"V":[5500.,3640.],
"R":[6400.,3080.],
"I":[7900.,2550.]
}

#vim command used to sort
#:'<,'>s/\(.\)\s\+\([[:digit:]]\+\)\s\+\([[:digit:]\.]\+\)\s\+\([[:digit:]\.]\+\)/"\1":[\2.,\3,\4],/  

def extinction(E_B_V,filt):
    return SFD[filt][2] * E_B_V


#def plot_sloan_filters():
#		fig = plt.figure()
#		ax = fig.add_subplot(111)
#		ax.fill_between(u_trans["WL"],u_trans["TRANS"],alpha=0.3,color="b")
#		ax.fill_between(g_trans["WL"],g_trans["TRANS"],alpha=0.3,color="c")
#		ax.fill_between(r_trans["WL"],r_trans["TRANS"],alpha=0.3,color="r")
#		ax.fill_between(i_trans["WL"],i_trans["TRANS"],alpha=0.3,color="y")
#		ax.fill_between(z_trans["WL"],z_trans["TRANS"],alpha=0.3,color="k")
#		ax.xaxis.set_minor_locator(matplotlib.ticker.MaxNLocator(49,steps=[1,5,10]))
#		ax.set_xlabel("Wavelength (Angstrom)")
#		ax.set_ylabel("Transmission")
#		ax.set_title("Sloan Filter Set Transmission")
#		plt.show()

'''Sloan filter transmission curves taken from: http://www.sdss.org/dr5/algorithms/standardstars/Filters/response.html'''




def distance_modulus(distance):
	'''Given a distance in parsecs, returns the value :math:`m - M`, a characteristic value used to convert from apparent magnitude :math:`m` to absolute magnitude, :math:`M`. 
	Uses the formula from Carroll and Ostlie, where :math:`d` is in parsecs 

    .. math::

        m - M = 5 \log_{10}(d) - 5 = 5 \log_{10}(d/10)'''
	return 5 * log(distance/10.0)/log(10.)

def distance_from_modulus(m, M):
	'''Given the distance modulus, return the distance to the source, in parsecs. Uses Carroll and Ostlie's formula,

    .. math::

        d = 10^{(m - M + 5)/5}'''
	return 10.0**(m - M + 5)/5

def lamb_to_Hz(lamb):
    '''Takes in a wavelength in Angstroms and converts it to Hz'''
    return c / (lamb * 1e-8)

def pc_to_cm(parsec):
    '''Takes in a measurement in parsecs and returns cm'''
    return parsecc * pc

def AU_to_cm(AUnit):
    '''Takes in a measurement in AU and returns cm'''
    return AUnit * AU

def Jy_to_AB(flux):
    '''Given the flux (in units of Janskys) of an object taken through a specific filter, return the AB magnitude. Uses Oke 1974 ApJ 27, 21 
    
    .. math::

            \rm AB = -2.5 \log( f_\nu \cdot 10^{-23}) - 48.60'''
    return -2.5 * log10(flux * 1e-23) - 48.6

def AB_to_Jy(AB):
		'''Given the AB magnitude of an astronomical object, return the flux in units of Janksys using the equation from Oke 1974 ApJ 27, 21

		.. math::

				f_\nu = 10^{23} \cdot 10^{(\frac{\rm AB + 48.60}{-2.5})}'''
		return 1e23 * 10**((AB + 48.60)/(-2.5))

def AB_to_Jy_err(flux,flux_err):
    return 1e23 * 10**(-(flux + 48.0)/2.5) * np.log(10.) * flux_err/2.5

def AB_to_Jy_err_func(flux, flux_err,filt=None):
    '''AB Magnitudes do not care about filters, but the filter parameter is included to make the calling consistent.'''
    func = lambda f: 2.5 /(np.log(10) * f * flux_err * np.sqrt( 2.0 * np.pi)) * np.exp(- (Jy_to_AB(f) - flux)**2.0/(2. * flux_err**2.))
    return func

def JC_to_Jy(mag, filt):
    '''Given the Johnson-Cousins magnitude of an astronomical object, taken in a specific filter, return the flux in units of Jys. Absolute calibrations are taken from Bessel, 1979 '''
    filters = 	{#"Filter": [central \lambda, flux (Jy)]
                    "U":[3600.,1810.],
                    "B":[4400.,4260.],
                    "V":[5500.,3640.],
                    "R":[6400.,3080.],
                    "I":[7900.,2550.]
                }
    flux = filters[filt][1] * 10**(mag/(-2.5))	
    return flux

def JC_to_Jy_err(mag, mag_err, filt):
    filters = 	{#"Filter": [central \lambda, flux (Jy)]
        "U":[3600.,1810.],
        "B":[4400.,4260.],
        "V":[5500.,3640.],
        "R":[6400.,3080.],
        "I":[7900.,2550.]
    }
    sigma_flux = filters[filt][1] * np.log(10.)/2.5 * 10**(mag/(-2.5)) * mag_err 	
    return sigma_flux

def mag_from_flux(flux, filt):
    return -2.5 * np.log10(flux/filter_zero[filt][1])

def JC_to_Jy_err_func(mag, mag_err, filt):
    func = lambda f: 2.5 /(np.log(10) * f * mag_err * np.sqrt( 2.0 * np.pi)) * np.exp(- (mag_from_flux(f,filt) - mag)**2.0/(2. * mag_err**2.))
    return func


#
def Flamb_to_Fnu(wave,Flamb):
    # Convert from angstroms to cm
    wavec = wave * 1e-8
    Fnu = 1e8 * Flamb * wavec**2/c
    # This is now in Jy?
    return Fnu*1e23

def Flamb_to_Jy(Flamb, wave):
    '''Takes in a Flamb in [erg/(s cm^2 ang)] and returns 1e23 * [erg/(s cm^2 Hz)]'''
    #Convert from ang to cm
    wavec = wave * 1e-8
    Flambc = Flamb * 1e8
    Fnu = Flambc * wavec**2/c # now in [erg/(s cm^2 Hz)]
    Jy = 1e23 * Fnu
    return Jy

def astro_blackbody(nu, T, r, R):
    '''Use to model the flux from an astrophysical source as from a blackbody. Takes in frequency in Hz, Temperature in Kelvin, radius and distance in cm. Assumes spherical sounce and F = pi B (R/r)**2 from Rybicki.Returns flux in Jy'''
    Fnu = 2 * np.pi * h * nu**3 * R**2 / (r**2 * c**2 * (np.exp(h * nu/ (k * T)) - 1)) 
    Jy = 1e23 * Fnu
    return Jy

def fit_astro_blackbody(nu, r):
    '''Takes in known values and returns a function useful for fitting temperature and radius'''
    func = lambda T,R: astro_blackbody(nu, T, r, R)
    return func

def blackbody_func_filter(filt, d):
    return fit_astro_blackbody(lamb_to_Hz(filter_wheel[filt]), d)

def planck(x, T, inp="wave", out="freq"):
    '''General Planck blackbody function to fit to photometry with different filters. Specify `inp` for whether one desires input as wavelength (Angstroms) or frequency (Hz). Specify `out` for whether one desires output as :math:`B_\lambda` or :math:`B_\nu`.'''
    # TODO: better error checking here on inp and out.
    if out=="freq":
        nu,lamb = 0,0
        if inp=="wave":
                nu = c/(x*1e-8)
                #print nu
        else:
                nu = x
#				print "h",h
#				print "nu",nu
#				print "c",c
#				print "k",k
#				print "T", T
#				print "h * nu /(k * T)", h * nu/ (k * T)
#				print "exp()",exp(h * nu/ (k * T))
# 
#				print "nu**3", nu**3
#				print "expression", ((2 * h * nu**3)/c**2) /(exp(h * nu / (k * T)) - 1)
        return ((2 * h * nu**3)/c**2) /(np.exp(h * nu / (k * T)) - 1)
    else:
        if inp=="wave":
                lamb = x*1e-8
        else:
                lamb = c/x
        #return 2 * h * c**2 / lamb**5 / (exp(h * c/ (lamb * k * T)) - 1)

def fit_planck(T,d,r,x, inp="wave", out="freq"):
		return np.pi * (r/d)**2 * 1.e23 * planck(x,T,inp=inp,out=out)
		

def test_planck():
		'''Implement a bunch of plots to see I coded `planck` correctly.'''
		xs = logspace(7,16)
		ws = c/xs
		y1 = planck(xs, 5000,inp='freq')
		y2 = planck(ws, 5000)
		loglog(xs,y1)
		loglog(xs,y2)
		show()

				
if __name__ == "__main__":
#		print("B flux",JC_to_Jy(18.5,"B"))
#		print("V flux",JC_to_Jy(17.6,"V"))
#		print("r flux",AB_to_Jy(17.5))
#		print("i flux",AB_to_Jy(17.4))
#		ys = array([JC_to_Jy(18.5,"B"),JC_to_Jy(17.6,"V"),AB_to_Jy(17.5),AB_to_Jy(17.4)])
#		xs = array([4400.,5500.,6260.,7670.])
#
#		from scipy.optimize import leastsq
#		fit_func = lambda p,x:fit_planck(p[0],p[1],x)
#		err_func = lambda p,x,y: ys - fit_func(p,x)
#		p1,success = leastsq(err_func,array([3900.,1e2]),args=(xs,ys))
#		print p1
#		#print(planck(xs, 4000*ones(len(xs))))
#
#		
#		plot(xs,ys,"bx")
##		plot(xs,planck(xs,4000*ones(len(xs))))
#		plot(xs,fit_func(p1,xs),label="T=%.1f K" % p1[0])
#		title("Blackbody of SN2010U")
#		xlabel("Wavelength")
#		ylabel("Flux, (Jy)")
#		legend()
#		show()
		plot_sloan_filters()
