#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    A simple 2d python ray tracer built with a DDA approach


Approach:
    1. Do diffuse   initial condition
    2. Do direct illumination
    3. Calculate upward hemispherical reflectance for traces


"""

# import model
from optics import *
from structural import *
from modelGrid import *
from utils import *
from dda import *

import numpy as np 
#import matplotlib.pyplot as plt


def run():
    rays = []
    maxs=25
    bounding = AABA(xmin=0, ymin=0, zmin=0, xmax=maxs, ymax=maxs, zmax=maxs,)
    gridd = np.zeros((maxs,maxs,maxs))
    # spectrum for red to nir leaves
    red_nir_leaves = spectrum(np.array([0.5, 0.85]), np.array([0.1, 0.6]), np.array([0.5, 0.1]))
    # spectrum for soil
    red_nir_soil = spectrum(np.array([0.5, 0.85]), np.array([0.3, 0.4]), np.array([0.0, 0.0]))


    # scattering setup
    scatt = BRDSF(red_nir_leaves, 0.0)
    lf = leaf(55.0, 0.8) # leaf angle distribution and leaf area density
    """
    Do over grid
    """
    for x in xrange(maxs):
        for y in xrange(maxs):
            for i in xrange(50):
                print (x,y)
                r = ray(np.array([x,y,maxs-1]), np.array([1.0,0.0, -1.0]),
                        np.array([1.0, 1.0]))
                r.dir /= np.linalg.norm(r.dir)
                DDA_traversal(r,gridd, scatt, red_nir_soil, bounding, lf)
                rays.append(r)
    return gridd, rays


def prun(x,y, maxs, gridd, scatt, red_nir_soil, bounding, lf):
    rays = []
    for i in xrange(50):
        print (x,y)
        r = ray(np.array([x,y,maxs-1]), np.array([1.0,0.0, -1.0]),
                np.array([1.0, 1.0]))
        r.dir /= np.linalg.norm(r.dir)
        DDA_traversal(r,gridd, scatt, red_nir_soil, bounding, lf)
        rays.append(r)
    return rays




def parallel_run():
    """
    Start parallel engines to run
    """
    from IPython.parallel import Client

    c = Client()   # here is where the client establishes the connection
    lv = c.load_balanced_view()   # this object represents the engines (workers)


    rays = []
    maxs=25
    bounding = AABA(xmin=0, ymin=0, zmin=0, xmax=maxs, ymax=maxs, zmax=maxs,)
    gridd = np.zeros((maxs,maxs,maxs))
    # spectrum for red to nir leaves
    red_nir_leaves = spectrum(np.array([0.5, 0.85]), np.array([0.1, 0.6]), np.array([0.5, 0.1]))
    # spectrum for soil
    red_nir_soil = spectrum(np.array([0.5, 0.85]), np.array([0.3, 0.4]), np.array([0.0, 0.0]))


    # scattering setup
    scatt = BRDSF(red_nir_leaves, 0.0)
    lf = leaf(55.0, 0.8) # leaf angle distribution and leaf area density


    tasks = []
    for x in xrange(maxs):
        for y in xrange(maxs):
            tasks.append(lv.apply(prun, x,y, maxs, gridd, scatt, red_nir_soil, bounding, lf))

    result = [task.get() for task in tasks]  # blocks until all results are back

    return results




import pylab as plt

#gri = run()
pgri = parallel_run()
plt.imshow(gri[0].sum(axis=2)); plt.show()





def do_diffuse_prior():
    pass

def direct(sun_pos, grid):
    """
    Fire collimated rays from sun location into scene 
    Sample across whole grid
    """

    # for each pixel at top of grid pass sun rays in
    for i in xrange(grid.gr.shape[0]):
        """
        Make an array starting at loc
        """
        xpos = i * grid.xres
        ypos = grid.zres * grid.zsize
        pos = np.array(xpos, ypos)
        direction = pos - sun_pos / np.norm(pos - sun_pos) # this location minus 
        r = ray(pos, direction)
        """
        The ray now travels down through the canopy being
        altered by transmission and reflectance

        amount of scattering vs absorption is determined by leaf area density

        """


import pdb; pdb.set_trace()

"""
See how the ray spectrum relates to leaf spectrum
"""
abss = gri[1][0].absorption_counts / gri[1][0].iOrders
scatss = gri[1][0].scattering_counts / gri[1][0].iOrders

absor = abss * np.ones((2))
scater = scatss *  np.ones((2))

"""
plot all ray scattering at NIR
"""

NIR_scat = [ gr.scattering_counts['leaf'][1] / gr.iOrders['leaf'] for gr in gri[1]  ]
NIR_scat = np.array(NIR_scat)


plt.scatter(phis, thetas, c=lorders)

locs = [gr.pos for gr in gri[1]]
dirs = np.array([gr.dir for gr in gri[1]])

thetas = np.array([cartToSph(dir[0], dir[1], dir[2])[1] for dir in dirs])
phis = np.array([cartToSph(dir[0], dir[1], dir[2])[2] for dir in dirs])

import pdb; pdb.set_trace()

sorders = [g.iOrders['soil'] for g in gri[1] ]
lorders = [g.iOrders['leaf'] for g in gri[1] ]

