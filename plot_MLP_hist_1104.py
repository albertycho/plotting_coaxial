#!/usr/bin/env python3

import os
import sys
import csv
import math
import statistics
import numpy as np
import matplotlib
import matplotlib.pyplot as plt 



#mlp_hists=[[0]*100]*2
mlp_hists=[]

apps = ['moses','imgdnn','masstree','pagerank' ,'xapian', 'sphinx','herd']


i=0;
for app in apps:
    mlp_hist=[0]*50
    fname = 'zsim.out_'+app
    zout=open(fname,'r')
    line = zout.readline()
    phases=0
    while line:
        if('Simulated phases' in line):
            tmp=line.split(':')[1];
            tmp=tmp.split('#')[0]
            phases = float(tmp)
            phases=phases*10
            print(phases)
        if('MLP Hist' in line):
            for j in range(50):
                line=zout.readline()
                #print(line)
                tmp2=line.split(':')
                assert(int(tmp2[0]) == j)
                assert(phases!=0)
                norm_val = float(tmp2[1]) / float(phases)
                #mlp_hists[i][j]=norm_val
                mlp_hist[j]=norm_val
                #print(str(i)+','+str(j)+','+str(norm_val))

                #cumulative_bw.append(bw)
            break;
        line=zout.readline()

    i=i+1
    zout.close()
    mlp_hists.append(mlp_hist)
        
ifig,iax=plt.subplots()
#iax.set_title(field_names[i])
X_axis = np.arange(50)


barwidth = 0.5
### just plot one ideal mc

#for j in range(1,len(mcs)):
#    for k in range(len(ddio_setups)):
alval=1
for k in range(len(apps)):
    iax.plot(X_axis, mlp_hists[k],label=apps[k]);
#iax.plot(X_axis, mlp_hists[0],label=apps[0]);
#iax.plot(X_axis, mlp_hists[1],label=apps[1]);
#iax.set_ylim([0,2])
iax.legend(ncol=2)

iax.grid()

ifig.savefig('mlp_hists.png', bbox_inches='tight')
