import numpy as np
np.seterr(all="ignore")

# Just an empty objet that will store all the data from a simulation
class Storage():
    def __init__(self, **kwargs):
        if "evolution" in kwargs: self.evolution = kwargs["evolution"]
        if "monomers" in kwargs: self.monomers = kwargs["monomers"]
        if "free_monomers" in kwargs: self.free_monomers = kwargs["free_monomers"]
        if "stuck_monomers" in kwargs: self.stuck_monomers = kwargs["stuck_monomers"]
        if "occuped_space" in kwargs: self.occuped_space = kwargs["occuped_space"]
        if "islands" in kwargs: self.islands = kwargs["islands"]
        if "visited_sites" in kwargs: self.visited_sites = kwargs["visited_sites"]
        if "average_displacements" in kwargs: self.average_displacements = kwargs["average_displacements"]
        if "a" in kwargs: self.a = kwargs["a"]
        if "b" in kwargs: self.b = kwargs["b"]
        if "c" in kwargs: self.c = kwargs["c"]
        if "d" in kwargs: self.d = kwargs["d"]
        if "ah" in kwargs: self.ah = kwargs["ah"]
        if "k1" in kwargs: self.k1 = kwargs["k1"]
        if "k2" in kwargs: self.k2 = kwargs["k2"]
        if "k3" in kwargs: self.k3 = kwargs["k3"]

# This file contain variable that store the occurrence of each events

a = 0 # deposition
b = 0 # diffusion
c = 0 # nucleation
d = 0 # attachment
e = 0 # detachment
f = 0 # edge diffusion
g = 0 # diffusion down step
h = 0 # nucleation on top of island
i = 0 # dimer diffusion
ah = 0 # deposition on top of island



# ________________________________________________________________________________
# Computation ok k

def get_k1():
    if b == 0:
        return 0
    return c / b

def get_k2():
    if b == 0:
        return 0
    return d / b

def get_k3():
    if a == 0:
        return 0
    return ah / a



# ________________________________________________________________________________
# Get and save the data the data

_record = []
def record() -> dict[str, int | float]:
    global a,b,c,d,e,f,g,h,i,ah
    current = {
        'a': a, # ok
        'b': b, # ok
        'c': c, # ok
        'd': d, # ok
        'e': e,
        'f': f,
        'g': g,
        'h': h,
        'i': i,
        'ah': ah, # ok
        'k1': get_k1(), # ok
        'k2': get_k2(), # ok
        'k3': get_k3(), # ok
    }
    _record.append(current)
    a = 0 # deposition
    b = 0 # diffusion
    c = 0 # nucleation
    d = 0 # attachment
    e = 0 # detachment
    f = 0 # edge diffusion
    g = 0 # diffusion down step
    h = 0 # nucleation on top of island
    i = 0 # dimer diffusion
    ah = 0 # deposition on top of island
    return current



# ________________________________________________________________________________
# Get the evolution of each data

def get_a_evolution() -> list[int]:
    return np.array([r['a'] for r in _record])

def get_b_evolution() -> list[int]:
    return np.array([r['b'] for r in _record])

def get_c_evolution() -> list[int]:
    return np.array([r['c'] for r in _record])

def get_d_evolution() -> list[int]:
    return np.array([r['d'] for r in _record])

def get_e_evolution() -> list[int]:
    return np.array([r['e'] for r in _record])

def get_f_evolution() -> list[int]:
    return np.array([r['f'] for r in _record])

def get_g_evolution() -> list[int]:
    return np.array([r['g'] for r in _record])

def get_h_evolution() -> list[int]:
    return np.array([r['h'] for r in _record])

def get_i_evolution() -> list[int]:
    return np.array([r['i'] for r in _record])

def get_ah_evolution() -> list[int]:
    return np.array([r['ah'] for r in _record])

def get_k1_evolution() -> list[float]:
    return np.array([r['k1'] for r in _record])

def get_k2_evolution() -> list[float]:
    return np.array([r['k2'] for r in _record])

def get_k3_evolution() -> list[float]:
    return np.array([r['k3'] for r in _record])

def smooth(lst: list[float], average_elements:int = 100) -> float:
    res = np.zeros(len(lst))
    for i in range(len(lst)):
        a = max(int(i-(average_elements/2)),0)
        b = min(int(i+(average_elements/2)), len(lst))
        res[i] = np.average(lst[a:b])
    return res