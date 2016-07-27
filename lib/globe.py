# -*- coding: utf-8 -*-

"""
Globals for ProbPath.

@author: David G. Khachatrian
"""


#### To ensure the working directory starts at where the script is located...
import os
abspath = os.path.abspath(__file__) #in lib directory
dname = os.path.dirname(os.path.dirname(abspath)) #twice to get path to main directory
dep = os.path.join(dname, 'dependencies')
os.chdir(dname)
####

import math

NUM_NEIGHBORS = 8

RIGHT = 0
UP_RIGHT = 1
UP = 2
UP_LEFT = 3
DOWN_RIGHT = -1
DOWN = -2
DOWN_LEFT = -3
LEFT = 4



out_dir = os.path.join(dname, 'outputs') #directory for output files
cache_dir = os.path.join(dname, 'cache')




