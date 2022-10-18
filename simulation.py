from numpy import *
from classes.monomer import Monomer

# Evolution
def run_step(layer, F, D1):

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