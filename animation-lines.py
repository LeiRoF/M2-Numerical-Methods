import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import time
from LRFutils import progress
from matplotlib.colors import Colormap
from numpy import *
from matplotlib.lines import Line2D

def generate(evolution, monomer, free, stuk, island, occuped_space, save_as = None, plot=False, verbose = False, axis:int=0):

    fig = plt.figure(figsize=(40, 20))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    i=0
    im = ax1.imshow(evolution[0], interpolation='none', aspect='auto', vmin=0, vmax=amax(evolution), cmap="inferno")
    ax2.set_ylim(0, len(evolution))
    line1 = Line2D([], [], label="Monomers", color="red")
    line2 = Line2D([], [], label="Free monomers", color="blue")
    line3 = Line2D([], [], label="Stuck monomers", color="green")
    line4 = Line2D([], [], label="Occuped space", color="black")
    line5 = Line2D([], [], label="Islands", color="orange")
    ax2.add_line(line1)
    ax2.add_line(line2)
    ax2.add_line(line3)
    ax2.add_line(line4)
    ax2.legend(handles=[line1, line2, line3, line4], loc=2)
    ax2.grid()


    a = progress.Bar(max=len(evolution), prefix="Generating animation")
    def updatefig(i):
        if verbose : print(f"🎞️ Generating animation... Step: {i+1}/{len(evolution)} ({(i+1)/len(evolution)*100:.0f} %)", end="\r")
        im.set_array(evolution[i])
        line1.set_data(arange(i), monomer[:i])
        line2.set_data(arange(i), free[:i])
        line3.set_data(arange(i), stuk[:i])
        line4.set_data(arange(i), occuped_space[:i])
        line5.set_data(arange(i), island[:i])
        a(i+1)
        return im,
    ani = animation.FuncAnimation(fig, updatefig, range(len(evolution)), blit=True)

    # __________________________________________________
    # Saving animation

    if save_as: 
        if not os.path.isdir(os.path.split(save_as)[0]): os.makedirs(os.path.split(save_as)[0])
        ani.save(save_as)

    if plot: plt.show()

if __name__ == "__main__":
    N = 10
    evolution = zeros((N*N,N,N))
    for i in range(N*N):
        evolution[i, i%N, i//N] = 1

    generate(evolution, save_as="./test.gif", plot=True, axis=-1)

