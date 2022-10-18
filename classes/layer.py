from numpy import *

class Layer:
    def __init__(self, L):
        self.L = L
        self.grid = []
        for i in range(L):
            self.grid.append([])
            for j in range(L):
                self.grid[i].append([])
        self.islands = []
    
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

    def monomers(self):
        return self.elements()[0]

    def islands(self):
        return self.elements()[1]

    def heightmap(self):
        heightmap = zeros((self.L,self.L))
        for x in range(self.L):
            for y in range(self.L):
                if self.grid[x][y] != []:
                    heightmap[x][y] = len(self.grid[x][y])
        return heightmap

    def corrected_pos(self, x):
        if x < 0:
            return self.L-1
        elif x >= self.L:
            return 0
        else:
            return x