# -*- coding: utf-8 -*-

"""

Visualizing functions for the model.

@author: David G. Khachatrian

"""

from lib import globe as g
from lib import helpers as h
from PIL import Image
from matplotlib import colorbar

def place_agents_on_image(agents, image, color = 'yellow'):
    '''
    Create an image with agents represented as pixels of color (color) with intensity determined by relative number of agents at a particular coordinate. A colorbar to the right of the image will update to map number_of_agents-->color_intensity
    Images to be collated into an MPEG (using e.g. mencoder).
    '''
    
    pass
    #pyplot.clf()
    #imshow(waoeignapowin)
    #colorbar()

def follow_agent_path_on_image(agent, image, color = 'yellow'):
    '''
    Follow a single agent on its random walk through the image space, denoting the path with color (color). Leaves a trace of subdued (color) when the agent moves from this position, which becomes slightly brighter as the agent visits that location more times.
    '''
    pass