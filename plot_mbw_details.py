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


f_dramsimlog = open('dramsim.log')

mbw_hist=[0]*40;
mbw_raw=[];


line = f_dramsimlog.readline()
while line:
    if 'aggregate average bandwidth' in line:
        tmp1=line.split('aggregate average bandwidth')[1]
        tmp1=tmp1.split('GB')[0]
        tmp2=float(tmp1)*2
        mbw_raw.append(tmp2)
        mbw_hist[(int(tmp2))]=mbw_hist[(int(tmp2))] + 1;

    line = f_dramsimlog.readline()

###### plot raw mbw fluctuation

matplotlib.rcParams.update({'font.size': 30})

ifig,iax=plt.subplots()

linewidth=1
raw_xaxis=[x for x in range(len(mbw_raw))]
iax.plot(raw_xaxis, mbw_raw, linewidth=linewidth);
iax.set_ylim([0,40])
plt.ylabel('Sampled Memory Bandwidth (GB/s)')
plt.xlabel('Sampled Phase (4ms periods)')
ifig.set_size_inches(20,12)

ifig.savefig('mbw_raw.png', bbox_inches='tight')

#exit(0)



####### Plotting CDF
#cdf_x_axis=[10*x for x in range(100)]
#cdf_x_axis=[5*x for x in range(100)] #10*x in cycles, but / 2 to convert ot NS
dist_xaxis=[x for x in range(40)]
ifig,iax=plt.subplots()
linewidth=3
iax.bar(dist_xaxis, mbw_hist, width=linewidth);
iax.set_ylim([0,14000])

#iax.legend(ncol=1)
plt.ylabel('Sampled Memory Bandwidth Distribution\n')
plt.xlabel('\nMemory Bandwidth (GB/s)')
plt.grid(color='gray', linestyle='--', linewidth=0.2, zorder=0)


ifig.set_size_inches(20,12)

ifig.savefig('mbw_hist.png', bbox_inches='tight')



