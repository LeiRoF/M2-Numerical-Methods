import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import time
from datetime import datetime
from collections import OrderedDict
#----------------------------------------------------------------------------------
time_1 = datetime.now()

D = 10e-4
L = 50
N_depo = 50
lattice = np.zeros((L,L))
max_Ndiff = 50
nb = 500
k2 = []

depo = []
for i in range(0,N_depo):
    depo.append([np.random.randint(0,L),np.random.randint(0,L)])

def diffusion():
    Ndiff = np.random.randint(0,max_Ndiff)
    #print('Ndiff =',Ndiff)
    pos = []
    sites = []
    pos.append([np.random.randint(0,L),np.random.randint(0,L)])
    for i in range(1, Ndiff):
        dir = np.random.randint(0,4)
        if dir == 0 :
            if pos[i-1][0] == L: 
                pos.append([0,pos[i-1][1]])
            else:
                pos.append([pos[i-1][0]+1,pos[i-1][1]])
        if dir == 1: 
            if pos[i-1][1] == L: 
                pos.append([pos[i-1][0],0])
            else:
                pos.append([pos[i-1][0],pos[i-1][1]+1])
        if dir == 2:
            if pos[i-1][0] == 0: 
                pos.append([L,pos[i-1][1]])
            else:
                pos.append([pos[i-1][0]-1,pos[i-1][1]])
        if dir == 3:
            if pos[i-1][1] == 0: 
                pos.append([pos[i-1][0],L])
            else:
                pos.append([pos[i-1][0],pos[i-1][1]-1])

        for j in pos:
            if j not in sites:
                sites.append(j)

        if pos[i] in depo:
            break
    return [pos,sites]

for k in range(0,100):
    for i in range(0,nb):
        sim = diffusion()
        res = len(sim[1])/len(sim[0])
        k2.append(res)
    mk2 = np.mean(k2)
k2.append(mk2)
print('k2 = ',np.mean(k2))

plt.figure()
plt.hist(k2,200)
plt.show()


time_2 = datetime.now()
ex_time = time_2-time_1
print('Running time : ',ex_time)