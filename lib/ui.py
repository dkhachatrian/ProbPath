# -*- coding: utf-8 -*-

"""

User-interface functions (using simple command-line inputs, i.e., input()). To ascertain which image to analyze, what the desired initial conditions are, etc.

@author: David G. Khachatrian
"""

import sys
from PIL import Image
import os
from lib import globe as g
import numpy as np
from lib import helpers as h


def get_image():
    """
    Prompts user for name of image, looking in the dependencies directory.
    """
    while True:
        try:
            file_name = input("Please state the name of the file corresponding to the data to be input, or enter nothing to quit: \n")
            if file_name == '':
                sys.exit()
            im = Image.open(os.path.join(g.dep, file_name))
            break
        except FileNotFoundError:
            print("File not found! Please check the spelling of the filename input, and ensure the filename extension is written as well.")
            continue
        except IOError: #file couldn't be read as an Image
            print("File could not be read as an image! Please ensure you are typing the filename of the original image..")
            continue
        
    
    return file_name, im


def choose_program_mode():
    """
    Chooses how this program will run. Details in print statements below.
    """
    
    print("Hello!")
    print("Please indicate your preference:")
    while True:
        print("To draw multiple paths with endpoint fixed, type '{0}'. You will then be asked to list the other desired coordinates.".format(g.MULTI))
        print("If you will indicate only one pair of coordinates, please type '{0}'.".format(g.SINGLE))
        resp = input("Please type your choice now:\n")
        
        if resp.lower() == 'm':
            return g.MULTI
        elif resp.lower() == 's':
            return g.SINGLE
        elif resp.lower() == 'q':
            sys.exit()
        else:
            print("Input not recognized! Please re-read the instructions and try again.")


def get_coords(mode):
    """ Ask for start and end coordinates. Ensure they're in the image size."""
    
#    # TODO: collapse things down -- too much repeated code between modes...
#    
#    start_coord = None
#    end_coords = [] #will either end up containing one or multiple elements depending on mode
##    if mode == g.SINGLE:
##        end_coord = None
##    elif mode == g.MULTI:
##        end_coords = []
##    
    coords = []
    
    while True:
        coord_ok = True
        #print("(Input 'q' to quit.)")
        print("Selected image's size is {0}.".format(g.orig_im.size))
        try:
            if len(coords) == 0:
                tup = input("Please input the desired start coordinate:\n")
            else:
                if mode == g.SINGLE:
                    if len(coords) == 2:
                        break
                    tup = input("Please input the desired end coordinate:\n")
                elif mode == g.MULTI:
                    print("You have currently input {0} end coordinate(s).".format(len(coords)-1))
                    tup = input("Please input a desired end coordinate. Type 'c' to finish input and continue.\n")
                    if tup == 'c':
                        break
            
            if tup == 'q':
                sys.exit()
            
            tup.strip('() ')
            nums = [int(x) for x in tup.split(',')]
        except ValueError:
            print('Error! Numbers not entered. Please try again.')
            continue
    
    
        if len(nums) != len(g.orig_im.size):
            print('Error! Input coordinates do not match image dimensions. Please try again.')
            continue
        for i,num in enumerate(nums):
            if num < 0 or num >= g.orig_im.size[i]:
                print('Error! Input values were out of image-size bounds! Image size bounds is {0}. Please try again.'.format(g.orig_im.size))
                coord_ok = False
                break
        if coord_ok:
            if len(nums) == 2:
                tup = (*nums, 0)
            elif len(nums) == 3:
                tup = tuple(nums)
            coords.append(tup)
    
    
    start_coord = coords.pop(0)
    end_coords = coords
    return start_coord, end_coords
    
    
    
def make_neighbor_ll(coord_list):
    """
    From a list of coordinates, return a list of a list of coordinates. Each list of coordinates contains a coordinate from coord_list and its valid neighbors (that remain within the bounds of the original image).
    """

    coord_ll = []

    for coord in coord_list:
        clist = G.generate_neighbor_coords(coord, *g.orig_im.size)
        clist.append(coord)
        coord_ll.append(clist)
    
    return coord_ll
    
    
    
    

def prompt_user_about_neighbors():
    """ Ask user whether to draw paths for neighbors as well as the indicated startpoint. """
    
    while True:
        resp = input("Would you like to draw paths for nearby startpoints as well? [Y/N]:\n")
        if resp.lower() == 'y':
            return True
        elif resp.lower() == 'n':
            return False
        else:
            print("Input not recognized! Please respond with either 'Y', 'y', 'N', or 'n'.")




def get_data():
    """
    Prompts user for names of files corresponding to outputs of OrientationJ's parameters: orientation, coherence, and energy.
    Input files are searched for in the script's dependencies folder.
    Input files must haev been saved as a Text Image using ImageJ.
    
    Returns a NumPy array of the data stacked such that the final axis has the data in order [orientation, coherence, energy].
    """

    data_names = ['orientation', 'coherence', 'energy']
    fnames = []
    data_list = []
    
    while len(fnames) < len(data_names):
        try:
            file_name = input("Please state the name of the file corresponding to the " + str(data_names[len(data_list)]) + " for the image of interest (saved as a Text Image from ImageJ), or enter nothing to quit: \n")
            with open(os.path.join(g.dep, file_name), 'r') as inf:
                d_layer = np.loadtxt(inf, delimiter = '\t')
            fnames.append(file_name)
            data_list.append(d_layer)
        except FileNotFoundError:
            print('File not found! Please ensure the name was spelled correctly and is in the dependencies directory.')
        except ValueError:
            print('File structure not recognized! Please ensure the file was spelled correctly and was saved as a Text Image in ImageJ.')
    
    data_shape = data_list[0].shape
    data_index = np.ndindex(data_shape)
    tupled_data = np.ndarray(data_shape).tolist()
    
    oris, cohs, eners = data_list
    
    for i in data_index:
        c_info = h.coord_info(coord=tuple(reversed(i)), orientation=oris[i], coherence=cohs[i], energy=eners[i])
        tupled_data[i] = c_info
        
    return tupled_data




#    print('Hello! Please place relevant files in the dependencies directory of this script. Please have the files saved as a "Text Image" in ImageJ.')
#    
#    data_list = []
#    data_names = ['orientation', 'coherence', 'energy']    
#
#
#    while len(data_list) < 3:
#        file_name = input("Please state the name of the file corresponding to the " + str(data_names[len(data_list)]) + " for the image of interest, or enter nothing to quit: \n")        
#        while not os.path.isfile(os.path.join(g.dep, file_name)):
#            if file_name == '':
#                sys.exit()
#            file_name = input("File not found! Please check the spelling of the filename input. Re-enter the name of the file corresponding to the " + str(data_names[len(data_list)]) + " for the image of interest (or enter nothing to quit): \n")
#        with open(os.path.join(g.dep, file_name), 'r') as inf:
#            d_layer = np.loadtxt(inf, delimiter = '\t')
#            #d_layer = np.around(d_layer, decimals = 3) #rarely are more than 3 decimal places needed -- just takes more time and space when left unrounded...
#            data_list.append(d_layer) #delimiter for Text Images is tab
#
#    #stack arrays
#
#    data = np.stack(data_list, axis = -1) #axis = -1 makes data the last dimension
#    np.around(data, decimals = 3, out = data)
#    
#    return data


def prompt_saving_paths():
    
    while True:
        tup = input("Would you like the individual paths to be saved separately? [Y/N]: \n")
        if tup.lower() == 'y':
            return True
        elif tup.lower() == 'n':
            return False
        else:
            print("Input not recognized! Please try again.")
