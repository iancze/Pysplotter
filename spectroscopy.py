#!/usr/bin/env python2
# Ian Czekala
# Harvard University Astronomy Grad Student
# Wed 15 Dec 2010 11:06:16 AM EST
# Routines for interpreting astronomical spectra of expanding objects.
# All units cgs, angstroms.

# docstrings can be called on any of the functions by doing Python's
# "help(function)"

import matplotlib.pylab as plt
from common_lines import wl
import math
from scipy.interpolate import interp1d
from scipy.optimize import fmin
from scipy.optimize import fminbound
from scipy.integrate import quad
from scipy.integrate import simps
from constants import *
import numpy as np
import photometry

# define constants
c = 2.9979e10 #cm/s

#f = open("redshifted_lines.dat","w")

# Lines identified from SPLOT
# uncertainty should be ~ bin width?
OI_red = 7786.4
OI_blue = 7750.7

Ha = 6567.4

FeII_blue = 6139.7
FeII_red = 6173.6

NaI_blue = 5875.7
NaI_red = 5912.1

#FeII multiplet
#Red peaks
FeII1_red = 5184.5
FeII2_red = 5026.0
FeII3_red = 4931.6

#Blue peaks 
FeII1_blue = 5150.7
FeII2_blue = 4999.2
FeII3_blue = 4909.1

Hb = 4868.7
Hc = 4348.9

def shift(line,z=0):
    '''Redshifts a line, given the rest wavelength and the redshift, z. All
    lines in angstroms.'''
    delta_lamb = line * z
    return line + delta_lamb

def gamma(v):
    '''Calculates relativistic `\gamma` based upon velocity (in km/s).
    ..math:
        
        \gamma = (1 - v_z^2/c^2)^{-1/2}'''
    #Hasn't been vetted yet
    return (1.0 - (v*1e5)**2/c**2)**(-0.5)

def vel_ref(obs_line, ref_line, rel=False):
    '''Given an observed line `\lambda` and a reference line `\lambda^\prime` (in Angstroms), calculate the velocity of
    the Doppler shift of the observed line, using the relativistic doppler formula. All lines in angstroms.
    Default output units are 'km/s'.

    Relativistic
    ..math:

    v = c \left ( 1 - \frac{\lambda}{\lambda^\prime \gamma} \right )			
   
    ..math:

    v = c \left ( 1 - \frac{2}{(\lambda/\lambda^\prime)^2 + 1} \right )

    Non Relativistic
    ..math:

    v = c \left ( 1 - \frac{\lambda}{\lambda^\prime} \right )			
    '''
    obs = obs_line * 1e-8
    ref = ref_line * 1e-8
    # float() is to ensure floating point division.
    if rel:
        #use relativistic Doppler formula
        return c * 1e-5 * ( 1. - 2./((float(obs)/float(ref))**2 + 1.))
    else:
        #use non-relativistic Doppler Formula
        return c * 1e-5 * (float(obs)/float(ref) -1 )

def hist_plot_lines(x,y):
    '''Given a spectrum with values, return lines that give the IRAF ability to show as histogram columns of flux'''
    length = len(x)
    x_fin = []
    y_fin = []
    if length != len(y):
        print "Input arrays must be the same length"
    else:
        x_fin.append((x[0]+x[1])/2.0)
        y_fin.append(y[0])
        for i in range(1,2 * length - 1):
            j = int(i/2)
            k = int((i - 1 )/ 2)
            x_fin.append((x[k] + x[k+1])/2.0)
            y_fin.append(y[j])
        x_fin.append((x[-1] + x[-2])/2.0)
        y_fin.append(y[-1])
        return x_fin,y_fin


def velcalc_uncertainty(obs_line, obs_line_uncer, ref_line, ref_line_uncer):
    '''Given an observed line, observed line uncertainty, ref line, and
    ref line uncertainty, returns the
    uncertainty in the velocity calculation.'''
    v = velcalc(obs_line, ref_line, units='cm/s')
    return sqrt( (c * ref_line * ref_line_uncer/(obs_line**2 * v))**2 \
                +(-c * ref_line_uncer/(obs_line * v))**2)


def redshift(obs_line, ref_line):
    '''Given an observed line and a reference line, calculate the redshift of
    the object. All lines angstroms.''' 
    return obs_line/ref_line - 1.0

def redshift_uncertainty(obs_line, obs_line_uncer, ref_line):
    '''returns the uncertainty in a redshift calculation given the
    uncertanity of the peak of the observed line. Ie, 0.87 => 87%
    uncertainty.'''
    return obs_line_uncer/(ref_line * redshift(obs_line, ref_line))

