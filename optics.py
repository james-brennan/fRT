#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
optics.py
"""
import numpy as np 
from utils import *
from structural import *
from modelGrid import *
from utils import *

class ray(object):
    def __init__(self, pos, direction, spectrum, repeats=10):
        """
        Model for ray is based on spectrum
        and absorption and scattering counts
        which will give the final spectrum of the ray

        """
        self.pos = pos
        self.dir = direction
        self.cell = np.array([0,0])
        self.cells = [] # store all visited cells -- why not?
        self.spectrum = spectrum
        """
        This is the crucial info part which provides counts of
        scattering which is used to chance spectrum to final spectrum
        This gets filled with each successive spectrum
        """
        self.absorption_counts = {"leaf": np.zeros_like(spectrum), 
        						  "soil": np.zeros_like(spectrum) }
        self.scattering_counts = {"leaf": np.zeros_like(spectrum), 
        						  "soil": np.zeros_like(spectrum) }
        self.iOrders = {"leaf": 0, 
        				"soil": 1 }
"""
Soil model
"""
def soilInteraction(ray, soilSpectrum):
	"""
	Soil is assumed lambertian
	"""
	if ray.iOrders['soil'] < 100:
	    # 1. choose random numbers
	    r = np.random.random(soilSpectrum.scattering.shape[0])
	    # at each wavelength decide is scattering or absorption 
	    # based on whether the random number exceeds absorption
	    absorbed = r < (1 - soilSpectrum.scattering)
	    """
	    Make at these locations contribution zero: photons absorbed
	    """
	    ray.absorption_counts['soil'] +=  absorbed
	    ray.scattering_counts['soil'] +=  ~absorbed
	    ray.iOrders['soil'] += 1 # increment counter

	"""
	Fire ray back up from soil
	"""
	theta = np.random.uniform(0, np.pi)
	phi = np.random.uniform(0, 2*np.pi)
	xyz = sphToCar(1.0, theta, phi)
	ray.dir = xyz
	ray.pos[2] = 1 # move out of ground
	return None


class BRDSF(object):
    """
    upper and lower hemispherical scattering
    function
    Assumed for leaves -- soil is only upwards

    Provide normalised reflectance distribution
    function with angle for upper and lower hemispheres

    Then provide a foward/backward scattering coeffiencet

    Asborption is then (1 - scat)

    The distribution is sampled from to choose direction
    of ray

    """
    def __init__(self, spectrum, angular_effect):
        """
        We are assuming that scattering is lambertian
        so actually no angular effect
        """
        self.spectrum = spectrum

    def interaction(self, ray, leaf):
        """
        The crucial part of whole algorithm:

        Probability of interaction with leaf 
        is dependent upon the leaf density along
        the direction of the ray

        Define what happens to a ray which reaches
        the leaf: options of course are:

        1. absorption
        2. scattering
            1. forward
            2. backward

        I use a random number generator to
        choose if absorption or scattering

        Then also whether forward or backward

        Then sample from BRDSF to choose direction that ray
        leaves the leaf

        """
        if ray.iOrders['leaf'] < 100:
            # 1. choose random numbers
            r = np.random.random(self.spectrum.scattering.shape[0])
            # at each wavelength decide is scattering or absorption 
            # based on whether the random number exceeds absorption
            absorbed = r < (1 - self.spectrum.scattering)
            """
            Make at these locations contribution zero: photons absorbed
            """
            ray.absorption_counts['leaf'] +=  absorbed
            ray.scattering_counts['leaf'] +=  ~absorbed
            ray.iOrders['leaf'] += 1 # increment counter
            """
            Now assume that the ray is also scattered
            We've recorded the truth but we may as well
            continue up to interactionOrder maxmimum
            """
            lad = np.radians(leaf.LAD)
            # need hemisphere around lad in direction of ray-dir
            # convert ray dir to spherical
            raySpherical = cartToSph(ray.dir[0], ray.dir[1],ray.dir[2])
            """
            Need to set up whether upper or lower hemisphere
            """
            hemi = np.argmin( [ abs(lad-raySpherical[2]) ,   abs((lad-np.pi)-raySpherical[2]) ] )
            if hemi == 0:
                """
                upper hemisphere
                1. So direction for the ray must be in an 
                upward hemisphere around lad
                phi is assumed isotropic as surfaces are lambertian
                """
                theta = np.random.uniform( lad - 0.5*np.pi, lad + 0.5*np.pi )
                phi = np.random.uniform(0, 2*np.pi)
            else:
                """
                Lower hemisphere
                1. So direction for the ray must be in an 
                downward hemisphere around (lad-pi) -- underside of leaf
                """
                theta = np.random.uniform( (lad-np.pi) - 0.5*np.pi, (lad-np.pi) + 0.5*np.pi )
                phi = np.random.uniform(0, 2*np.pi)
            """
            Convert back to cartesian and use as ray new direction
            """
            xyz = sphToCar(1.0, theta, phi)
            ray.dir = xyz
            return None


class spectrum(object):
    def __init__(self,wavelength, scattering, forward_ratio):
        self.wavelength = wavelength
        self.scattering = scattering
        self.forward_ratio = forward_ratio
        self.absorption = (1 - scattering)

