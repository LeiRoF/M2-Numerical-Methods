from numpy import *
seterr(all="ignore")
import matplotlib.pyplot as plt
from LRFutils import progress
from numba import njit
import simulation
import multiplot
from classes.layer import Layer
from classes.island import Island
from classes.monomer import Monomer
import data
from multiprocessing import Pool, Process, Manager, Value, cpu_count
from time import time
from config import *




# ________________________________________________________________________________
# Clear the previous simulation data

def run(mode, L, D1, F, N, steps, number_of_simulations):
    # Clearing plots
    multiplot.setup(F, D1, L, steps, number_of_simulations)

    cores = cpu_count()
    
    

    parameters = [(
        L,
        D1,
        F,
        N,
        steps,
        number_of_simulations == 1, # save
        number_of_simulations == 1, # verbose
        number_of_simulations == 1, # animate
    )]

    main_loops = parameters * cores
    last_loop = parameters * (number_of_simulations % cores)

    res = []
    
    pbar = progress.Bar(number_of_simulations, prefix=f"Runing simulations ({cores} by {cores})")
    pbar(0)

    for i in range(number_of_simulations // cores):
        with Pool(cores) as p:
            res += p.starmap(simulation.run, main_loops)
        pbar((i+1)*cores)
    
    if number_of_simulations % cores != 0:
        with Pool(number_of_simulations % cores) as p:
            res += p.starmap(simulation.run, last_loop)
        pbar(number_of_simulations)

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
            by = array(mean([x.occuped_space for x in res], axis=0)) / (L**2)
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
            alpha = max(0.01, 1/number_of_simulations),
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

if __name__ == "__main__":
    run("iteration", L, D1, F, N, steps, number_of_simulations)
