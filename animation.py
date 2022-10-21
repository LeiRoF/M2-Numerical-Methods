import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import time
from LRFutils import progress
from matplotlib.colors import Colormap
from numpy import *
from matplotlib.lines import Line2D
import data

def generate(evolution, monomer, free, stuk, island, occuped_space, save_as = None, plot=False, verbose = False, axis:int=0):

    fig = plt.figure(figsize=(10, 10))
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3)
    ax4 = fig.add_subplot(2, 2, 4)

    i=0

    # Init 1st plot
    im = ax1.imshow(evolution[0], interpolation='none', aspect='auto', vmin=0, vmax=amax(evolution), cmap="inferno")

    # Init 2nd plot
    ax2.set_xlim(0, len(evolution))
    ax2.set_ylim(0, max(max(monomer), max(free), max(stuk), max(island)))
    line1 = Line2D([], [], label="Monomers", color="red")
    line2 = Line2D([], [], label="Free monomers", color="blue")
    line3 = Line2D([], [], label="Stuck monomers", color="green")
    line4 = Line2D([], [], label="Occuped space", color="black")
    line5 = Line2D([], [], label="Islands", color="orange")
    ax2.add_line(line1)
    ax2.add_line(line2)
    ax2.add_line(line3)
    ax2.add_line(line4)
    ax2.add_line(line5)

    # Init 3rd plot
    k1 = data.get_k1_evolution()
    k2 = data.get_k2_evolution()
    k3 = data.get_k3_evolution()
    ax3.set_xlim(0, len(evolution))
    ax3.set_ylim(0, 1)
    line_k1 = Line2D([], [], label="k1", color="red")
    line_k2 = Line2D([], [], label="k2", color="blue")
    line_k3 = Line2D([], [], label="k3", color="green")
    ax3.add_line(line_k1)
    ax3.add_line(line_k2)
    ax3.add_line(line_k3)

    # Init 4th plot
    a = data.get_a_evolution()
    b = data.get_b_evolution()
    c = data.get_c_evolution()
    d = data.get_d_evolution()
    ah = data.get_ah_evolution()
    ax4.set_xlim(0, len(evolution))
    ax4.set_ylim(0, max(max(a), max(b), max(c), max(d), max(ah)))
    line_a = Line2D([], [], label="Deposition", color="blue")
    line_b = Line2D([], [], label="Diffusion", color="orange")
    line_c = Line2D([], [], label="Nucleation", color="green")
    line_d = Line2D([], [], label="Attachement", color="red")
    line_ah = Line2D([], [], label="Deposition on monomer", color="black")
    ax4.add_line(line_a)
    ax4.add_line(line_b)
    ax4.add_line(line_c)
    ax4.add_line(line_d)
    ax4.add_line(line_ah)


    # Generate frames
    progress_bar = progress.Bar(max=len(evolution), prefix="Generating animation")
    def updatefig(i):
        if verbose : print(f"🎞️ Generating animation... Step: {i+1}/{len(evolution)} ({(i+1)/len(evolution)*100:.0f} %)", end="\r")

        # Update 1st plot
        im.set_array(evolution[i])

        # Update 2nd plot
        line1.set_data(arange(i), monomer[:i])
        line2.set_data(arange(i), free[:i])
        line3.set_data(arange(i), stuk[:i])
        line4.set_data(arange(i), occuped_space[:i])
        line5.set_data(arange(i), island[:i])
        # ax2.plot(i, monomer[i], 'rx', label="Monomers")
        # ax2.plot(i, free[i], 'g+', label="Free monomers")
        # ax2.plot(i, stuk[i], 'b4', label="Stuck monomers")
        # ax2.plot(i, occuped_space[i], 'k1', label="Occuped space")
        # ax2.plot(i, island[i], 'y.', label="Islands")

        # Update 3rd plot
        line_k1.set_data(arange(i), k1[:i])
        line_k2.set_data(arange(i), k2[:i])
        line_k3.set_data(arange(i), k3[:i])

        # Update 4th plot
        line_a.set_data(arange(i), a[:i])
        line_b.set_data(arange(i), b[:i])
        line_c.set_data(arange(i), c[:i])
        line_d.set_data(arange(i), d[:i])
        line_ah.set_data(arange(i), ah[:i])

        progress_bar(i+1)
        return im,
        
    ani = animation.FuncAnimation(fig, updatefig, range(len(evolution)), blit=True)

    # Adding 2nd plot properties
    ax2.grid()
    ax2.legend()

    # Adding 3rd plot properties
    ax3.grid()
    ax3.legend()

    # Adding 4th plot properties
    ax4.grid()
    ax4.legend()

    # __________________________________________________
    # Saving animation

    if save_as: 
        if not os.path.isdir(os.path.split(save_as)[0]): os.makedirs(os.path.split(save_as)[0])
        ani.save(save_as)

    if plot: plt.show()

