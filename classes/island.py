class Island:
    all = []
    id = 0
    def __init__(self, layer, monomers):
        self.id = Island.id
        Island.id += 1
        Island.all.append(self)
        self.layer = layer
        if type(monomers) is not list: monomers = [monomers] 
        self.monomers = monomers
    
    def add_monomer(self, monomer):
        monomer.island = self
        self.monomers.append(monomer)