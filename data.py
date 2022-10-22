import numpy as np

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