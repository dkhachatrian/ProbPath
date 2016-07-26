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

#RIGHT = 0
#UPPER_RIGHT = 1
#UP = 2



out_dir = os.path.join(dname, 'outputs') #directory for output files
cache_dir = os.path.join(dname, 'cache')




