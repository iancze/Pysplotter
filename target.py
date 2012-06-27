'''Target Class. Defined for each object we want to work with. Will hold all the general properties of the object'''

class Target(object):
    def __init__(self,name,z=0.0):
        self.name = name
        self.z = z
        self.spectra = []
        self.lightcurves = []

    def set_z(self,z):
        self.z = z
        self.update_spectra_to_z()
        print("Updating all the spectra")

    def add_spectrum(self,spectrum):
        spectrum.set_parent(self)
        self.spectra.append(spectrum)
        return spectrum

    def add_lightcurve(self,lightcurve):
        lightcurve.set_parent(self)
        self.lightcurves.append(lightcurve)
        
    def update_spectra_to_z(self):
        for i in self.spectra:
            i.update_z()