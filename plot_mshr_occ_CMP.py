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


f_mem_lat = open('mem_lats.csv','w')

numMSHR=129

mshr_occ_hist_exist=False;
occhist_DDR=[0]*numMSHR;
occhist_CXL=[0]*numMSHR;

zsimout = open('zsim.out_DDR')

#sancheck counter
num_llc_banks=0



line = zsimout.readline()
while line:
    if 'l3-' in line:
        num_llc_banks+=1
        while not 'occHist' in line:
            line=zsimout.readline()
        for i in range(numMSHR):
            line=zsimout.readline()
            tmp=line.split(': ')
            assert(int(tmp[0])==i)
            occhist_DDR[i]+=int(tmp[1])

    line=zsimout.readline()

print('DDR LLC BANKS: '+str(num_llc_banks)+' (sancheck)\n')
zsimout.close()

num_llc_banks=0


zsimout = open('zsim.out_CXL')

line = zsimout.readline()

line = zsimout.readline()
while line:
    if 'l3-' in line:
        num_llc_banks+=1
        while not 'occHist' in line:
            line=zsimout.readline()
        for i in range(numMSHR):
            line=zsimout.readline()
            tmp=line.split(': ')
            assert(int(tmp[0])==i)
            occhist_CXL[i]+=int(tmp[1])

    line=zsimout.readline()

print('CXL LLC BANKS: '+str(num_llc_banks)+' (sancheck)\n')
zsimout.close()


####### Plotting CDF

cdf_x_axis=[x for x in range(numMSHR)]
ifig,iax=plt.subplots()
#plt.plot(cdf_x_axis,occhist_DDR, label="DDR")
#plt.plot(cdf_x_axis,occhist_CXL, label="CXL")

plt.plot(cdf_x_axis[40:], occhist_DDR[40:], label="DDR")
plt.plot(cdf_x_axis[40:], occhist_CXL[40:], label="CXL")

iax.legend(ncol=1)
plt.grid(color='gray', linestyle='--', linewidth=0.2, zorder=0)
ifig.savefig('occ_hist_cmp.png')



