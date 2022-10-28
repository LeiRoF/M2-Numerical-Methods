# Import util modules
from numpy import *
from LRFutils import progress
from LRFutils import archive
from numba import njit
import os
import json
import matplotlib.pyplot as plt

# Import program classes
from classes.layer import Layer
from classes.island import Island
from classes.monomer import Monomer

# import program modules
import simulation
import data
import animation



# ________________________________________________________________________________
# Run a step of the simulation

def run_step(layer, F, D1):
    L = layer.L

    # Incoming flux
    for y in range(layer.L):
        for x in range(layer.L):
            if random.random() < F/D1 / layer.L**2:
                Monomer(layer, x=x, y=y)

    # Move monomers
    for monomer in layer.monomers():
        monomer.move()

    # Return the new state of the layer as a matrix with 1 if there is a monomer, 0 otherwise
    return layer.heightmap()



# ________________________________________________________________________________
# Run an entire simulation

def run(L, D1, F, N, steps, save = False, verbose = True, animate= True, parent_bar = None):

    layer = Layer(L)
    evolution = []
    monomers = []
    free_monomers = []
    stuck_monomers = []
    occuped_space = []
    islands = []
    visited_sites = []
    stepline = arange(0,steps)
    already_islanded = []
    average_displacements = []

    # Base monomers (N monomers present at the begining of the simulation)
    for _ in range(N):
        Monomer(layer)

    # Generating evolution
    if verbose:
        pbar = progress.Bar(max=steps, prefix=f"Simulating evolution")

    for i in stepline:
        new_state = simulation.run_step(layer, F, D1)
        evolution.append(new_state)
        monomers.append(len(Monomer.all))
        free_monomers.append(len(Monomer.get_free_monomers()))
        stuck_monomers.append(len(Monomer.get_monomers_in_island()))
        occuped_space.append(sum(new_state > 0))
        islands.append(len(Island.all))

        # Monomers already in island
        just_islanded = Monomer.get_monomers_in_island()
        for m in already_islanded:
            if m in just_islanded:
                just_islanded.remove(m)

        visited_sites.append(mean([len(x.visited_sites) for x in just_islanded]))
        average_displacements.append(mean([x.displacements for x in just_islanded]))

        data.record()
        if verbose:
            pbar(i+1)

    # Saving the simulation data
    if save:
        desc = archive.description(L=L, D1=D1, F=F)
        path = archive.new(desc)

        if verbose: print(f"Results saved in {path}")

        savez_compressed(f"{path}/Evolution.npy")

    res = data.Storage(
        evolution = evolution,
        monomers = monomers,
        free_monomers = free_monomers,
        stuck_monomers = stuck_monomers,
        occuped_space = occuped_space,
        islands = islands,
        visited_sites = visited_sites,
        average_displacements = average_displacements,
        a = data.get_a_evolution(),
        b = data.get_b_evolution(),
        c = data.get_c_evolution(),
        d = data.get_d_evolution(),
        ah = data.get_ah_evolution()
    )

    if animate:
        animation.generate(evolution, monomers, free_monomers, stuck_monomers, islands, occuped_space, save_as = "res/animation.gif", plot=False, verbose = False)

    return res
