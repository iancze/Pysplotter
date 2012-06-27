'''Module contributed by Nathan Sanders, to use IRAF's task fitprofs to fit spectral line profiles.'''

#############################################################
########Setup the environment (don't need all of this just for fitprofs)
#############################################################

###Load packages
from pyraf import iraf
#from iraf import *
import os,glob,time,re,pickle,math,matplotlib,aplpy
from numpy import *
from scipy.optimize import leastsq,fsolve#,fmin_slsqp
from scipy.integrate import quad
from scipy.stats import *
from datetime import datetime, date, time
import matplotlib.pyplot as plt
from datetime import timedelta
from numpy.random import randint
import pyfits
iraf.tables()
iraf.noao()
iraf.imred()
iraf.twodspec()
iraf.onedspec()
iraf.ccdred()
iraf.apextract()
iraf.longslit()
iraf.plot()
iraf.stsdas()
iraf.nebular()
from time import strftime


#############################################################
########Setup a list of lines and fitting regions
#############################################################

#the list of lines
linenames=[3727,4102,4340,4363,4686,4861,4959,5007,5755,5876,6548,6562,6584,6717,6731]
elines=array([.5*(3727.092+3729.875),4102.89,4341.68,4364.436,4686,4862.68,4960.295,5008.240,5754.59,5876,6549.86,6564.61,6585.27,6718.29,6732.67])
#define a preferred background region width
bgsize=20
#define a perferred background region offset (should be larger than the expected line half-width)
bgoff=20
#the minimum offset between lines is then the sum of these, otherwise the lines are grouped
reqoff=2*bgoff+2*bgsize
#now group the lines if needed and decide what the fitting and background regions should be
glines={};gfitrs={};gbgrs={}
skip=0;gnum=-1 ##start gnum at 0 by adding +1...
for i in range(len(elines)):
    #were we instructed to skip a line?
    if skip>=1:
        skip=skip-1
        continue
    else:
        gnum=gnum+1
    #unless this is the last line, check if the next line is very close
    if ((i+1)<=len(elines)-1) and (elines[i+1]-elines[i]<=reqoff):
        #is it a triplet?
        if ((i+2)<=len(elines)-1) and (elines[i+2]-elines[i+1]<=reqoff):
            glines[gnum]=[elines[i],elines[i+1],elines[i+2]]
            gfitrs[gnum]=[(elines[i]-1*bgoff),(elines[i+2]+1*bgoff)]
            gbgrs[gnum]=[(elines[i]-1*bgoff-1*bgsize),(elines[i]-1*bgoff),(elines[i+2]+1*bgoff),(elines[i+2]+1*bgoff+1*bgsize)]            
            #skip the next one
            skip=2
        #or maybe just a doublet (don't even quant to think about quadruplets...
        else:
            glines[gnum]=[elines[i],elines[i+1]]
            gfitrs[gnum]=[(elines[i]-1*bgoff),(elines[i+1]+1*bgoff)]
            gbgrs[gnum]=[(elines[i]-1*bgoff-1*bgsize),(elines[i]-1*bgoff),(elines[i+1]+1*bgoff),(elines[i+1]+1*bgoff+1*bgsize)]
            #skip the next two
            skip=1
    #it's just a singlet...
    else:
        glines[gnum]=[elines[i]]
        gfitrs[gnum]=[(elines[i]-bgoff),(elines[i]+bgoff)]
        gbgrs[gnum]=[(elines[i]-bgoff-bgsize),(elines[i]-bgoff),(elines[i]+bgoff),(elines[i]+bgoff+bgsize)]












