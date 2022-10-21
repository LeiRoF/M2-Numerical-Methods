from typen import enforce_type_hints
from .layer import Layer
from copy import copy

class Island:
    all = []
    id = 0



    # ________________________________________________________________________________
    # Create a new island

    # @enforce_type_hints
    def __init__(self, layer: Layer, monomers: list["Monomer"]):
        self.id = Island.id
        Island.id += 1
        Island.all.append(self)
        self.layer = layer
        if not isinstance(monomers, list): monomers = [monomers]
        self.monomers = copy(monomers)
    


    # ________________________________________________________________________________
    # Add monomer to island
    
    @enforce_type_hints
    def add_monomer(self, monomer: "Monomer"):
        monomer.island = self
        self.monomers.append(monomer)



    # ________________________________________________________________________________
    # Replace this island by a new one and return the number of edited monomers
    
    @enforce_type_hints
    def replace(self, island: Island) -> int:
        cpt = 0
        if island is self:
            return 0
        for monomer in self.monomers:
            island.add_monomer(monomer)
            cpt += 1
        Island.all.remove(self)
        del self
        return cpt
