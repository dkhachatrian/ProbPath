# -*- coding: utf-8 -*-

"""
Smaller helper functions/tools used in other modules.

@author: David G. Khachatrian
"""

from collections import namedtuple
import math
from lib import globe as g
import numpy as np

agent_info = namedtuple('agent_info', ['coord', 'traj_angle'])
rel_coord = namedtuple('rel_coord', ['coord', 'rel_movement'])
coord_info = namedtuple('coord_info', ['coord', 'orientation','coherence','energy'])


def get_angle(origin, head, reference_vector = None):
    """ Get angle of vector created by (head-origin) with respect to the reference vector (defaulting to the horizontal if not supplied). """
    i_hat = [1,0,0]    
    
    u = reference_vector #shorter name...
    if u is None:
        u = i_hat
    u_hat = u / np.linalg.norm(u)
    
    v = np.subtract(head, origin)
    v_hat = v / np.linalg.norm(v)


    
    theta = np.arccos(np.dot(u_hat, v_hat)) #no need to divide by norms, as both norms are already 1
    
    return theta

#def get_angle(relative_movement):
#    """ Convert proposed movement to a trajectory angle. """
#    
#    return (2*math.pi/g.NUM_NEIGHBORS) * relative_movement
#    



def get_dtheta(theta1,theta2):
    """ Return the angle between the two angles, bounded by [-pi, pi]. For use in prob_funcs functions."""
    
    dtheta = theta2 - theta1
    
    if dtheta >= -math.pi and dtheta <= math.pi:
        return dtheta
    else:
        while dtheta > math.pi:
            dtheta -= (2*math.pi)
        while dtheta < math.pi:
            dtheta += (2*math.pi)
        
        return dtheta



def create_agent_dict(agent_ids, coords, angles):
    """ From the lists provided, create a mapping of Agent_ID --> namedtuple(coord, angle). """
    agents_dict = {}
    
#    if len(agents) != len(coords) or len(coords) != len(angles):
#        dosomething
    
    for i,x in agent_ids:
        agents_dict[x] = agent_info(coord = coords[i], traj_angle = angles[i])
    
    return agents_dict
        


def access_data(data, x, y, z = 0):
    """ Supplied an (x,y,z) coordinate of the image (0-indexed), returned the information in the 4D NumPy array corresponding to the expected pixel. """
    # arrays are index "outward-in", i.e., the x-coordinate is always the *last* element
    
    return data[z,y,x]




def get_neighbor_coords(coord, lower_bounds = (0,0,0), upper_bounds):
    """ From original tuple, generate nonegative-integer tuples from the center with bounds  [lower_bounds,upper_bounds). """
    delta = 1
    step = 1
    
    ords = []
    for ord, min_o, max_o in zip(coord, min_coord, max_coord):
        low = max(min_o, ord-delta)
        high = min(max_o-delta, ord+delta) #minus delta due to zero-indexing
        ords.append(list(range(low,high,step)))
    
    coords = [(x,y,z) for x in ords[0] for y in ords[1] for z in ords[2]]
    coords.remove(coord)
    
    return coords
    
    
    


#def generate_neighbor_coords(t, x_max, y_max, z_max = 1, discriminant_distance = 1.5):
#    """From original tuple, generate nonnegative-integer tuples within discrminant_distance of the center. Returns a list of such tuples."""
#    #default value of discriminant_distsance gives 8 nearest-neighbor pixels
#
#    dt = discriminant_distance #shorter name
#    
#
#    if len(t) == 3:
#        x,y,z = t
##        neighbors = [(i,j,k) for i in range(x - dt, x + dt) if lambda i: i >= 0 and i < x_max\
##                            for j in range(y-dt, y+dt) if j >= 0 and j < y_max\
##                            for k in range(z - dt, z + dt) if k >= 0 and k < z_max\
##                            if (i,j,k) != t\
##                            if sum((t-f)**2 for t,f in zip(t, (i,j,k))) < discriminant_dist**2\
##                            ]
#    
#    
#        # have to use several nested loops because parameters like x_max and y_max do not fall under the scope of list comprehensions when used in conditional statements
#        neighbors = []
#        for i in range(x-dt, x+dt):
#            if i >=0 and i < x_max:
#                for j in range(y-dt,y+dt):
#                    if j>=0 and j<y_max:
#                        for k in range(z-dt,z+dt):
#                            if k>=0 and k<z_max:
#                                cur = (i,j,k)
#                                if cur != t:
#                                    if (sum((to_-f)**2 for to_,f in zip(t,cur)))<dt**2:
#                                        neighbors.append(cur)
#                                elif cur == t:
#                                    pass
#        return neighbors
##    elif len(t) == 2:
##        x,y = t
##        neighbors = [(i,j,0) for i in range(x - dt, x + dt) if i >= 0 and i < x_max\
##                            for j in range(y-dt, y+dt) if j >= 0 and j < y_max\
##                            if (i,j) != t\
##                            if sum((t-f)**2 for t,f in zip(t, (i,j))) <=\
##                            discriminant_dist**2\
##                            ]
#    else:
#        print('Unexpected length of tuple for generate_neighbor_coords!')
#    
#    return neighbors
