#!/usr/bin/env python
#functions.py

'''This class will simply hold a bunch of generic functions which may need to be called by spectrum or photometry. Many of these can be used as line profiles.'''

import numpy as np

def gaussian(x, p):
    A = p[0]
    x0 = p[1]
    sigma = p[2]
    return A * np.exp(-(x - x0)**2 / (2 * sigma**2))

def gaussian_bkg(x, p):
    '''A gaussian on top of a linear background'''
    A = p[0]
    x0 = p[1]
    sigma = p[2]
    m = p[3]
    b = p[4]
    return A * np.exp(-(x - x0)**2 / (2 * sigma**2)) + line(x,p[3:5])

def line(x,p):
    m = p[0]
    b = p[1]
    return m*x + b
    
@np.vectorize
def boxcar(x,A=1,x0=0, w=1):
    '''This function would likely need to me mapped or vectorized'''
    if (x > x0 - w) and (x < x0 + w):
        return A
    else:
        return 0.