# -*- coding: utf-8 -*-

"""
Smaller helper functions/tools used in other modules.

@author: David G. Khachatrian
"""


def access_data(data, x, y, z = 0):
    """ Supplied an (x,y,z) coordinate of the image (0-indexed), returned the information in the 4D NumPy array corresponding to the expected pixel. """
    # arrays are index "outward-in", i.e., the x-coordinate is always the *last* element
    
    return data[z,y,x]







def generate_neighbor_coords(t, x_max, y_max, z_max = 1, discriminant_distance = 1):
    """From original tuple, generate nonnegative-integer tuples within discrminant_dist of the center. Returns a list of such tuples."""

    dt = discriminant_distance #shorter name
    

    if len(t) == 3:
        x,y,z = t
#        neighbors = [(i,j,k) for i in range(x - dt, x + dt) if lambda i: i >= 0 and i < x_max\
#                            for j in range(y-dt, y+dt) if j >= 0 and j < y_max\
#                            for k in range(z - dt, z + dt) if k >= 0 and k < z_max\
#                            if (i,j,k) != t\
#                            if sum((t-f)**2 for t,f in zip(t, (i,j,k))) < discriminant_dist**2\
#                            ]
    
    
        # have to use several nested loops because parameters like x_max and y_max do not fall under the scope of list comprehensions when used in conditional statements
        neighbors = []
        for i in range(x-dt, x+dt):
            if i >=0 and i < x_max:
                for j in range(y-dt,y+dt):
                    if j>=0 and j<y_max:
                        for k in range(z-dt,z+dt):
                            if k>=0 and k<z_max:
                                cur = (i,j,k)
                                if cur != t:
                                    if (sum((to_-f)**2 for to_,f in zip(t,cur)))<dt**2:
                                        neighbors.append(cur)
                                elif cur == t:
                                    pass
        return neighbors
#    elif len(t) == 2:
#        x,y = t
#        neighbors = [(i,j,0) for i in range(x - dt, x + dt) if i >= 0 and i < x_max\
#                            for j in range(y-dt, y+dt) if j >= 0 and j < y_max\
#                            if (i,j) != t\
#                            if sum((t-f)**2 for t,f in zip(t, (i,j))) <=\
#                            discriminant_dist**2\
#                            ]
    else:
        print('Unexpected length of tuple for generate_neighbor_coords!')
    
    return neighbors
