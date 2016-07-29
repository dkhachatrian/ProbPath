# -*- coding: utf-8 -*-

"""

Visualizing functions for the model.

@author: David G. Khachatrian

"""

from lib import globe as g
from lib import helpers as h
from PIL import Image
from matplotlib import colorbar
from matplotlib import pyplot as plt
from matplotlib import pylab
from matplotlib import colors
import numpy as np
from collections import Counter

def place_agents_on_image(agents, image, color = 'yellow'):
    '''
    Create an image with agents represented as pixels of color (color) with intensity determined by relative number of agents at a particular coordinate. A colorbar to the right of the image will update to map number_of_agents-->color_intensity
    Images to be collated into an MPEG (using e.g. mencoder).
    '''
    
    im = prep_bg_image(image)
    loc_data = np.zeros(np.array(im).shape[:-1]) #-1 to remove the [RGB] axis    
    fig, ax = pylab.subplots()
    agent_im = Image.fromarray(loc_data)
    #overlay = overlay
    ax.imshow(overlay)

    while True:

        agent_im.set_data(prep_agents_im_data(agents,image,color))
        overlay.set_data(np_array) #overlay images
        plt.colorbar(mappable = agent_im) #create/update colorbar
        fig.canvas.draw() #update image
        # TODO: save image to a subdirectory, to be able to make movie
        # TODO: pause? depends on how fast the program actually runs...
        agents = yield #get new agents_data
        
        
    return
    
    #pass
    #pyplot.clf()
    #imshow(waoeignapowin)
    #colorbar()

def follow_agent_path_on_image(agent, image, color = 'yellow'):
    '''
    Follow a single agent on its random walk through the image space, denoting the path with color (color). Leaves a trace of subdued (color) when the agent moves from this position, which becomes slightly brighter as the agent visits that location more times.
    '''
    
    im = prep_bg_image(image)
    path_im_data = np.zeros(im.shape)
    
    # how to best leave trace? How to best visualize multiple visits to same pixel? 
    
    
    while True:
        
        pass
        # TODO: save image to a subdirectory, to be able to make movie
        # TODO: pause? depends on how fast the program actually runs...
    
    
#    
#    fig, ax = pylab.subplots()
#    im = ax.
    
    

    
    pass


def prep_bg_image(image, alpha = 0.3):
    '''
    Prepare original image, so that the agents' locations may be overlaid clearly on top in other images.
    "Preparation" entails making it grayscale, then turning the image into an RGBA image with the alpha-band equaling 'alpha' at every pixel.
    Returns an RGBA image.
    '''
    im = (image.convert('L')).convert('RGBA') #will plot agent's path on a grayscale version of the image
    r,g,b,a = im.split() # a will be all 255, i.e., fully opaque
    a = Image.fromarray(((np.array(a))*alpha).astype('uint8'))
    im = Image.merge(mode = 'RGBA', (r,g,b,a))
    return im
#    im = im.convert('RGB') #to overlay yellow



# pass in a coord2counts variable instead of agents? Generalize creation of agent overlay for both many_agents_at_once and follow_agent_path
def prep_agents_im_data(agents, image, color):
    '''
    Prepare image overlay for agents with color (passed in as an RGB tuple with ranges (0-1)).
    Does *not* create colorbar.
    Returns RGBA image (A = eye*255)
    '''
    
    #initialize values as the value of color...
    max_val = 255 #uint8
    im_data = np.zeros(image.convert('RGB').shape)
    
    color = colors.rgb_to_hsv(color)
    
    for i,x in enumerate(color):
        im_data[...,i].fill(x) #fill RGB data
    
    loc_data = np.zeros(image.convert('L').shape)
    
    # count will determine saturation (bright yellow ==> most agents, white ==> )
    counts = Counter((agent.coord for agent in agents))
    max_c = max(counts.values())
    #scalar = max_val/max(counts.values()) #scale factor for alpha channel
    for coord in counts:
        arr_coord = tuple(reversed(coord))
        loc_data[arr_coord] = counts[coord]/max_c #update array with locations
        
    im_data[1] = loc_data #set saturation channel
    
    im_data = (im_data*max_val).astype('uint8')
    im = Image.fromarray(im_data, mode = 'HSV')
    im = im.convert('RGB')
    return np.array(im)
    # TODO: ^is using PIL's Image.convert faster than manually converting back to RGB?
#    
#    
##    im = Image.fromarray((im_data*max_val).astype('uint8')) #now good as an image
#    return im
