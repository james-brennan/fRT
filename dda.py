#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
DDA stuff
"""
from numba import autojit
import numpy as np 
from optics import *
from structural import *
from modelGrid import *
from utils import *

"""
    DDA stuff
"""
@autojit
def __traversal_initialise(aray):
    """
    Calculate distances to axis boundaries and direction of discrete DDA steps
    """
    coords = aray.pos.copy() # starting location
    deltaDistance = np.zeros(3)
    nextT = np.zeros(3)
    step = np.zeros(3, dtype=int)
    # loop over 3 dimensions
    for i in xrange(3):
        """
        Check direction vector is not exactly zero for a dimension
        """
        if aray.dir[i] == 0.0:
            # set to float min
            aray.dir[i] = 1e-10

        x = (aray.dir[0] / aray.dir[i])
        y = (aray.dir[1] / aray.dir[i])
        z = (aray.dir[2] / aray.dir[i])
        # set deltaDistance
        deltaDistance[i] = np.sqrt((x**2 + y**2 + z**2))
        if aray.dir[i] < 0.0:
            # negative direction
            step[i] = -1
            nextT[i] = (aray.pos[i] - coords[i]) * deltaDistance[i]
        else:
            # is positive direction in this basis axis
            step[i] = 1
            nextT[i] = (coords[i] + (1.0 - aray.pos[i])) * deltaDistance[i];
    return coords, deltaDistance, nextT, step



@autojit
def DDA_traversal(aray, grid,scatteringBox,soilSpect, AABA_system, the_leaf):

    """
    Run traversal initialiser
    """
    coords, deltaDistance, nextT, step = __traversal_initialise(aray)
    """
    Now actual traversal
    """
    while True:
        side = 0
        for i in xrange(3):
            if nextT[side] > nextT[i]:
                # this is the maximum movement direction (either x,y or z)
                side = i
        #import pdb; pdb.set_trace()
        # update location to here
        nextT[side] += deltaDistance[side]
        coords[side] += step[side]
        #print coords
        #print step
        """
        Check if out of bounds

        Special for soil eg [2] == 0
        """
        #import pdb; pdb.set_trace()
        if coords[2] < 0:
            """
            Hit soil interface
            Do soil scattering
            """
            # re-direct ray back upwards
            # need to re-run above above
            #print 'soil'
            soilInteraction(aray, soilSpect)
            """
            Do some soil effect?

            NEED to also do something when ray exits sides of the box
            --- keep or not?
            """
        if (coords[side] < 0 or coords[side] >= AABA_system.maxs[side]):   
          break
        else:
            """
            Where the recursive shading occurs:
            split into a direct then Calculate a diffuse as well?

            """
            # for now just save visit into grid?
            #import pdb; pdb.set_trace()
            grid[coords[0], coords[1], coords[2]] +=1
            # interact with box contents
            if the_leaf.hits_leaf(aray):
            	"""
            	Ray intercepted leaf
            	"""
            	scatteringBox.interaction(aray, the_leaf)
    return None

