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
from multiprocessing import Process, Manager, Value



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

    monomers = []
    free_monomers = []
    stuck_monomers = []
    occuped_space = []
    islands = []
    visited_sites = []
    average_displacements = []
    a = []
    b = []
    c = []
    d = []
    ah = []
    k1 = []
    k2 = []
    k3 = []

    # Creating a progress bar
    pbar = progress.Bar(number_of_simulations, prefix="Bulk simulations")
    pbar(0)

    # Running several simulations
    for i in range(number_of_simulations):
        # Updating progress bar
        pbar(i+1)
        # print(i, end=", ")

        # Clearing the previous simulation data
        clear()
        
        # Running one simulation
        res = simulation.run(L, D1, F, N, steps, save = number_of_simulations == 1, verbose = number_of_simulations == 1, animate = i==0, parent_bar = pbar)
        monomers.append(res[1])
        free_monomers.append(res[2])
        stuck_monomers.append(res[3])
        occuped_space.append(res[4])
        islands.append(res[5])
        visited_sites.append(res[6])
        average_displacements.append(res[7])

        a.append(data.get_a_evolution())
        b.append(data.get_b_evolution())
        c.append(data.get_c_evolution())
        d.append(data.get_d_evolution())
        ah.append(data.get_ah_evolution())
        k1.append(data.get_k1_evolution())
        k2.append(data.get_k2_evolution())
        k3.append(data.get_k3_evolution())

        # Getting x axis data
        if mode == "density":
            by = array(mean(occuped_space, axis=0)) / (L**2)
        if mode == "iteration":
            by = arange(steps)

        # Plotting data for each simulation
        multiplot.record(
            L = L,
            by = by,
            by_name = mode,
            monomers = monomers[-1],
            free_monomers = free_monomers[-1],
            stuck_monomers = stuck_monomers[-1],
            occuped_space = occuped_space[-1],
            islands = islands[-1],
            visited_sites = visited_sites[-1],
            average_displacements = average_displacements[-1],
            a = a[-1],
            b = b[-1],
            c = c[-1],
            d = d[-1],
            ah = ah[-1],
            k1 = k1[-1],
            k2 = k2[-1],
            k3 = k3[-1],
            alpha = 0.01,
            simu = i+1 if number_of_simulations > 1 else i
        )

    # Plotting average of data
    multiplot.record(
        L = L,
        by = by,
        by_name = mode,
        monomers = mean(monomers, axis=0),
        free_monomers = mean(free_monomers, axis=0),
        stuck_monomers = mean(stuck_monomers, axis=0),
        occuped_space = mean(occuped_space, axis=0),
        islands = mean(islands, axis=0),
        visited_sites = mean(visited_sites, axis=0),
        average_displacements = mean(average_displacements, axis=0),
        a = mean(a, axis=0),
        b = mean(b, axis=0),
        c = mean(c, axis=0),
        d = mean(d, axis=0),
        ah = mean(ah, axis=0),
        k1 = mean(k1, axis=0),
        k2 = mean(k2, axis=0),
        k3 = mean(k3, axis=0),
        alpha = 1,
        simu = 0
    )
    
    multiplot.save(mode)
    multiplot.show()
