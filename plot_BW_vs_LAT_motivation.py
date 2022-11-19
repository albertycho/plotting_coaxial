#!/usr/bin/env python3

import os
import sys
import csv
import math
import statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['agg.path.chunksize'] = 10000
import matplotlib.pyplot as plt 

import argparse

from matplotlib.pyplot import figure


parser = argparse.ArgumentParser()
parser.add_argument('--infile', type=str, default='collected_stats.csv')  
parser.add_argument('--outdir', type=str, default='BW_LAT_plots')
parser.add_argument('--plotAll', type=bool, default=False)
args = parser.parse_args()
infile = args.infile
outdir = args.outdir
plotAll = args.plotAll

print(infile)

freq_in_GHz = 2.0
num_ddr_cont=1
mbw_ddr_cap = 23.84 * num_ddr_cont


#toparr = [[] for i in range(mclen)]

MBWS = []
MBW_UTILS = []
AVGLATS = []
LAT90S = []
IPCS = []


def getindex(elem, arr):
    for i in range(len(arr)):
        if str(arr[i])==elem:
            return i
    print('didnt find elem '+elem+' in arr')
    exit
    return -1

def get_ds_index(elem):
    if 'clean' in elem:
        if ('clean' in ddio_setups):
            return 1
        else:
            return -1
    else:
        return 0



field_names=[]
field_names.append('MBW')
field_names.append('MBW_UTIL')
field_names.append('AVGLAT')
field_names.append('LAT90')
field_names.append('IPC')
#field_names.append('MPKI')
#field_names.append('L3_MR')
#field_names.append('wr_lat_avg')
#field_names.append('rd_lat_avg')
#field_names.append('all_lat_avg')
#field_names.append('svc_time_avg')
#color_list=[ '#ABBFB0', '#799A82', '#3D5A45','darkslategrey', '#A89AE4', '#7C67D6', 'darkslateblue','#42347E']
#color_list=[ '#3D5A45','darkslategrey', '#7C67D6', 'darkslateblue','#42347E']
color_list=[ '#3D5A45','darkslategrey', '#A89AE4', '#42347E', 'darkslateblue']
#colors = [ '#ABBFB0', '#799A82', '#3D5A45',       '#C26989', '#6e92f2']
# greens: '#a4c1ab','#3b6d56',                                                  
#purples warm: '#dba5ce','#7B476F','#451539',                                   
# oranges: '#FFC966','#e58606','#ffa500'                                        
# reds: '#4B0215',                                                              
# blues:'#6e92f2',  

#purples:  '#A89AE4', '#7C67D6', '#42347E',

if infile in os.listdir('.'):
    f=open(infile,'r')
    line=f.readline();
    line=f.readline();
    expected_cores=1;
    while line:
        tmp=line.split(',')
        #### parse setup
        assert(expected_cores==int(tmp[0]))
        expected_cores=expected_cores+1

 
        bw_multiplier = 1;
        mbw_cap = 23.84 * num_ddr_cont* bw_multiplier

        avgLat_in_ns = float(tmp[2])/freq_in_GHz
        Lat90_in_ns = float(tmp[3])/freq_in_GHz
        
        MBWS.append(float(tmp[1]));
        MBW_UTILS.append(float(tmp[1]) / mbw_cap);
        AVGLATS.append(avgLat_in_ns);
        LAT90S.append(Lat90_in_ns);
        IPCS.append(float(tmp[4]));
        
       #print(str(mci)+str(qdi)+str(dsi))

        line=f.readline();

    print('toparr populated')
    
    os.system('mkdir '+outdir)
    os.chdir(outdir)

    matplotlib.rcParams.update({'font.size': 30})

    xtick_labels=[]
    for k in range(1,len(MBWS)+1):
        if(k%2==0):
            xtick_labels.append(str(k))
        else:
            xtick_labels.append('')

    
    #put arrays in a top array, for easier loop coding
    toparr=[]
    toparr.append(MBWS)
    toparr.append(MBW_UTILS)
    toparr.append(AVGLATS)
    toparr.append(LAT90S)
    toparr.append(IPCS)
    #field_names = ['MBW','LAT','IPC']

    for i in range(len(field_names)):
        #### when overlapping avg lat and 90% lat. 
        if(i==3): # lat90 is plotted with avglat, skip
            continue
        
        ifig,iax=plt.subplots()
        #iax.set_title(field_names[i])
        X_axis = np.arange(len(toparr[i]))

        barwidth = 0.6
        ### just plot one ideal mc

        #for j in range(1,len(mcs)):
        #    for k in range(len(ddio_setups)):
        alval=1

        #### when overlapping avg lat and 90% lat. 
        if(i==2): ### plot avg with 90% lat
            iax.bar(X_axis, toparr[i], label='Average Latency', edgecolor='black', alpha=alval, color=color_list[i], width=barwidth, zorder=5)
            iax.bar(X_axis, toparr[i+1], label='90% Latency', edgecolor='black', alpha=alval, color=color_list[i+1], width=barwidth, zorder=4)
            #iax.legend(bbox_to_anchor=(0.5,1.2) , ncol=1, loc='upper left')#, columnspacing=)
            iax.legend(ncol=1, loc='upper left')#, columnspacing=)
        else:
            iax.bar(X_axis, toparr[i], edgecolor='black', alpha=alval, color=color_list[i], width=barwidth, zorder=5)

        plt.xticks(X_axis, xtick_labels, horizontalalignment='center')
        #iax.legend(bbox_to_anchor=(0.5,1.2) , ncol=1, loc='center')#, columnspacing=)
        plt.setp(iax.get_xticklabels(), horizontalalignment='center')
        #ifig.set_size_inches(16,3)
        ifig.set_size_inches(20,12)
        #plt.subplots_adjust(bottom=0.2)
        plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int, zorder=0, axis='y')

        #plt.xlabel('\nType_Delay(ns)')

        plt.ylabel(field_names[i] + '\n')
        plt.xlabel('\nNumber of Cores Running Workload')
        ####Y LABELS#####
        if 'IPC' in field_names[i]:
            plt.ylabel('IPC\n')
        if 'MBW' in field_names[i]:
            plt.ylabel('Memory Bandwidth (GB/s)\n')
        if 'MBW_UTIL' in field_names[i]:
            plt.ylabel('Memory Bandwidth Utilization\n')
        if 'AVGLAT' in field_names[i]:
            plt.ylabel('Memory Access Latency (ns) \n')
        #if 'AVGLAT' in field_names[i]:
        #    plt.ylabel('Average Mem Access Latency (ns) \n')
        #if 'LAT90' in field_names[i]:
        #    plt.ylabel('90Percentile Mem Access Latency (ns) \n')





        ifig.savefig(field_names[i]+'_motivation.pdf', bbox_inches='tight')
        #ifig.savefig(field_names[i]+'.png',dpi=1000)
        


exit
    
