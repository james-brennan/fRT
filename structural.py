#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
structural
"""
from utils import *
import numpy as np 
from optics import *
from structural import *
from modelGrid import *
from utils import *

class leaf(object):
    def __init__(self, normal_angle, u):
        self.LAD = normal_angle
        self.u = u # leaf density

    def hits_leaf(self, aray):
    	"""
    	Function which decides whether a ray
    	is likely to have been intercepted by a leaf 
    	this ofcourse depends upon it's direction relative
    	to Leaf angle and leaf area density

    	this is a model for the total extinction coefficient:
    		eg the probabilty that photon travelling along direction 
    			x interacts with a leaf

    	Need to define a geometry factor G(x)
    	assume that photons hits leaf if direction dot with leaf normal is small
    		-- because horizontal leaf angle is assumed to be isotropic
    			this is sampled each time


    	For now assume this is based on:
    		-- angle between leaf and ray dir less than 30°
    		-- modulated by area density

    	"""
    	raySpherical = cartToSph(aray.dir[0], aray.dir[1],aray.dir[2])
    	#import pdb; pdb.set_trace()
    	if abs(np.dot(raySpherical[1], np.radians(self.LAD))) > 0.1: # about 45 degrees
    		r = np.random.random()
    		if r < self.u:
    			return True # hits leaf 
    		else:
    			return False # misses leaf 