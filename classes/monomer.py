from numpy import *
from classes.layer import Layer
from .island import Island

class Monomer: 
    all = []
    id = 0
    def __init__(self, layer, prob=1, x=None, y=None):
        self.id = Monomer.id
        Monomer.id += 1
        Monomer.all.append(self)
        self.layer = layer
        self.island = None
        
        # Place the monomer randomly on the layer
        if x is None:
            self.x = random.randint(0, layer.L)
        else:
            self.x = x
        if y is None:
            self.y = random.randint(0, layer.L)
        else: self.y = y
        
        layer.grid[self.x][self.y].append(self)
        self.islandify()
    
    def neighbors(self):
        neighbors = []

        if m := self.layer.grid[self.layer.corrected_pos(self.x-1)][self.y]:
            neighbors += m
        if m := self.layer.grid[self.layer.corrected_pos(self.x+1)][self.y]:
            neighbors += m
        if m := self.layer.grid[self.x][self.layer.corrected_pos(self.y-1)]:
            neighbors += m
        if m := self.layer.grid[self.x][self.layer.corrected_pos(self.y+1)]:
            neighbors += m
        if m := self.layer.grid[self.x][self.y]:
            m = [] + m # create a new list to avoid modifying the original
            if self in m:
                m.remove(self)
            neighbors += m
                        
        return neighbors

    def islandify(self):
        # Transform the monomer into an island if it has a neighbor
        if len(neighbors := self.neighbors()) != 0:

            new_island = Island(self.layer, self)
            
            self.island = new_island

            for monomer in neighbors:
                old_island = monomer.island
                if old_island is not None and old_island is not new_island:
                    for m in Monomer.all:
                        if m.island is old_island:
                            new_island.add_monomer(m)
                    if old_island in Island.all:
                        Island.all.remove(old_island)
                    


    def move(self):

        self.islandify()

        if self.island is not None: return

        x, y = self.x, self.y

        d = random.randint(0, 4)
        if d == 0: x -= 1
        elif d == 1: x += 1
        elif d == 2: y -= 1
        elif d == 3: y += 1

        # Apply limit conditions
        x = self.layer.corrected_pos(x)
        y = self.layer.corrected_pos(y)

        self.layer.grid[self.x][self.y].remove(self)
        self.layer.grid[x][y].append(self)
        self.x, self.y = x, y

        self.islandify()

    def get_free_monomers():
        free = []
        for monomer in Monomer.all:
            if monomer.island is None:
                free.append(monomer)
        return free

    def get_monomers_in_island():
        stuck = []
        for monomer in Monomer.all:
            if monomer.island is not None:
                stuck.append(monomer)
        return stuck
