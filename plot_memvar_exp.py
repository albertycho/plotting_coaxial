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
parser.add_argument('--infile', type=str, default='allstats.csv')  
#parser.add_argument('--ylabel', type=str, default='IPC')  
args = parser.parse_args()
infile = args.infile

#cxl_delays=['0','30','50','100']

cxl_delay = 60

appNames=[]

fixed_ipcs=[]
d350_ipcs=[]
d450_ipcs=[]
d550_ipcs=[]

#350_pci=[]
#450_pci=[]
#550_pci=[]

d350_norm=[]
d450_norm=[]
d550_norm=[]

#toparr = [[[[[] for m in range(cxlen)] for l in range(mclen)] for k in range(ptlen)] for j in range(rblen)]

ddr5_BW = 38.4


def getindex(elem, arr):
    for i in range(len(arr)):
        if str(arr[i])==elem:
            return i
    print('didnt find elem '+elem+' in arr')
    exit
    return -1

#def getGeomean(iarr):
#    a=np.array(iarr);
#    return a.prod()**(1.0/len(a))
def getGeomean(iarr):
    a=np.array(iarr);
    #np.delete(a, 0)
    na=a;
    i=0
    while (i<len(a)):
    #for i in range(len(a)):
        if(a[i]==0):
            na=np.delete(a,[i])
            a=na
        else:
            i=i+1
    return na.prod()**(1.0/len(na))
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
        if ('####' in line):
            line=f.readline();
            continue
        tmp=line.split(',')
        appNames.append(tmp[0]);
    
        fixed_ipcs.append(float(tmp[1]));  
        d350_ipcs.append(float(tmp[2]));
        d450_ipcs.append(float(tmp[3]));
        d550_ipcs.append(float(tmp[4]));

        ###CPI
        #d350_norm.append(float(tmp[1]) /  float(tmp[2]));
        #d450_norm.append(float(tmp[1]) /  float(tmp[3]));
        #d550_norm.append(float(tmp[1]) /  float(tmp[4]));
        
        ##IPC
        d350_norm.append(float(tmp[2]) / float(tmp[1])  );
        d450_norm.append(float(tmp[3]) / float(tmp[1])  );
        d550_norm.append(float(tmp[4]) / float(tmp[1])  );
        
        line=f.readline();

    print('toparr populated')
    print(appNames)

    matplotlib.rcParams.update({'font.size': 20})


    GM_fixed_ipcs= getGeomean(fixed_ipcs)
    GM_350_ipcs= getGeomean(d350_ipcs)
    GM_450_ipcs= getGeomean(d450_ipcs)
    GM_550_ipcs= getGeomean(d550_ipcs)
    

    fixed_ipcs.append(GM_fixed_ipcs)
    d350_ipcs.append(GM_350_ipcs)
    d450_ipcs.append(GM_450_ipcs)
    d550_ipcs.append(GM_550_ipcs)
   
    ###CPI
    #d350_norm.append( GM_fixed_ipcs / GM_350_ipcs)
    #d450_norm.append( GM_fixed_ipcs / GM_450_ipcs)
    #d550_norm.append( GM_fixed_ipcs / GM_550_ipcs)
   
    #appNames.append('')
    #d350_norm.append(0) 
    #d450_norm.append(0)
    #d550_norm.append(0)    

    appNames.append('gm')
    ##IPC
    d350_norm.append( GM_350_ipcs / GM_fixed_ipcs  )
    d450_norm.append( GM_450_ipcs / GM_fixed_ipcs  )
    d550_norm.append( GM_550_ipcs / GM_fixed_ipcs  )



    ifig,iax=plt.subplots()
    #iax.set_title(field_names[i])
    #X_axis = np.arange(pslen*rblen)
    X_axis = np.arange(len(appNames))

    barwidth = 0.2
    alval=1

    d350_bar = iax.bar(X_axis-(barwidth), d350_norm,edgecolor='black',alpha=alval, color=color_list[4],label='(100ns,350ns)', width=barwidth, zorder=6)
    d450_bar = iax.bar(X_axis, d450_norm,edgecolor='black',alpha=alval, color=color_list[5],label='(75ns,450ns)', width=barwidth, zorder=6)
    d550_bar = iax.bar(X_axis+(barwidth), d550_norm,edgecolor='black',alpha=alval, color=color_list[7],label='(50ns,550ns)', width=barwidth, zorder=6)
    #d350_bar = iax.bar(X_axis-(barwidth), d350_norm,edgecolor='black',alpha=alval, color=color_list[4],label='80% 100ns, 20% 350ns', width=barwidth, zorder=6)
    #d450_bar = iax.bar(X_axis, d450_norm,edgecolor='black',alpha=alval, color=color_list[5],label='80% 75ns,   20% 450ns', width=barwidth, zorder=6)
    #d550_bar = iax.bar(X_axis+(barwidth), d550_norm,edgecolor='black',alpha=alval, color=color_list[7],label='80% 50ns,   20% 550ns', width=barwidth, zorder=6)
    
    iax.axhline(y=1,color='black',linestyle='--')
    
    #iax.margins(y=0.2)
    #print('dummy')
    #tmp_count=0
    #for p in cxl_bar: ## for main eval
    #    height = p.get_height();
    #    iax.text(x=p.get_x() - (barwidth), y=height+0.05, s="{}".format(perf_gains[tmp_count]), fontsize=10)
    #    tmp_count=tmp_count+1
 
    #for p in ddr_bar: ## for low load
    #    height = p.get_height();
    #    iax.text(x=p.get_x() + (barwidth/2), y=height+0.05, s="{}".format(perf_gains[tmp_count]), fontsize=10)
    #    tmp_count=tmp_count+1
 
    plt.xticks(X_axis, appNames, fontsize=20)
    #iax.legend(ncol=2, reversed(handles), reversed(labels), loc='upper left')
    iax.legend(ncol=3,bbox_to_anchor=[0.42,1.15], loc='center')

    plt.setp(iax.get_xticklabels(), rotation=35, horizontalalignment='center')
    ifig.set_size_inches(10,4)
    #plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int)
    #plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int, zorder=1, axis='y', alpha=0.3) #for pdf
    plt.grid(color='gray', linestyle='--', linewidth=0.7, markevery=int, zorder=1, axis='y', alpha=0.9) #for png

    plt.ylabel('Performance normalized \nto fixed latency',fontsize=20, labelpad=10)

    ifig.savefig('memvar_exp_plot_ipc.png', bbox_inches='tight')
    ifig.savefig('memvar_exp_plot_ipc.pdf', bbox_inches='tight')

    print(d350_norm) 
    print(d450_norm) 
    print(d550_norm) 

exit
    
