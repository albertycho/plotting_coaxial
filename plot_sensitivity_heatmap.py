#!/usr/bin/env python3

import os
import sys
import csv
import math
import statistics
import numpy as np
import matplotlib
import matplotlib.pyplot as plt 
import seaborn as sn

def getindex(elem, arr):
    for i in range(len(arr)):
        if str(arr[i])==elem:
            return i
    print('didnt find elem '+elem+' in arr')
    exit
    return -1


xtick_labels = ['10ns','30ns','50ns']
ytick_labels = ['2X','4X','8X']

delays=['20','60','100']
bw_gains=['2','4','8']



#data=[[1,2,3],[1,2,0.2],[1.4,1.1,0.8]]
#ipc_gains = [[1]*3]*3
ipc_gains = [[0,0,0],[0,0,0],[0,0,0]]

infile = 'ss_ipcs.csv'
if not(infile in os.listdir('.')):
    print('infile not found')
    exit(1)

f=open(infile,'r')
line=f.readline();
DDR_ipcs = 0
if('DDR' in line):
    tmp=line.split(',')[1]
    DDR_ipcs = float(tmp)
    print(str(DDR_ipcs))
assert(DDR_ipcs!=0)

line=f.readline();
while(line):
    tmp=line.split(',')
    tmp2=tmp[0].split('_')
    bw_gain = tmp2[0]
    delay=tmp2[1]
    yi=getindex(bw_gain, bw_gains)
    xi=getindex(delay, delays)
    ipc_delta = float( ((float(tmp[1]) / DDR_ipcs) -1) )
    print(str(ipc_delta))
    print(str(xi)+','+str(yi))
    ipc_gains[yi][xi]=ipc_delta
    line=f.readline();



print(ipc_gains)

#hm=sn.heatmap(data=ipc_gains, annot=True, fmt=".0%", vmin=-1,vmax=3)
hm=sn.heatmap(data=ipc_gains, annot=True, fmt=".0%", vmin=-1,vmax=3, cmap="BuPu")
#plt.annotate
X_axis = [0.5,1.5,2.5]
#xtick_labels = [10,30,50]
#hm.set_xticks(xtick_labels)
plt.xticks(X_axis, xtick_labels)
plt.yticks(X_axis, ytick_labels)
plt.savefig('heatmap.png', bbox_inches='tight')
