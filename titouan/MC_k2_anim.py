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
max_Ndiff = 300
nb = 1000

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

def generate_animation(evolution, save_as = None, plot=False, verbose = False):

    if verbose : print("\n🎞️ Generating animation...", end="\r")

    fig = plt.figure()
    i=0
    im = plt.imshow(evolution[0], animated=True)
    def updatefig(i):
        if verbose : print(f"🎞️ Generating animation... Step: {i+1}/{len(evolution)} ({(i+1)/len(evolution)*100:.0f} %)", end="\r")
        im.set_array(evolution[i])
        return im,
    ani = animation.FuncAnimation(fig, updatefig, range(len(evolution)), blit=True)

    print(f"🎞️ Generating animation... Step: {len(evolution)}/{len(evolution)} (100 %) ✅")

    # __________________________________________________
    # Saving animation

    if save_as: 
        if verbose : print(f"\n📀  Saving animation...", end="\r")
        if not os.path.isdir(os.path.split(save_as)[0]): os.makedirs(os.path.split(save_as)[0])
        ani.save(save_as)
        if verbose : print(f"📀  Saving animation... ✅\n   -> Saved in {save_as}")

    if plot: plt.show()


visited = diffusion()
evol = np.zeros((len(visited[0])+1,L+1,L+1))


for j in range(len(visited[0])):
    for i in range(N_depo):
        evol[j][depo[i][0]][depo[i][1]] = 1

for i in range(1,len(visited[0])+1):
    evol[i][visited[0][i-1][0]][visited[0][i-1][1]] = 1
generate_animation(evol, save_as = None, plot=True, verbose = False)


k2 = len(visited[1])/len(visited[0])
#print('k2 = ',k2)

k2 = []
for i in range(0,nb):
    sim = diffusion()
    res = len(sim[1])/len(sim[0])
    k2.append(res)

print('k2 = ',np.mean(k2))

plt.figure()
plt.hist(k2,200)
plt.show()


time_2 = datetime.now()
ex_time = time_2-time_1
print('Running time : ',ex_time)