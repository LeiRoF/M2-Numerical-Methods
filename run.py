# Import util modules
from numpy import *
import matplotlib.pyplot as plt
from LRFutils import progress
from LRFutils import archive
from numba import njit
import gc

# Import program classes
from classes.layer import Layer
from classes.island import Island
from classes.monomer import Monomer

# import program modules
import bulk_simulation
import animation
import data
import multiplot
from config import *

bulk_simulation.run(mode, L, D1, F, N, steps, number_of_simulations)