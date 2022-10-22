from numpy import *
import data

_first_plot = True

axes = []

def setup(fig):
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

    return [ax1, ax2, ax3, ax4, ax5, ax6]

def record(fig,
    L,
    by,
    ab_name,
    monomers,
    free_monomers,
    stuck_monomers,
    occuped_space,
    islands,
    visited_sites,
    average_displacements,
    alpha = 1
):
    global _first_plot, axes
    if _first_plot:
        axes = setup(fig)
        _first_plot = False
        # alpha = 1
   
    ax1, ax2, ax3, ax4, ax5, ax6 = axes

    plots = [
        ax1.plot(by, average_displacements, "g", alpha=alpha)[0],
        ax1.plot(by, visited_sites, "b", alpha=alpha)[0],
    ]

    legends = ["Average diplacements","Average visited cells"]

    # if _first_plot:
    for i in range(len(plots)):
        plots[i].set_label(legends[i])

    # Update 2nd plot
    plots = [
        ax2.plot(by, monomers, "b", alpha=alpha)[0],
        ax2.plot(by, free_monomers, "g", alpha=alpha)[0],
        ax2.plot(by, stuck_monomers, "r", alpha=alpha)[0],
        ax2.plot(by, occuped_space, "y", alpha=alpha)[0],
        ax2.plot(by, islands, "m", alpha=alpha)[0]
    ]

    legends = ["Monomers (total)","Free monomers","Monomers in island","Occuped space","Number of islands"]

    # if _first_plot:
    for i in range(len(plots)):
        plots[i].set_label(legends[i])

    # Update 3rd plot
    k1 = data.get_k1_evolution()
    k2 = data.get_k2_evolution()
    k3 = data.get_k3_evolution()
    plots = [
        ax3.plot(data.smooth(by), data.smooth(k1), "b", alpha=alpha)[0],
        ax3.plot(data.smooth(by), data.smooth(1/array(visited_sites)), "g", alpha=alpha)[0],
        ax3.plot(data.smooth(by), data.smooth(k3), "r", alpha=alpha)[0]
    ]

    legends = ["k1","k2","k3"]

    # if _first_plot:
    for i in range(len(plots)):
        plots[i].set_label(legends[i])

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

    legends = ["Deposition","Diffusion","Nucleation","Attachement","Deposition on another monomer"]

    # if _first_plot:
    for i in range(len(plots)):
        plots[i].set_label(legends[i])

    # Update 5th plot
    plots = [
        ax5.plot(by, array(monomers) / (L**2), "b", alpha=alpha)[0],
        ax5.plot(by, array(free_monomers) / (L**2), "g", alpha=alpha)[0],
        ax5.plot(by, array(stuck_monomers) / (L**2), "r", alpha=alpha)[0],
        ax5.plot(by, array(occuped_space) / (L**2), "y", alpha=alpha)[0],
    ]

    legends = ["Monomers (total)","Free monomers","Monomers in island","Occuped space"]

    # if _first_plot:
    for i in range(len(plots)):
        plots[i].set_label(legends[i])

    s = a + b + c + d + ah
    s += s==0

    # Update 6th plot
    plots = [
        ax6.plot(data.smooth(by), data.smooth(a / s), "b", alpha=alpha)[0],
        ax6.plot(data.smooth(by), data.smooth(b / s), "g", alpha=alpha)[0],
        ax6.plot(data.smooth(by), data.smooth(c / s), "r", alpha=alpha)[0],
        ax6.plot(data.smooth(by), data.smooth(d / s), "y", alpha=alpha)[0],
        ax6.plot(data.smooth(by), data.smooth(ah / s), "m", alpha=alpha)[0]
    ]

    legends = ["Deposition","Diffusion","Nucleation","Attachement","Deposition on another monomer"]

    # if _first_plot:
    for i in range(len(plots)):
        plots[i].set_label(legends[i])