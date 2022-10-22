from numpy import *
import matplotlib.pyplot as plt
from LRFutils import progress
from numba import njit
import simulation
from config import *
import multiplot
import os
import numpy as np

def run(mode):
    fig = plt.figure(figsize=(15, 10))

    pbar = progress.Bar(number_of_simulations, "Running simulations")

    for i in range(number_of_simulations):
        
        
        evolution, monomers, free_monomers, stuck_monomers, occuped_space, islands, visited_sites, average_displacements = simulation.run(save = number_of_simulations == 1, verbose = number_of_simulations == 1, parent_bar = pbar)

        if mode == "density":
            by = array(occuped_space) / (L**2)
        if mode == "iteration":
            by = arange(steps)

        multiplot.record(
            fig = fig,
            L = L,
            by = by,
            ab_name = "Iteration",
            monomers = monomers,
            free_monomers = free_monomers,
            stuck_monomers = stuck_monomers,
            occuped_space = occuped_space,
            islands = islands,
            visited_sites = visited_sites,
            average_displacements = average_displacements,
            alpha = 0.1
        )

    pbar(i+1)

    for i, ax in enumerate(multiplot.axes):
        ax.grid()
        # ax.legend()
        if mode == "density": ax.set_xlabel("Density")
        if mode == "iteration": ax.set_xlabel("Iteration")
        if i in [0, 1, 3]:
            ax.set_ylabel("Count")
        for i in [2, 4, 5]:
            ax.set_ylabel("Ratio")

    fig.savefig(f"{mode}.png", facecolor='white')
    plt.close()