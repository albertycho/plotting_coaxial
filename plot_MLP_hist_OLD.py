#!/usr/bin/env python3

import os
import sys 
import csv 
import math
import statistics
import numpy as np
from os.path import exists
import matplotlib
import matplotlib.pyplot as plt 


zoutf= open('zsim.out')

hist_buckets=100

mbw_hist=[0]*40;
mbw_raw=[];

mlp_hist=[0]*hist_buckets

num_cores=0;


line = zoutf.readline()
while line:
    if 'MLP Hist' in line:
        num_cores=num_cores+1
        for i in range(hist_buckets):
            line=zoutf.readline()
            tmp=line.split(':')
            assert(int(tmp[0]) == i)
            mlp_hist[i]=mlp_hist[i] + int(tmp[1])

    line = zoutf.readline()


mlp_hist =  [x / num_cores for x in mlp_hist]
#mlp_hist=mlp_hist/num_cores;

###### plot raw mbw fluctuation

matplotlib.rcParams.update({'font.size': 30})

ifig,iax=plt.subplots()

linewidth=1
mlp_xaxis=[x for x in range(hist_buckets)]
iax.bar(mlp_xaxis, mlp_hist, width=linewidth);
#iax.bar(dist_xaxis, mbw_hist, width=linewidth);
#iax.set_ylim([0,40])
plt.ylabel('Histogram')
plt.xlabel('# of memory accesses in the last 100 cycles')
ifig.set_size_inches(20,12)

ifig.savefig('MLP_hist.png', bbox_inches='tight')

#exit(0)


