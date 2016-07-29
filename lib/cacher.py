# -*- coding: utf-8 -*-

"""

Will save/load variables to/from the 'cache' directory. File-naming conventions for these cached files are in the functions themselves.

@author: David G. Khachatrian
"""

import os
from lib import globe as g
import pickle


fname2var = {} #dictionary containing filenames --> variable names (all originally set to None). If load_cache finds it, it loads the file into the variable through fname2var

def load_cache(fname):
    """ Checks cache direcctory to see if the cached pickle file is there. If so, loads it into the appropriate variable in fname2var. """
    
    if fname in fname2var and fname in os.listdir(g.cache_dir):
        with open(os.path.join(g.cache_dir, fname), mode = 'rb') as inf:
            fname2var[fname] = pickle.load(inf)


def save_to_cache(var, fname):
    """ Saves var into a file named name in the cache directory. """
    with open(os.path.join(g.cache_dir, fname), mode = 'wb') as inf:
        pickle.dump(var, inf, pickle.HIGHEST_PROTOCOL)