def dofitprofs(spectrum,specband,varband,redshift,outprefix,alreadyvar=0,startfwhm=4.5,fwhmlim=10,theconstant=10000):
    """
    Use IRAF's fitprofs to do spectral line fitting
    theconstant is added to the spectrum to prevent negative values that would confuse fitprofs (it should be larger than the most negative value in the spectrum)
    """
    outdic={}
    ##add a constant to the spectrum so that fitprofs won't be confused by negative values
    shiftspec='fitprofstempfile.fits';os.system('rm -f '+shiftspec)
    iraf.imarith(spectrum,'+',theconstant,shiftspec)
    for j in glines.keys():
        ##redshift the line centers and fitting regions
        zbgreg=array(gbgrs[j])*(1+redshift)
        zcenters=array(glines[j])*(1+redshift)
        ##create positions file
        os.system('rm -f fitprofs_positions.temp')
        for val in zcenters:
            os.system('echo '+str(val)+' INDEF INDEF '+str(startfwhm)+' >> fitprofs_positions.temp')
        ##load spectrum
        [waves,spec]=pygetspec(spectrum,specband-1)
        [waves,var]=pygetspec(spectrum,varband-1)
        if alreadyvar==0:
            var=var**2
        #find index numbers associated with the bg and fit region and center wavelengths
        bg1=0;bg2=0;bg3=0;bg4=0
        for i in range(len(waves)):
            if (waves[i]>=zbgreg[0]) and (bg1==0): bg1=i
            if (waves[i]>=zbgreg[1]) and (bg2==0): bg2=i
            if (waves[i]>=zbgreg[2]) and (bg3==0): bg3=i
            if (waves[i]>=zbgreg[3]) and (bg4==0): bg4=i
        ##get estimate of noise parameters
        x=append(spec[bg1:bg2],spec[bg3:bg4])+theconstant;y=append(var[bg1:bg2],var[bg3:bg4])+theconstant
        slope, intercept, r_value, p_value, std_err=linregress(x,y)
            #plt.plot(x,y,'o');plt.plot(x,x*slope+intercept);plt.show();pdb.set_trace()
        if intercept<0: intercept=0
        noisefloor=intercept+median(x)*slope
        ##get estimate of background level
        bglevel=median(x-theconstant);bgsigma=bglevel/std(x-theconstant)
        ##run fitprofs
        bgstring="med("+str(int(zbgreg[0]))+"-"+str(int(zbgreg[1]))+") med("+str(int(zbgreg[2]))+"-"+str(int(zbgreg[3]))+")"
        rgstring=str(int(zbgreg[1]))+' '+str(int(zbgreg[2]))
        flog=outprefix+'_fitprofs_log.temp';fplot=outprefix+'_fitprofs'+str(j)+'.gki';os.system('rm -f '+fplot)
        try:
            iraf.fitprofs(shiftspec,lines=specband,region=rgstring,positions='fitprofs_positions.temp',background=bgstring,profile='gaussian',gfwhm=4,fitbackground='yes',fitpositions='single',fitgfwhm='all',nerrsample=100,sigma0=intercept**.5,invgain=slope,logfile=flog,plotfile=fplot,verbose=0)
        except:
            print "Fitting failed for "+spectrum+", "+str(glines[j])
            os.system("echo '#fitprofs fitting failed' >> "+flog)
            for k in range(len(glines[j])):
                os.system("echo 'nan nan nan nan nan nan nan' >> "+flog)
        ##load results
        f=open(flog,'r');lst=f.readlines()
        for k in range(len(glines[j])):
            ##did the error calculation work?
            if '(' in lst[-1]:
                goback=2*(len(glines[j])-k-1);backstep=2
                ##errors
                scenter=float(lst[-1-goback].replace('(','').replace(')','').split()[0])
                sflux=float(lst[-1-goback].replace('(','').replace(')','').split()[2])
                sew=float(lst[-1-goback].replace('(','').replace(')','').replace('INDEF','nan').split()[3])*(1+theconstant/bglevel)  ##correct for theconstant
                sfwhm=float(lst[-1-goback].replace('(','').replace(')','').split()[5])
            else:
                goback=1*(len(glines[j])-k-1);backstep=1
                ##take the variance floor as the error
                scenter=nan
                sflux=noisefloor**.5*startfwhm
                sfwhm=nan
                sew=nan
            ##values
            center=float(lst[-backstep-goback].replace('(','').replace(')','').split()[0])
            flux=float(lst[-backstep-goback].replace('(','').replace(')','').split()[2])
            ew=float(lst[-backstep-goback].replace('(','').replace(')','').replace('INDEF','nan').split()[3])*(1+theconstant/bglevel)
            fwhm=float(lst[-backstep-goback].replace('(','').replace(')','').split()[5])
            ##reject negative fluxes
            ##reject objects with too-large FWHM
            if flux<0 or fwhm>fwhmlim:
                center=nan;flux=nan;fwhm=nan;sflux=nan;scenter=nan;sfwhm=nan
            ##If continuum was negligable (<2sigma), read out huge equivalent width
            if bgsigma<2:
                ew=-inf;sEW=-inf
            ##don't accept a flux error below the noise floor
            if sflux<noisefloor**.5*startfwhm: sflux=noisefloor**.5*startfwhm
            ##save to dictionary
            outdic[glines[j][k]]={'cent':center,'scent':scenter,'flux':flux,'sflux':sflux,'fwhm':fwhm,'sfwhm':sfwhm,'EW':ew,'sEW':sew}
    ###rename lines
    outdic2={}
    for i in range(len(elines)):
        outdic2[linenames[i]]=outdic[elines[i]]
    return outdic2







