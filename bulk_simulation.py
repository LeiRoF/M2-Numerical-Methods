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
from multiprocessing import Pool, Process, Manager, Value
from time import time



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
    # Clearing the previous simulation data
    clear()

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

    start_time = time()

    parameters = [(
        mode,
        L,
        D1,
        F,
        N,
        steps,
        number_of_simulations == 1, # save
        number_of_simulations == 1, # verbose
        # pbar,
        # i==0, # animate
    ) for i in range(number_of_simulations)]

    bulk = Process(target=simulation.run, args=parameters)
    bulk.start()
    bulk.join()

    print(f"Bulk simulation time: {time() - start_time}s")
    print(bulk)

    # Creating a progress bar
    pbar = progress.Bar(number_of_simulations, prefix="Generating plots")
    pbar(0)

    # Running several simulations
    for i in range(number_of_simulations):
        # Updating progress bar
        pbar(i+1)
        # print(i, end=", ")

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
            monomers = res[i].monomers,
            free_monomers = res[i].free_monomers,
            stuck_monomers = res[i].stuck_monomers,
            occuped_space = res[i].occuped_space,
            islands = res[i].islands,
            visited_sites = res[i].visited_sites,
            average_displacements = res[i].average_displacements,
            a = res[i].a,
            b = res[i].b,
            c = res[i].c,
            d = res[i].d,
            ah = res[i].ah,
            k1 = res[i].k1,
            k2 = res[i].k2,
            k3 = res[i].k3,
            alpha = 0.01,
            simu = i+1 if number_of_simulations > 1 else i
        )

    # Plotting average of data
    multiplot.record(
        L = L,
        by = by,
        by_name = mode,
        monomers = mean([x.monomers for x in res], axis=0),
        free_monomers = mean([x.free_monomers for x in res], axis=0),
        stuck_monomers = mean([x.stuck_monomers for x in res], axis=0),
        occuped_space = mean([x.occuped_space for x in res], axis=0),
        islands = mean([x.islands for x in res], axis=0),
        visited_sites = mean([x.visited_sites for x in res], axis=0),
        average_displacements = mean([x.average_displacements for x in res], axis=0),
        a = mean([x.a for x in res], axis=0),
        b = mean([x.b for x in res], axis=0),
        c = mean([x.c for x in res], axis=0),
        d = mean([x.d for x in res], axis=0),
        ah = mean([x.ah for x in res], axis=0),
        k1 = mean([x.k1 for x in res], axis=0),
        k2 = mean([x.k2 for x in res], axis=0),
        k3 = mean([x.k3 for x in res], axis=0),
        alpha = 1,
        simu = 0
    )
    
    multiplot.save(mode)
    multiplot.show()
