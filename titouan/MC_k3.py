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
N_depo = 0
lattice = np.zeros((L,L))
max_Ndiff = 50
nb = np.arange(50,2000,50)
res = []

for q in nb:
    for m in range(0,q):
        k3 = []
        depo = []
        colision = 0
        deposite = 0
        for i in range(0,N_depo):
            depo.append([np.random.randint(0,L),np.random.randint(0,L)])

        for l in range(0,q):
            pos = [np.random.randint(0,L),np.random.randint(0,L)]
            if pos in depo:
                colision += 1
            else:
                deposite += 1
                depo.append(pos)

        mk3 = colision/deposite
        k3.append(mk3)
    res.append(np.mean(k3))

plt.figure()
plt.plot(nb,res,ls='',marker='+',c='b')
plt.xlabel('Ndep')
plt.ylabel('k3')
plt.show()

time_2 = datetime.now()
ex_time = time_2-time_1
print('Running time : ',ex_time)