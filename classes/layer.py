from numpy import *
from typen import enforce_type_hints

class Layer:

    # ________________________________________________________________________________
    # Create a new virtual substrate

    @enforce_type_hints
    def __init__(self, L:int):
        self.L = L
        self.grid = []
        for i in range(L):
            self.grid.append([])
            for j in range(L):
                self.grid[i].append([])
        self.islands = []



    # ________________________________________________________________________________
    #  Get all elements on this layer
    
    def elements(self):
        monomers = []
        islands = []
        for row in self.grid:
            for monomerList in row:
                if monomerList != []:
                    # If the monomer is NOT a part of an islan, it is counted as a monomer
                    if monomerList[0].island is None:
                        monomers += monomerList
    
                    # If the monomer is a part of an islan, it is counted as an island
                    else:
                        if monomerList[0].island not in islands:
                            islands.append(monomerList[0].island)
        return monomers, islands



    # ________________________________________________________________________________
    # Get the free monomers on this layer

    def monomers(self):
        return self.elements()[0]


    
    # ________________________________________________________________________________
    #  Get the islands on this layer

    def islands(self):
        return self.elements()[1]

    

    # ________________________________________________________________________________
    #  Return a matrix of LxL with the number of monomer (free or in island) per cell

    def heightmap(self):
        heightmap = zeros((self.L,self.L))
        for x in range(self.L):
            for y in range(self.L):
                if self.grid[x][y] != []:
                    heightmap[x][y] = len(self.grid[x][y])
        return heightmap



    # ________________________________________________________________________________
    #  Definition of the boundary conditions

    def corrected_pos(self, x):
        if x < 0:
            return self.L-1
        elif x >= self.L:
            return 0
        else:
            return x