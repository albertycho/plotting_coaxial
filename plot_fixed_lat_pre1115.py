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
parser.add_argument('--infile', type=str, default='cxl_stats.csv')  
parser.add_argument('--outdir', type=str, default='fixlat_plots')
parser.add_argument('--plotAll', type=bool, default=False)
args = parser.parse_args()
infile = args.infile
outdir = args.outdir
plotAll = args.plotAll

print(infile)

freq_in_GHz = 2.0
num_ddr_cont=8
DDR_BW = 38.4
mbw_ddr_cap = DDR_BW * num_ddr_cont
mbw_cxl_cap = DDR_BW * num_ddr_cont*2



#mcs = ['8','16']
#cxl_delays=['0','60','120','200','300']
#
#mclen=len(mcs)
#cxlen=len(cxl_delays)
#
##toparr = [[[[] for l in range(ddioslen)] for j in range(wlen)] for k in range(qdlen)]
#toparr = [[[] for i in range(cxlen)] for j in range(mclen)]


#mcs=['fixed','r100','r200','r300','r400']
#FOR EVEN RADIUS
mcs=['fixed','r100','r200','r300']
mc_tags=['fixed','r50','r100','r150'] # radius in ns (divide cycles by 2, as f=2GHz)
#mcs=['fixed','r200','r400']
#mc_tags=['fixed','r100','r200'] # radius in ns (divide cycles by 2, as f=2GHz)




#FOR SEVERE&LESS FREQUENT TAIL
#mcs=['fixed','tv1','tv2','tv3','tv4','tv5']
#mc_tags=['fixed','tail_50ns','tail_100ns','tail_150ns', 'tail_200ns', 'tail_250ns'] # radius in ns (divide cycles by 2, as f=2GHz)
#mc_tags=['fixed','tail_1','tail_2','tail_3', 'tail_4', 'tail_5'] # radius in ns (divide cycles by 2, as f=2GHz)


mclen=len(mcs)
toparr = [[] for i in range(mclen)]
avg_lats =[[] for i in range(mclen)] ## for plotting partial plots


def getindex(elem, arr):
    for i in range(len(arr)):
        if str(arr[i])==elem:
            return i
    print('didnt find elem '+elem+' in arr')
    exit
    return -1


#field_names=[]
#field_names.append('IPC')
#field_names.append('MBW')
#field_names.append('MBW_UTIL')
#field_names.append('MPKI')
#field_names.append('L3_MR')
#field_names.append('wr_lat_avg')
#field_names.append('rd_lat_avg')
#field_names.append('all_lat_avg')
##field_names.append('svc_time_avg')
#color_list=[ '#ABBFB0', '#799A82', '#3D5A45','darkslategrey', '#A89AE4', '#7C67D6', 'darkslateblue','#42347E']
color_list=['#17becf','#1f77b4','#2ca02c', '#9467bd','#ff7f0e','#d62728' ]
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
    while line:
        if('setup' in line):
            line=f.readline();
            continue
        tmp=line.split(',')
        #### parse setup
        su=tmp[0]
        tmp2=su.split('_')
        mc_type=tmp2[0]
        print(tmp2)
        avg_lat= int(tmp2[1])
        mci = getindex(mc_type,mcs)

        validSetup=True
        if mci==-1:
            line=f.readline();
            continue

        #assert(len(toparr[mci]) == int(avg_lat/100));
        
        if(avg_lat <700 and avg_lat > 250):
            toparr[mci].append(float(tmp[2]))   ## store CPI
            avg_lats[mci].append(int(avg_lat / freq_in_GHz))   ## store x-axis (plot partial)

        line=f.readline();

    print('toparr populated')
    
    os.system('mkdir '+outdir)
    os.chdir(outdir)

    matplotlib.rcParams.update({'font.size': 50})

    xtick_labels=[]
    for i in range(len(toparr[0])):
        xtick_labels.append(str(i*50))
        
    ifig,iax=plt.subplots()
    #iax.set_title(field_names[i])
    X_axis = np.arange(len(toparr[0]))
    

    barwidth = 4
    ### just plot one ideal mc

    #for j in range(1,len(mcs)):
    #    for k in range(len(ddio_setups)):
    alval=1
    
    for i in range(0,mclen):
        #iax.plot(X_axis,toparr[i],label=(mcs[i]),linewidth=barwidth, zorder=5);
        #iax.plot(avg_lats[i],toparr[i],label=(mc_tags[i]),linewidth=barwidth, color=color_list[i], zorder=5);
        iax.plot(avg_lats[i],toparr[i],label=(mc_tags[i]),linewidth=barwidth, zorder=5);
        #iax.plot(avg_lats[i],toparr[i],label=(mc_tags[i]),linewidth=barwidth, zorder=5);


    #plt.xticks(X_axis, xtick_labels, rotation=50, horizontalalignment='right')
    iax.legend(bbox_to_anchor=(0.5,1.1) , ncol=2, loc='center')#, columnspacing=)
    #plt.setp(iax.get_xticklabels(), horizontalalignment='right')
    #ifig.set_size_inches(16,3)
    ifig.set_size_inches(20,16.5)
    #plt.subplots_adjust(bottom=0.2)
    plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int, zorder=0, axis='both')
    
    #iax.set_ylim([0,6])
    iax.set_ylim(ymin=0, ymax=3.1)
    plt.xlabel('\nAverage Memory Latency(ns)')

    plt.ylabel('Cycles Per Instruction\n')
    #####Y LABELS#####
    #if 'IPC' in field_names[i]:
    #    plt.ylabel('IPC\n')
    #if 'MBW' in field_names[i]:
    #    plt.ylabel('Memory Bandwidth (GB/s)\n')
    #if 'MBW_UTIL' in field_names[i]:
    #    plt.ylabel('MBW Utilization')
    #if 'wr_lat_avg' in field_names[i]:
    #    plt.ylabel('wr_lat_avg (ns) \n')
    #if 'rd_lat_avg' in field_names[i]:
    #    plt.ylabel('rd_lat_avg (ns) \n')
    #if 'all_lat_avg' in field_names[i]:
    #    plt.ylabel('all_lat_avg (ns) \n')




    ifig.savefig('fixedlat_plot.png', bbox_inches='tight')
    #ifig.savefig(field_names[i]+'.png',dpi=1000)
        


exit
    
