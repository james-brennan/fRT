#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
modelGrids.py
"""
import numpy as np 

def make_grids(xsize=200, zsize=200, xres=1, yres=1):
    """
    """
    radField = np.zeros((xsize, zsize))
    u =  np.ones((xsize, zsize)) # leaf area density
    #u[:, ] *= 
    return radField, u


from numba import jit


class grid(object):
    def __init__(self, gr, xres=1, zres=1):
        self.gr = gr 
        self.xres = xres
        self.zres = zres
        self.xszie = gr.shape[0]
        self.zsize = gr.shape[1]

class AABA(object):
    def __init__(self, xmin=0, ymin=0, zmin=0, xmax=10, ymax=10, zmax=10, xres=1, yres=1, zres=1):
        """
        Construct AABA volumes
        """
        self.mins = np.array([xmin, ymin, zmin])
        self.maxs = np.array([xmax, ymax, zmax])
        self.resolution = np.array([xres, yres, zres])


