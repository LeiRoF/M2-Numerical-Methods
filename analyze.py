import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import time
from LRFutils import progress
from matplotlib import colors

C = colors.Normalize(vmin=0, vmax=10)

def generate_animation(evolution, save_as = None, plot=False, verbose = False):

    fig = plt.figure()
    i=0
    im = plt.imshow(evolution[0], animated=True)
    a = progress.Bar(max=len(evolution), prefix="Generating animation")
    def updatefig(i):
        if verbose : print(f"🎞️ Generating animation... Step: {i+1}/{len(evolution)} ({(i+1)/len(evolution)*100:.0f} %)", end="\r")
        im.set_array(evolution[i])
        a(i+1)
        return im,
    plt.clim(0, 150)
    ani = animation.FuncAnimation(fig, updatefig, range(len(evolution)), blit=True)

    # __________________________________________________
    # Saving animation

    if save_as: 
        if not os.path.isdir(os.path.split(save_as)[0]): os.makedirs(os.path.split(save_as)[0])
        ani.save(save_as)

    if plot: plt.show()