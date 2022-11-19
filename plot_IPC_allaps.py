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
parser.add_argument('--infile', type=str, default='ipcs.txt')  
parser.add_argument('--ylabel', type=str, default='IPC')  
args = parser.parse_args()
infile = args.infile
ylab = args.ylabel
ylab='IPC'
#ylab='Average Memory Latency'
#ylab='Memory Bandwidth Utilization'
print('infile: '+infile)
print('ylabel: '+ylab)
#outdir = args.outdir

#cxl_delays=['0','30','50','100']

appNames=[]
DDR_ipcs=[]
CXL_ipcs=[]

#toparr = [[[[[] for m in range(cxlen)] for l in range(mclen)] for k in range(ptlen)] for j in range(rblen)]



def getindex(elem, arr):
    for i in range(len(arr)):
        if str(arr[i])==elem:
            return i
    print('didnt find elem '+elem+' in arr')
    exit
    return -1

#field_names=[]
#field_names.append('maxIR')
#field_names.append('MBW')
#field_names.append('ST')
#field_names.append('NIC_RB_Miss_Rate')
#field_names.append('Memhog_ipcs')
#field_names.append('Memhog_L3_Miss_Rate')
#field_names.append('Memhog_cCycle_ratio')
#field_names.append('core_rb_mr')
#field_names.append('NIC_LB_Miss_Rate')
#field_names.append('MBW_Util')
#field_names.append('avg_e2e')
#field_names.append('90%_e2e')

#color_list= [[['black'] for l in range(ddioslen)] for k in range(ptlen)]
#
#color_list[getindex('2',partitions)][getindex('clean',ddio_setups)]='#A89AE4'
#color_list[getindex('6',partitions)][getindex('clean',ddio_setups)]='#7C67D6'
#color_list[getindex('12',partitions)][getindex('clean',ddio_setups)]= '#42347E'
#
#color_list[getindex('2',partitions)][getindex('nocl',ddio_setups)]='#ABBFB0'
#color_list[getindex('6',partitions)][getindex('nocl',ddio_setups)]='#799A82'
#color_list[getindex('12',partitions)][getindex('nocl',ddio_setups)]='#3D5A45'
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
        tmp=line.split(',')
        appNames.append(tmp[0]);
        DDR_ipcs.append(float(tmp[1]));
        CXL_ipcs.append(float(tmp[2]));

        #mem latency in cycles, convert to ns by /2
        #DDR_ipcs.append(float(tmp[1])/2);
        #CXL_ipcs.append(float(tmp[2])/2);
        
        line=f.readline();

    print('toparr populated')


    matplotlib.rcParams.update({'font.size': 20})


    
        
    ifig,iax=plt.subplots()
    #iax.set_title(field_names[i])
    #X_axis = np.arange(pslen*rblen)
    X_axis = np.arange(len(appNames))

    barwidth = 0.3
    alval=1
    iax.bar(X_axis-(barwidth/2), DDR_ipcs,edgecolor='black',alpha=alval, color=color_list[0],label='DDR Memory', width=barwidth, zorder=5)
    iax.bar(X_axis+(barwidth/2), CXL_ipcs,edgecolor='black',alpha=alval, color=color_list[4],label='CXL Memory', width=barwidth, zorder=5)
    
    plt.xticks(X_axis, appNames)
    #iax.legend(ncol=2, reversed(handles), reversed(labels), loc='upper left')
    iax.legend(ncol=2,bbox_to_anchor=[0.5,1.15], loc='center')

    plt.setp(iax.get_xticklabels(), rotation=15, horizontalalignment='center')
    ifig.set_size_inches(10,4)
    plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int)
    plt.ylabel(ylab)

    ifig.savefig(ylab+'.png', bbox_inches='tight')

    


    ### just plot one ideal mc
    #iax.bar(X_axis-0.4+(barwidth*3), tmparr[0][0],edgecolor='black', alpha=0.5, color="black", label='ideal', width=barwidth)

    #for j in range(1,len(mcs)):
    #    for k in range(len(ddio_setups)):
    ##for k in range(len(ddio_setups)):
    ##    if(k==1): #plot ideal here, for legend alignment reasons..
    ##        lname = 'Ideal DDIO'
    ##        xoffset=barwidth*(getindex('ideal',partitions));
    ##        iax.bar(X_axis-0.2+(xoffset), tmparr[j][k],edgecolor='black', alpha=alval, color=color_list[getindex('ideal',partitions)][k], label=lname, width=barwidth, zorder=5)

    ##        
    ##    for j in range(ptlen):
    ##        alval=1
    ##        z_order=5
    ##        lname = 'DDIO '+partitions[j]+' ways'
    ##        if 'clean' in ddio_setups[k]:
    ##            lname = lname + '+ Sweeper'
    ##            if (i==0 or i==3):
    ##                z_order=0
    ##        if (not ('ideal' in partitions[j])): # skip plotting ideal
    ##            if ('ideal' in partitions[j]):
    ##                lname = 'Ideal DDIO'
    ##            xoffset = barwidth*(j)
    ##            iax.bar(X_axis-0.2+(xoffset), tmparr[j][k],edgecolor='black', alpha=alval, color=color_list[j][k], label=lname, width=barwidth, zorder=z_order)

    ##    #else:
    ##    #    for k in (range(len(ddio_setups))):
    ##    #        alval=0
    ##    #        if 'nocl' in ddio_setups[k]:
    ##    #            alval=1
    ##    #        if (not (('nocl' in ddio_setups[k]) and ('ideal' in partitions[j]))): # plot just one ideal

    ##    #            xoffset = barwidth*(j)
    ##    #            iax.bar(X_axis-0.2+(xoffset), tmparr[j][k],edgecolor='black', alpha=alval, color=color_list[j][k], label=str(partitions[j]), width=barwidth)


    ###iax.bar(X_axis-0.4+(barwidth*3), tmparr[0][0],edgecolor='black', alpha=0.5, color="black", label='ideal', width=barwidth)
    ##plt.xticks(X_axis, xtick_labels)
    ###iax.legend(ncol=2, reversed(handles), reversed(labels), loc='upper left')
    ##iax.legend(ncol=2,bbox_to_anchor=[0.5,1.4], loc='center')

    ##plt.setp(iax.get_xticklabels(), rotation=15, horizontalalignment='right')
    ##ifig.set_size_inches(10,4)
    ##plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int)

    ######Y LABELS#####
    ##if 'maxIR' in field_names[i]:
    ##    plt.ylabel('L3fwd Throughput (Mrps)')
    ##if 'MBW' in field_names[i]:
    ##    plt.ylabel('avg Memory BW (GB/s)')
    ##if 'ST' in field_names[i]:
    ##    plt.ylabel('avg service time (ns)')
    ##if 'e2e' in field_names[i]:
    ##    plt.ylabel('avg e2e latency (ns)')




    ##ifig.savefig(field_names[i]+'.png', bbox_inches='tight')
    ###ifig.savefig(field_names[i]+'.png',dpi=1000)
        


exit
    
