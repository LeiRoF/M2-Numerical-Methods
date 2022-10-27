from numpy import *
import data
import matplotlib.pyplot as plt

# Creating the main plot
fig = None
ax1 = None
ax2 = None
ax3 = None
ax4 = None
ax5 = None
ax6 = None

def setup(F, D1, L, steps, number_of_simulations):
    global fig, ax1, ax2, ax3, ax4, ax5, ax6
    
    # Creating the main plot
    fig = plt.figure(figsize=(15, 10))

    ax1 = fig.add_subplot(2, 3, 1)
    ax1.set_title("Monomer properties")
    ax2 = fig.add_subplot(2, 3, 2)
    ax2.set_title("Population")
    ax3 = fig.add_subplot(2, 3, 3)
    ax3.set_title("Coeficients")
    ax4 = fig.add_subplot(2, 3, 4)
    ax4.set_title("Event occurence")
    ax5 = fig.add_subplot(2, 3, 5)
    ax5.set_title("Population (density)")
    ax6 = fig.add_subplot(2, 3, 6)
    ax6.set_title("Event (proportion)")

    fig.suptitle(f'{number_of_simulations} simulations of {steps} steps on a {L}x{L} grid with F={F} and D1={D1}')

def save(mode):
    fig.savefig(f"res/{mode}.png", facecolor='white')

def show():
    fig.show()

def record(
    L,
    by,
    by_name,
    monomers,
    free_monomers,
    stuck_monomers,
    occuped_space,
    islands,
    visited_sites,
    average_displacements,
    alpha = 1,
    simu = 0
):

    global _first_plot, ax1, ax2, ax3, ax4, ax5, ax6

    if simu == 0:
        alpha = 1

    # ______________________________
    # Update 1st

    plots = [
        ax1.plot(by, average_displacements, "g", alpha=alpha)[0],
        ax1.plot(by, visited_sites, "b", alpha=alpha)[0],
    ]

    if simu == 0:
        legends = ["Average diplacements","Average visited cells"]
        for i in range(len(plots)):
            plots[i].set_label(legends[i])

    # ______________________________
    # Update 2nd plot

    plots = [
        ax2.plot(by, monomers, "b", alpha=alpha)[0],
        ax2.plot(by, free_monomers, "g", alpha=alpha)[0],
        ax2.plot(by, stuck_monomers, "r", alpha=alpha)[0],
        ax2.plot(by, occuped_space, "y", alpha=alpha)[0],
        ax2.plot(by, islands, "m", alpha=alpha)[0]
    ]

    if simu == 0:
        legends = ["Monomers (total)","Free monomers","Monomers in island","Occuped space","Number of islands"]
        for i in range(len(plots)):
            plots[i].set_label(legends[i])

    # ______________________________
    # Update 3rd plot

    k1 = data.get_k1_evolution()
    k2 = data.get_k2_evolution()
    k3 = data.get_k3_evolution()
    plots = [
        ax3.plot(data.smooth(by), data.smooth(k1), "b", alpha=alpha)[0],
        ax3.plot(data.smooth(by), data.smooth(1/array(visited_sites)), "g", alpha=alpha)[0],
        ax3.plot(data.smooth(by), data.smooth(k3), "r", alpha=alpha)[0]
    ]

    if simu == 0:
        legends = ["k1","k2","k3"]
        for i in range(len(plots)):
            plots[i].set_label(legends[i])

    # ______________________________
    # Update 4th plot

    a = data.get_a_evolution()
    b = data.get_b_evolution()
    c = data.get_c_evolution()
    d = data.get_d_evolution()
    ah = data.get_ah_evolution()
    plots = [
        ax4.plot(data.smooth(by), data.smooth(a), "b", alpha=alpha)[0],
        ax4.plot(data.smooth(by), data.smooth(b), "g", alpha=alpha)[0],
        ax4.plot(data.smooth(by), data.smooth(c), "r", alpha=alpha)[0],
        ax4.plot(data.smooth(by), data.smooth(ah), "m", alpha=alpha)[0]
    ]

    if simu == 0:
        legends = ["Deposition","Diffusion","Nucleation","Attachement","Deposition on another monomer"]
        for i in range(len(plots)):
            plots[i].set_label(legends[i])

    # ______________________________
    # Update 5th plot

    plots = [
        ax5.plot(by, array(monomers) / (L**2), "b", alpha=alpha)[0],
        ax5.plot(by, array(free_monomers) / (L**2), "g", alpha=alpha)[0],
        ax5.plot(by, array(stuck_monomers) / (L**2), "r", alpha=alpha)[0],
        ax5.plot(by, array(occuped_space) / (L**2), "y", alpha=alpha)[0],
    ]

    if simu == 0:
        legends = ["Monomers (total)","Free monomers","Monomers in island","Occuped space"]
        for i in range(len(plots)):
            plots[i].set_label(legends[i])

    s = a + b + c + d + ah
    s += s==0

    # ______________________________
    # Update 6th plot
    
    plots = [
        ax6.plot(data.smooth(by), data.smooth(a / s), "b", alpha=alpha)[0],
        ax6.plot(data.smooth(by), data.smooth(b / s), "g", alpha=alpha)[0],
        ax6.plot(data.smooth(by), data.smooth(c / s), "r", alpha=alpha)[0],
        ax6.plot(data.smooth(by), data.smooth(d / s), "y", alpha=alpha)[0],
        ax6.plot(data.smooth(by), data.smooth(ah / s), "m", alpha=alpha)[0]
    ]

    if simu == 0:
        legends = ["Deposition","Diffusion","Nucleation","Attachement","Deposition on another monomer"]
        for i in range(len(plots)):
            plots[i].set_label(legends[i])

    # ______________________________
    # Plot properties

    if simu == 0:
        for i, ax in enumerate([ax1, ax2, ax3, ax4, ax5, ax6]):
            ax.grid()
            ax.legend()
            if by_name.lower() == "density": ax.set_xlabel("Density")
            if by_name.lower() == "iteration": ax.set_xlabel("Iteration")
            if i in [0, 1, 3]:
                ax.set_ylabel("Count")
            for i in [2, 4, 5]:
                ax.set_ylabel("Ratio")