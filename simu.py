# %%
from numpy import *
import matplotlib.pyplot as plt
from LRFutils import progress
from LRFutils import archive
import analyze

# %% [markdown]
# ---

# %% [markdown]
# # Config

# %%
L = 100 # Size of the grid
D1 = 1e4 # Diffusion coefficient [s-1]
F = linspace(5e-6,1e4,1000,endpoint=True) # Flux [s-1]

simulation_time = 10 # [s]

# %% [markdown]
# ---

# %% [markdown]
# # Class definition

# %%
class Layer:
    def __init__(self, L):
        self.grid = []
        for i in range(L):
            self.grid.append([])
            for j in range(L):
                self.grid[i].append(None)
        self.islands = []
    
    def elements(self):
        monomers = []
        islands = []
        for row in self.grid:
            for monomer in row:
                if monomer is not None:
                    if monomer.island is None:
                        monomers.append(monomer)
                    else:
                        if monomer.island not in islands:
                            islands.append(monomer.island)
        return monomers, islands

    def monomers(self):
        return self.elements()[0]

    def islands(self):
        return self.elements()[1]

    def heightmap(self):
        heightmap = zeros((L,L))
        for x in range(L):
            for y in range(L):
                if self.grid[x][y] is not None:
                    heightmap[x][y] = 1
        return heightmap

    def corrected_pos(x):
        if x < 0:
            return L-1
        elif x >= L:
            return 0
        else:
            return x

# %%
class Island:
    def __init__(self, layer, monomers):
        self.layer = layer
        if type(monomers) is not list: monomers = [monomers] 
        self.monomers = monomers
    
    def add_monomer(self, monomer):
        monomer.island = self
        self.monomers.append(monomer)
                

# %%
class Monomer: 
    def __init__(self, layer, x=None, y=None):
        self.layer = layer
        self.island = None
        
        # Place the monomer randomly on the layer
        cpt = 0
        while True:
            if x is None:
                self.x = random.randint(0, L)
            else:
                self.x = x
            if y is None:
                self.y = random.randint(0, L)
            else: self.y = y
            
            # Add the monomer to the layer
            if layer.grid[self.x ][self.y] is None:
                layer.grid[self.x][self.y] = self
                break

            cpt += 1
            if cpt > 1000:
                print("More than 1000 iteration to find a free spot... cancelling particle apparition for this loop (it's recommended to stop the program)")
                break
    
    def neighbors(self):
        neighbors = []

        if self.layer.grid[Layer.corrected_pos(self.x-1)][self.y] is not None:
            neighbors.append(self.layer.grid[Layer.corrected_pos(self.x-1)][self.y])
        if self.layer.grid[Layer.corrected_pos(self.x+1)][self.y] is not None:
            neighbors.append(self.layer.grid[Layer.corrected_pos(self.x+1)][self.y])
        if self.layer.grid[self.x][Layer.corrected_pos(self.y-1)] is not None:
            neighbors.append(self.layer.grid[self.x][Layer.corrected_pos(self.y-1)])
        if self.layer.grid[self.x][Layer.corrected_pos(self.y+1)] is not None:
            neighbors.append(self.layer.grid[self.x][Layer.corrected_pos(self.y+1)])

        # for x in range(self.x - 1, self.x + 2):
        #     if x < 0: x = L
        #     if x >= L: x = 0
            
        #     for y in range(self.y - 1, self.y + 2):
        #         if y < 0: y = L
        #         if y >= L: y = 0

        #         # Not taking itself
        #         if x != self.x and y != self.y:

        #             # Not taking diagonals
        #             if not (x != self.x and y != self.y):

        #                 # Checking if their is monomers
        #                 if self.layer.grid[x][y] is not None:
        #                     neighbors.append(self.layer.grid[x][y])
                        
        return neighbors

    def islandify(self):
        # Transform the monomer into an island if it has a neighbor
        if len(neighbors := self.neighbors()) != 0:
            islandified = False
            for monomer in neighbors:
                if monomer.island is not None:
                    monomer.island.add_monomer(self)
                    islandified = True
                    break
            if not islandified:
                self.island = Island(self.layer, self)
                for monomer in neighbors:
                    monomer.island = self.island

    def move(self):

        self.islandify()

        if self.island is not None: return

        x, y = self.x, self.y

        # Choose a random direction
        direction = random.randint(0, 2)
        if direction == 0:
            x += random.randint(-1, 2)
        else:
            y += random.randint(-1, 2)

        # Apply limit conditions
        x = Layer.corrected_pos(x)
        y = Layer.corrected_pos(y)

        self.layer.grid[self.x][self.y] = None
        self.layer.grid[x][y] = self
        self.x, self.y = x, y

        self.islandify()

# %% [markdown]
# ---
# # Simulation

# %%
layer = Layer(L)
evolution = []

def evolve():
    # Creating layer
    monomer = Monomer(layer)

    for monomer in layer.monomers():
        
        # Move alll monomers
        monomer.move()

        # Check if monomers are in contact -> create island
        if len(neighbors := monomer.neighbors()) > 0:
            island = Island(layer, neighbors + [monomer])

    # Return the new state of the layer as a matrix with 1 if there is a monomer, 0 otherwise
    return layer.heightmap()

# Generating evolution
a = progress.Bar(max=1000, prefix="Simulating evolution")
for i, simulation_step in enumerate(linspace(0,simulation_time,1000)):
    evolution.append(evolve())
    a(i+1)

path = archive.new()
analyze.generate_animation(evolution, save_as = f"{path}/Evolution.gif", plot=False, verbose = False)