def pygetspec(spectrum,band=0,fixgap=1,ap=0,varband=-1):
    """
    A task to load a fits spectrum into a python array using pyfits
    wcs specification: http://iraf.noao.edu/projects/fitswcs/spec3d.html#2
    we assume a linearized spectrum
    
    Note: This task is designed to work with data where the dispersion axis is the final axis (i.e. as
    output by apall).  It will also read in one special case where there are two axes and the dispersion 
    axis is the first, but in that case will not trim based on variancr.
    
    * band: band of spectrum (starts at 0, ignored if single spectrum)
    * fixgap: (boolean) will replace any chipgaps (>20 angstrom jumps in the x-axis) with noise
    * ap: Aperture number
    * varband: band of variance spectrum; used to reject certain pixels (if set to varband>=0)

    """
    fixed=0
    ##open file
    f=pyfits.open(spectrum)
    theshape=shape(f[0].data)
    ##Which axis has the spectral data?
    saxis=argmax(theshape)
    if saxis==0: ##result of scopy
        specvec=f[0].data[:,band]
    else: #normal
        ##read in fluxes and pixels
        if len(theshape)==2:  #one aperture
            multi=0
            if theshape[0]==1: ##one band
                specvec=f[0].data[0,:]
            else: ##multibands
                specvec=f[0].data[band,:]
        elif len(theshape)==3: #multiple apertures
            multi=1
            if theshape[0]==1:  ##one band
                specvec=f[0].data[0,ap,:]        
            else: #multiple bands
                specvec=f[0].data[band,ap,:]             
        else: raise InputError('Format not recognized by pygetspec')    
        ###read in fluxes and pixels
        #if (band==-1):
            #specvec=f[0].data
        #else:
            #try:
                #specvec=f[0].data[band,0,:]
                #multi=1
            #except:
                #specvec=f[0].data[band,:]
                #multi=0
        ##remove this point if the variance spectrum is zero, otherwise the random number generator will complain
        if (varband>=0):
            if multi==0: notbad=where((f[0].data[varband])>=0)
            else: notbad=where((f[0].data[varband,ap])>=0)
            fixed=1
    ##wavelength solution
    pixels=linspace(1,len(specvec),len(specvec))
    ##read in wavelength calibration
    delta=f[0].header['CD1_1']
    refwave=f[0].header['CRVAL1']
    refpix=f[0].header['CRPIX1']
    offset=refwave-refpix*delta
    ##tranform pixel coordinate to wavelength
    wavevec=pixels*delta+offset
    ##apply bad pixel fix
    if fixed:
        wavevec=wavevec[notbad]
        specvec=specvec[notbad]
    ##Fix chipgap?
    if fixgap: [wavevec,specvec]=fixchipgap(wavevec,specvec)
    return wavevec,specvec


