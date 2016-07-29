# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 09:27:35 2016

A function-weighted probabilistic pathfinding model of some agent, with a user interface to feed in images, a startpoint, original trajectories, and desired endpoints whose paths should be traced (if applicable). The function depends on data derived from the input image of interest.

In this case, the model describes the movement of neural stem cells (NSCs) along brain tissue. The weighting function is determined by information regarding the anisotropy at a pixel in the image, as derived from structure tensor analysis [cite]. Structure tensors have been shown to have a strong correlation with the diffusion tensor (R**2 = ~0.9) [cite], which has clinical signficance, as the diffusion tensor can be obtained non-invasively using diffusion-tensor (DT) magnetic resonance imaging (MRI), a modality of MRI focused on the diffusion of water molecules in the brain.
A momentum function is also considered as a factor, assuming the agent has some inertia that overcomes diffusive tendencies. This is not an unreasonable assumption for agents at the size of cells, whose diffusivity in water could be estimated as D_cell_in_water \approx 10^(-12) cm2/s \approx 0.000009 mm2/day (assuming D ~ R (from D = 6*pi*eta*R_ion), and knowing that D_protein_in_water \approx 10^(-9) cm2/s). Taking into account the much larger mass, it is unlikely that momentum effects can be ignored.

The weighted random-walk model is, however, fairly adaptable, simply by altering the weighting function and the momentum function. By introducing further terms, such as a taxis term toward some point (or points), the random-walk can be more biased to end at a certain location.

The current implementation assumes that orientations, coherencies, and energies are passed in (as described in the ui functions), as opposed to the original (structure) tensors themselves.

@author: David G. Khachatrian
"""

#### To ensure the working directory starts at where the script is located...
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
dep = os.path.join(dname, 'dependencies')
os.chdir(dname)
####

from lib import ui
from lib import globe as g
from lib import prob_funcs as f
import prob_path as p
from lib import visualizer as v
from PIL import Image
from lib import helpers as h

# create directories if necessary

if not os.path.isdir(g.outdir):
    os.mkdir(g.outdir)

if not os.path.isdir(g.cache_dir):
    os.mkdir(g.cache_dir)
    
    
# get variables...

#### image
#im_name, im = ui.get_image()
im_name = 'test.jpg'
im = Image.open(os.path.join(g.dep, im_name))

### agents
agent_nums, start_coords, start_angles = ui.get_agent_info()
agents = h.create_agent_dict(num_agents = agent_nums, coords = start_coords, angles = start_angles)

### data
tupled_data = ui.get_data()

### num_iterations
num_steps = ui.get_iteration_number()


### follow one agent, or look at all agents?
visualizer_flag = g.SHOW_ALL

if visualizer_flag == g.FOLLOW_ONE:
    follow_agent_id = 0

    
agents_generator = p.prob_path(data = tupled_data, agents = agents, num_steps = num_steps)

if visualizer_flag == g.FOLLOW_ONE:
    follow_one_gen = v.follow_agent_path_on_image(agents[follow_agent_id], im)
    visual_generator = follow_one_gen
elif visualizer_flag == g.SHOW_ALL:
    visual_many_agents_gen = v.place_agents_on_image(agents, im)
    visual_generator = visual_many_agents_gen    
    




agents_generator.send(None)
visual_generator.send(None) #shows inital conditions


while True:
    try:
        agents = agents_generator.send(agents) #keep updating agents
        # create image to visualize locations of agents. Keep
        # show image to user
        # save image into a subdirectory of the outputs folder
    except StopIteration:
        pass # closing out of program...
    
    # TODO: can probably clean this up by changing input parameters of v.follow_agent_path_on_image ...
    if visualizer_flag == g.SHOW_ALL:
        try:
            visual_generator.send(agents)
        except StopIteration:
            pass
    elif visualizer_flag == g.FOLLOW_ALL:
        try:
            visual_generator.send(agents[follow_agent_id])
        except StopIteration:
            pass
