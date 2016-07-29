# -*- coding: utf-8 -*-

"""

The mathematical functions determining the probabilities used by the agent when performing the random walk.

@author: David G. Khachatrian

"""

import math
from lib import helpers as h
import numpy as np
import random

#
#def orientation_map(data):
#    """ From the 4D NumPy array (data) containing orientation data, create a map of parametrized functions corresponding to each pixel. Agents can then supply the variables needed to compute the probability distribution. """
#    
#    dim = data.shape[:-1] #dimensions of image
#    prob_map = (np.ones(dim)).tolist() #to hold function map
#    index = np.ndindex(dim)
#    
#    for ind in index: #loop to each 3D coordinate in the NumPy array
#        ori, ener, coh = data[ind]
#        ori_func_map = (prob_function, ori, ener, coh)
#        pass


def prob_function(theta_cur, theta_past, theta_st, E, C):
    """ Not normalized (which shouldn't be an issue when using random.choose)."""
    return orientation_function(traj_angle = theta_cur, theta_st = theta_st, E = E, C = C) * momentum_function(new_traj_angle = theta_cur, past_traj_angle = theta_past)


#def ori_func_map_parametrization(ori, ener, coher):
#    """ From the 4D NumPy array containing orientation data, """
#    return orientation_function(theta_ori = ori, E = ener, C = coher) * momentum_function
#    pass

def orientation_function(traj_angle, theta_st, E, C):
    """ st == 'structure tensor' """
    # follows expectations in anisotropy in that (E,C) ~ 0 ==> probability is uniform; (E,C) high ==> probability is highest and more pronounced where traj_angle == theta_st
    return math.exp(-(E*C*(traj_angle-theta_st))**2)
    # Gaussian with expontent (E*C*(traj_angle-theta_ori))**2
    
def momentum_function(new_traj_angle, past_traj_angle):
    """
    new_traj_angle = the proposed angle along which the agent would move
    past_traj_angle = the angle along which the agent moved on the previous iteration
    """
    return math.exp(-(new_traj_angle-past_traj_angle)**2)


def will_move(cur_info, neighbors_info):
    """
    Probabilistically determine whether an agent will move from the coord corresponding to cur_info, based on cur_info and neighbors_info
    """
    #will just do it by energy values
    
    cur_e = cur_info.energy
    neighbors_e = sum(n.energy for n in neighbors_info)
    
    p_move = neighbors_e / (cur_e + neighbors_e)
    
    rand = random.random()
    
    return (rand < p_move)
    