# -*- coding: utf-8 -*-

"""

The functions(s) that actually perform the random walk.

@author: David G. Khachatrian

"""

import random

def prob_path(data, agents, start_coords, start_angles, end_coord = None, num_steps = None):
    """
    Generator function to track the movement of agents along paths.
    
    Inputs:
    data = a 4D NumPy array with coordinates [z,y,x][d], where d determines what information about the pixel is received: orientation(0), coherence(1), and energy(2)
    num_agents = number of agents to walk along the model. Set to 1 -- no assumptions about interdependence between agents has yet been made.
    start_coords = a list of length (num_agents) describing the starting coordinates of the agents.
    start_angles = a list of length (num_agents) describing the initial trajectory angles (to the horizontal, with range [-pi,pi]) of the agents.
    end_coord = a desired end location for the agent. If this is specified, the number of iterations ('steps') it took to reach the end will be logged for each agent in a list.
    num_steps = the desired number of iterations, to obtain a spatial map of propbable locations.
    
    If both end_coord and num_steps are described, num_steps will take precedence -- the simulation will end after num_steps regardless of the locations of the agents.
    
    Yields:
    coords = current locations of the agents
    angles = the angle with respect to the horizontal of the agents' trajectories
    
    """
    
    
#    for each step toward num_step:
#        for each agent in agents:
#            get its current location and previous trajectory angle
#            get the orientation, energy, and coherence coresponding to the current location (from the data array)
#            
#            for each possible movement angle:
#                get the probability of moving to that location using prob_funcs.prob_function()
#                shove them all into a dict, mapping 'next location' --> 'probability weight'
#            
#            use random.choose(next location, probability weights) to choose where the agent moves
#            save new coord in a coords (list)
#            save angle of trajectory in a traj_angles (list)
#            
#        yield coords, traj_angles (can be used for visualization)