def find_peak(xs,ys,guess,spread=50.):
    '''Find the top of the spectral line, assuming that the user has given coordinates within the local maximum'''
    lower = guess - spread
    upper = guess + spread
    vals = np.where(( xs > lower) & (xs < upper))
    interp_func = interp1d(xs[vals],ys[vals])
    fit_func = lambda x: - interp_func(x)
    max_x = fminbound(fit_func, lower, upper)
    max_y = interp_func(max_x)
    return [max_x,max_y]

def annotate_line(label,wavelength,ax,xs,ys,offset=1e-16,length=16):
    '''Annotate the spectral line in a plot, given the current axes'''
    max_x,max_y = find_peak(xs,ys,wavelength)
    print max_x,max_y
    
    print max_y + offset

    ax.annotate(label,(wavelength,max_y + offset),(0,length),textcoords="offset points",rotation="vertical",horizontalalignment="center",verticalalignment="bottom",arrowprops={"width":.1,"frac":1,"headwidth":.1},size=10).draggable()

def annotate_multiplet(name,wavelength,ax,xs,ys,offset=5e-17,length=5e-17,label="Base"):
    lines =[]
    if not isinstance(name,str):
        for i in name:
            lines+=wl[i]
    else:
        lines = wl[name]
    lines.sort()
    max_x,max_y = find_peak(xs,ys,wavelength)

    #Get all the vertical lines
    for i in lines:
        ax.annotate("",(i,max_y + offset),(i,max_y + offset + length),textcoords="data",rotation="vertical",horizontalalignment="center",verticalalignment="bottom",arrowprops={"width":.1,"frac":1,"headwidth":.1})
    
    y_val = max_y + offset + length
    ax.annotate("",(lines[0],y_val),(lines[-1],y_val),xycoords="data",textcoords="data",rotation="horizontal",horizontalalignment="center",verticalalignment="bottom",arrowprops={"width":.1,"frac":1,"headwidth":.1})

    ag = np.mean(np.array(lines))
    ax.annotate(label,(ag,y_val),(ag,y_val + length),xycoords="data",textcoords="data",rotation="vertical",horizontalalignment="center",verticalalignment="bottom",arrowprops={"width":.1,"frac":1,"headwidth":.1},size=10)

def annotate_multiplet_l(name,lines,wavelength,ax,xs,ys,offset=5e-17,length=5e-17,xoff=0,yoff=0):
    lines.sort()
    max_x,max_y = find_peak(xs,ys,wavelength)

    #Get all the vertical lines
    for i in lines:
        ax.annotate("",(i,max_y + offset),(i,max_y + offset + length),textcoords="data",rotation="vertical",horizontalalignment="center",verticalalignment="bottom",arrowprops={"width":.1,"frac":1,"headwidth":.1})
    
    y_val = max_y + offset + length
    print y_val
    ax.annotate("",(lines[0],y_val),(lines[-1],y_val),xycoords="data",textcoords="data",rotation="horizontal",horizontalalignment="center",verticalalignment="bottom",arrowprops={"width":.1,"frac":1,"headwidth":.1})

    ag = np.mean(np.array(lines))
    ax.annotate(name,(ag,y_val),(ag + xoff,y_val + length + yoff),xycoords="data",textcoords="data",rotation="vertical",horizontalalignment="center",verticalalignment="bottom",arrowprops={"arrowstyle":"-",#"width":.1,"frac":1,"headwidth":.1,
        "connectionstyle":"bar,angle=180,fraction=-0.2"},size=10)

def synthesize_photometric_point(filt, wl, fl):
    '''Takes in a spectrum in [ang], and [erg/(s cm^2 ang)], and then returns Jy'''
    if filt in {"u","g","r","i","z"}:
        wl_key = "lam"
        p_key = "air1.0"
    else:
        wl_key = "WL"
        p_key = "RES"
    p = interp1d(photometry.responses[filt][wl_key],photometry.responses[filt][p_key])
    filt_re = photometry.responses[filt][wl_key]
    p_min = min(filt_re)
    p_max = max(filt_re)
    if p_min < wl[0] or p_max > wl[-1]:
        print "ERROR, spectrum is out of range of filter: %s" % filt
    def px(x):
        if (x < p_min) or (x > p_max):
            return 0
        else:
            return p(x)
    pxs = map(px, wl)
    f_num = wl * pxs * fl
    f_denom = wl * pxs
    #print f_num, f_denom
    num = simps(f_num, x=wl)
    denom = simps(f_denom, x=wl)
    flux = num/denom
    #This should be in spectral flux [erg/(s cm^2 A)]
    central = denom/simps(pxs, wl)
    #Returned product is in Jy  
    return photometry.Flamb_to_Jy(flux,central) 

def main():
    pass

if __name__ == "__main__":
    main()



