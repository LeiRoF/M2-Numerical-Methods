from numpy import *
from classes.layer import Layer
from .island import Island
import data
from typen import enforce_type_hints


class Monomer: 

    all = []
    _id = 0



    # ________________________________________________________________________________
    # Create a new monomer

    # @enforce_type_hints
    def __init__(self, layer: Layer, prob: int|float = 1, x: int|None = None, y: int|None = None):

        self.id = Monomer._id
        Monomer._id += 1
        Monomer.all.append(self)
        self.layer = layer
        self.island = None
        data.a += 1 # deposition event
        
        # Place the monomer randomly on the layer
        if x is None:
            self.x = random.randint(0, layer.L)
        else:
            self.x = x

        if y is None:
            self.y = random.randint(0, layer.L)
        else: self.y = y
        
        # Add the monomer to the grid
        layer.grid[self.x][self.y].append(self)

        # Check if the monomer arrive on another one
        if self.islandify():
            data.ah += 1 # deposition on top of another monomer event



    # ________________________________________________________________________________
    # Count the number of monomers given in parameter that are in an island

    @staticmethod
    def is_part_of_island(monomer: list["Monomer"]) -> int:

        count = 0
        for m in monomer:
            if m.island is not None:
                count += 1

        return count



    # ________________________________________________________________________________
    # Stick monomers to form an island

    def islandify(self) -> bool:

        if self.island is not None:
            return True # the monomer is already an island

        neighbors = self.neighbors()

        # Transform the monomer into an island if it has a neighbor
        if neighbors == []:
            return False # the monomer is still free

        # Increase event according type of collision
        if Monomer.is_part_of_island(neighbors):
            data.d +=1
        else:
            data.c += 1

        new_island = Island(self.layer, self)
        
        self.island = new_island

        # Replace the old island by the new one
        for monomer in neighbors:
            if monomer is self:
                continue
            if (old_island := monomer.island) is not None:
                old_island.replace(new_island)
        
        return True # the monomer get islanded



    # ________________________________________________________________________________
    # Get all the nerby monomers

    def neighbors(self):
        neighbors = []

        monomer_in_cell = self.layer.grid
        pos = self.layer.corrected_pos
        x = self.x
        y = self.y

        neighbors += monomer_in_cell[pos(x-1)][y]
        neighbors += monomer_in_cell[pos(x+1)][y]
        neighbors += monomer_in_cell[x][pos(y-1)]
        neighbors += monomer_in_cell[x][pos(y+1)]

        m = [] + monomer_in_cell[x][y] # create a new list to avoid modifying the original

        if self in m:
            m.remove(self)

        neighbors += m

        return neighbors
                    


    # ________________________________________________________________________________
    # Move a monomer (diffusionn)

    def move(self) -> bool:

        # Check if the monomer didn't get collided by another one
        if self.islandify():
            return False # The monomer hasn't moved

        x, y = self.x, self.y

        # Chose a random direction
        d = random.randint(0, 4)
        if d == 0: x -= 1
        elif d == 1: x += 1
        elif d == 2: y -= 1
        elif d == 3: y += 1

        # Apply limit conditions
        x = self.layer.corrected_pos(x)
        y = self.layer.corrected_pos(y)

        # Move the monomer on the new location
        self.layer.grid[self.x][self.y].remove(self)
        self.layer.grid[x][y].append(self)
        self.x, self.y = x, y

        # Check if it colided another monomer
        self.islandify()

        # Diffusion event
        data.b += 1

        return True # The monomer has moved



    # ________________________________________________________________________________
    # Get the list of free monomers

    def get_free_monomers():
        free = []
        for monomer in Monomer.all:
            if monomer.island is None:
                free.append(monomer)
        return free



    # ________________________________________________________________________________
    # Get the list of monomers trapped in island

    def get_monomers_in_island():
        stuck = []
        for monomer in Monomer.all:
            if monomer.island is not None:
                stuck.append(monomer)
        return stuck
