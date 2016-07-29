# -*- coding: utf-8 -*-

"""

The functions(s) that actually perform the random walk.

@author: David G. Khachatrian

"""

import numpy as np
from lib import helpers as h
from lib import prob_funcs as f

def prob_path(data, agent_ids, start_coords, start_angles, num_steps, end_coord = None):
    """
    Generator function to track the movement of agents along paths.
    
    Inputs:
    data = a 4D NumPy array with coordinates [z,y,x][d], where d determines what information about the pixel is received: orientation(0), coherence(1), and energy(2)
    agent_ids = number of agents to walk along the model. Set to [1] -- no assumptions about interdependence between agents has yet been made.
    start_coords = a list of length (num_agents) describing the starting coordinates of the agents.
    start_angles = a list of length (num_agents) describing the initial trajectory angles (to the horizontal, with range [-pi,pi]) of the agents.
    end_coord = a desired end location for the agent. If this is specified, the number of iterations ('steps') it took to reach the end will be logged for each agent in a list.
    num_steps = the desired number of iterations, to obtain a spatial map of propbable locations.
    
    If both end_coord and num_steps are described, num_steps will take precedence -- the simulation will end after num_steps regardless of the locations of the agents.
    
    Yields:
    coords = current locations of the agents
    angles = the angle with respect to the horizontal of the agents' trajectories
    
    """
    
    #initialization    
    agents = h.create_agent_dict(agent_ids = agent_ids, coords = start_coords, angles = start_angles)
    dims = tuple(reversed(data.shape[:-1]))
    
    for i in range(0, num_steps, 1):
        for agent in agents:
            poss_coords = h.get_neighbor_coords(coord = agent.coord, upper_bounds = dims)
            movement_angles = {}
            weights = []
            
            
            for poss_coord in poss_coords:
                i = tuple(reversed(poss_coord)) #array/list dimension ordering and Cartesian ordering are opposite
                theta = h.get_angle(origin = agent.coord, head = poss_coord, reference_vector = None)
                movement_angles[poss_coord] = theta
                theta_st, coh, ener = data[i].orientation, data[i].coherence, data[i].energy
                prob_for_theta = f.prob_function(theta_cur = theta, theta_past = agent.traj_angle, theta_st = theta_st, E = ener, C = coh)
                weights.append(prob_for_theta)
            
            next_coord = np.random.choice(poss_coords, p = weights)
            next_angle = movement_angles[next_coord]
            
            agent.coord, agent.traj_angle = next_coord, next_angle
            
        
        yield agents
            
    
    
#    for each step toward num_step:
#        for each agent in agents:
#            get its current location and previous trajectory angle
#            get the orientation, energy, and coherence coresponding to the current location (from the data array)
#            
#            for each possible movement angle:
#                get the probability of moving to that location using prob_funcs.prob_function()
#                shove them all into a dict, mapping 'next location' --> 'probability weight'
#            
#            use numpy.random.choose(next location, probability weights) to choose where the agent moves
#            save new coord in a coords (list)
#            save angle of trajectory in a traj_angles (list)
#            
#        yield coords, traj_angles (can be used for visualization)