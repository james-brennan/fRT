#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
utils.py
"""
import numpy as np 
import math

"""
Coordinates utility functions
"""
def cartToSph(x,y,z):
    r = math.sqrt(x**2 + y**2 + z**2)
    phi = math.atan(y/x)
    theta = math.atan(z/math.sqrt(x**2+y**2))
    return np.array([r, theta, phi])


def sphToCar(r, theta, phi):
    x = r*math.cos(phi)*math.cos(theta)
    y = r*math.sin(phi)*math.cos(theta)
    z = r*math.sin(theta)
    return np.array([x,y,z])

