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
parser.add_argument('--infile', type=str, default='mlatstats.csv')  
#parser.add_argument('--ylabel', type=str, default='IPC')  
args = parser.parse_args()
infile = args.infile
#ylab = args.ylabel
#ylab='IPC'
#ylab='Average Memory Latency'
#ylab='Memory Bandwidth Utilization'
#print('infile: '+infile)
#print('ylabel: '+ylab)
#outdir = args.outdir

#cxl_delays=['0','30','50','100']

cxl_delay = 60

appNames=[]

#fields = ['IPC', 'Memory BW Utilization', 'Average Memory Latency']


DDR_mbws=[]
DDR_mlats=[]
lowload_mlats=[]
dummy_for_MBW_label=[]
#toparr = [[[[[] for m in range(cxlen)] for l in range(mclen)] for k in range(ptlen)] for j in range(rblen)]

ddr5_BW = 38.4


def getGeomean(iarr):
    a=np.array(iarr);
    return a.prod()**(1.0/len(a))



def getindex(elem, arr):
    for i in range(len(arr)):
        if str(arr[i])==elem:
            return i
    print('didnt find elem '+elem+' in arr')
    exit
    return -1


#color_list[getindex('ideal',partitions)][getindex('clean',ddio_setups)] ='#C26989'
color_list=[ '#ABBFB0', '#799A82', '#3D5A45','darkslategrey', '#A89AE4', '#7C67D6', 'darkslateblue','#42347E']



#xtick_labels is appNames
#xtick_labels=[]
#for l in range(len(appNames)):
#    xtick_labels.append()

if infile in os.listdir('.'):
    f=open(infile,'r')
    line=f.readline();
    line=f.readline();
    while line:
        if ('####' in line):
            line=f.readline();
            continue
        tmp=line.split(',')
        appNames.append(tmp[0]);


        DDR_mbws.append((float(tmp[1])) / ddr5_BW)
        DDR_mlats.append(float(tmp[2]) /2)
        lowload_mlats.append(float(tmp[3]) /2)
        dummy_for_MBW_label.append(0)

        ## add empty entry to split server app and spec
        if(tmp[0]=='xapian'):
            appNames.append('');
            DDR_mbws.append(0)
            DDR_mlats.append(0)
            lowload_mlats.append(0)
            dummy_for_MBW_label.append(0)



        line=f.readline();

    print('toparr populated')


    matplotlib.rcParams.update({'font.size': 12})

    #appNames.append('Geometric\nMean')
    #GM_DDR_mbw= getGeomean(DDR_mbws)
    #DDR_mbws.append(GM_DDR_mbw)
    #GM_DDR_mlat= getGeomean(DDR_mlats)
    #DDR_mlats.append(GM_DDR_mlat)
    #GM_LL_mlat= getGeomean(lowload_mlats)
    #lowload_mlats.append(GM_LL_mlat)
    #dummy_for_MBW_label.append(0) 



    ################# PLOT latency breakdown ##################3

    #ifig,iax=plt.subplots()
    ifig,(iax1,iax2)=plt.subplots(2)
    #iax2=iax.twinx()
    #iax.set_title(field_names[i])
    #X_axis = np.arange(pslen*rblen)
    X_axis = np.arange(len(appNames))

    barwidth = 0.5
    alval=1
    iax1.bar(X_axis, DDR_mlats,edgecolor='black',alpha=alval, color=color_list[4],label='Queuing Delay', width=barwidth, zorder=4)
    iax1.bar(X_axis, lowload_mlats,edgecolor='black',alpha=alval, color=color_list[0],label='Access Service Time', width=barwidth, zorder=5)
    #iax1.bar(X_axis, dummy_for_MBW_label,edgecolor='black',alpha=alval, color='cornflowerblue',label='MBW Utilization', width=barwidth, zorder=5)
            
 
    #plt.xticks(X_axis, appNames, fontsize=10)
    #iax1.legend(ncol=3,bbox_to_anchor=[0.5,1.3], loc='center', fontsize=16)
    #iax1.legend(ncol=1,bbox_to_anchor=[1,0.9], loc='right', fontsize=16)
    iax1.legend(ncol=1,loc='best')
    iax1.set_xticks([], [])
    iax1.set_ylabel('Average Memory\nAccess Latency (ns)')
    iax1.set_ylim(0,200)
    iax1.text(-0.5,202,'356ns',zorder=5, fontsize=10)

    #plt.setp(iax1.get_xticklabels(), rotation=45, ha='right', fontsize=13)
    #plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int, zorder=1)
    iax1.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int, zorder=1)

    #ifig.savefig('mlat_qd_st_DDR.png', bbox_inches='tight')



    ################# PLOT MBW ##################3

    #ifig,iax=plt.subplots()
    #iax.set_title(field_names[i])
    #X_axis = np.arange(pslen*rblen)
    X_axis = np.arange(len(appNames))

    barwidth = 0.5
    alval=1
    iax2.bar(X_axis, DDR_mbws,edgecolor='black',alpha=alval,label='MBW Utilization', width=barwidth, zorder=5, color='cornflowerblue')
    #iax2.bar(X_axis, DDR_mbws,edgecolor='black',alpha=alval,label='MBW Utilization', width=barwidth, zorder=5, color='cornflowerblue')
 
    plt.xticks(X_axis, appNames, fontsize=10)
    #iax.legend(ncol=2, reversed(handles), reversed(labels), loc='upper left')
    #iax.legend(ncol=2,bbox_to_anchor=[0.5,1.15], loc='center', fontsize=20)
    #iax2.legend(ncol=2,bbox_to_anchor=[0.5,1.17], loc='center', fontsize=16)
    #iax2.legend(ncol=1,loc='best')
    #iax3=iax2.twinx()
    #iax3.set_ylabel('Memory Bandwidth\nUtilization')
    iax2.set_ylabel('Memory Bandwidth\nUtilization')
    #iax.set_ylabel('Memory Bandwidth Utilization')
    #iax.set_ylim(0,200)
    #iax.text(-0.5,201,'356ns',zorder=5, fontsize=10)

    #plt.setp(iax.get_xticklabels(), rotation=35, horizontalalignment='center')
    plt.setp(iax2.get_xticklabels(), rotation=45, ha='right', fontsize=13)
    dx = 0.1; dy = 0.05 
    offset = matplotlib.transforms.ScaledTranslation(dx, dy, ifig.dpi_scale_trans) 
    
    ifig.set_size_inches(10,4)
    plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int, zorder=1)
    #plt.ylabel(fields[ii])

    #ifig.savefig('all_apps_mbw_DDR.png', bbox_inches='tight')
    ifig.savefig('mlat_bd_and_mbw_DDR.png', bbox_inches='tight')




exit
    
