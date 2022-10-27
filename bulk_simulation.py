from numpy import *
import matplotlib.pyplot as plt
from LRFutils import progress
from numba import njit
import simulation
import multiplot
from classes.layer import Layer
from classes.island import Island
from classes.monomer import Monomer
import data
import gc



# ________________________________________________________________________________
# Clear the previous simulation data

def clear():

    # Removing all objects of types Monomer, Island and Layer
    for obj in gc.get_objects():
        if isinstance(obj, Monomer) or isinstance(obj, Island) or isinstance(obj, Layer):
            del obj

    # Clearing the lists
    Island.all = []
    Monomer.all = []

    # Clearing the records
    data._record = []





# ________________________________________________________________________________
# Clear the previous simulation data

def run(mode, L, D1, F, N, steps, number_of_simulations):
    # Clearing plots
    multiplot.setup(F, D1, L, steps, number_of_simulations)

    # Creating a progress bar
    pbar = progress.Bar(number_of_simulations, prefix="Bulk simulations", average_ETA=number_of_simulations)
    pbar(0)

    # Running several simulations
    for i in range(number_of_simulations):
        # Updating progress bar
        pbar(i+1)
        # print(i, end=", ")

        # Clearing the previous simulation data
        clear()
        
        # Running one simulation
        evolution, monomers, free_monomers, stuck_monomers, occuped_space, islands, visited_sites, average_displacements = simulation.run(L, D1, F, N, steps, save = number_of_simulations == 1, verbose = number_of_simulations == 1, animation = i==0, parent_bar = pbar)

        # Getting x axis data
        if mode == "density":
            by = array(occuped_space) / (L**2)
        if mode == "iteration":
            by = arange(steps)

        # Plotting data
        multiplot.record(
            L = L,
            by = by,
            by_name = mode,
            monomers = monomers,
            free_monomers = free_monomers,
            stuck_monomers = stuck_monomers,
            occuped_space = occuped_space,
            islands = islands,
            visited_sites = visited_sites,
            average_displacements = average_displacements,
            alpha = 0.01,
            simu = i
        )
    
    multiplot.save(mode)
    multiplot.show()
