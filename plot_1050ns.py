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
parser.add_argument('--type', type=str, default='no')  
#parser.add_argument('--ylabel', type=str, default='IPC')  
args = parser.parse_args()
infile = args.infile
stype=args.type
is2X=False

legend_labels=[]
#ylab_str = 'Performance Normalized to\n DD'
if(is2X):
    legend_labels=['2X','4X','8X']
else:
    legend_labels=['10ns','30ns','50ns']



#cxl_delays=['0','30','50','100']

server_apps=['moses','imgdnn','xapian','sphinx','masstree','mica','bc','pr','bfs','tc','sssp','cc','monetDB']

cxl_delay = 60

appNames=[]

DDR_ipcs=[]
d2X_ipcs=[]
d4X_ipcs=[]
d8X_ipcs=[]
d2X_gains=[]
d4X_gains=[]
d8X_gains=[]

##server app gain
sa_d2X_gains=[]
sa_d4X_gains=[]
sa_d8X_gains=[]

##spec gain
sp_d2X_gains=[]
sp_d4X_gains=[]
sp_d8X_gains=[]




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
        is_SA = True; ## is server app?
        if ('####' in line):
            line=f.readline();
            continue
        tmp=line.split(',')
        appNames.append(tmp[0]);
        SA_i = getindex(tmp[0], server_apps)
        if (SA_i==-1):
            is_SA=False;
        #ipc
        DDR_ipcs.append(float(tmp[3]));
        d2X_ipcs.append(float(tmp[1]));
        d4X_ipcs.append(float(tmp[4]));
        d8X_ipcs.append(float(tmp[2]));

        d2X_gains.append(float(tmp[1])/ float(tmp[3]));
        d4X_gains.append(float(tmp[4])/ float(tmp[3]));
        d8X_gains.append(float(tmp[2])/ float(tmp[3]));
       
        if(is_SA): ##spec gain
            sa_d2X_gains.append(float(tmp[1]) / float(tmp[3])) 
            sa_d4X_gains.append(float(tmp[4]) / float(tmp[3]))
            sa_d8X_gains.append(float(tmp[2]) / float(tmp[3]))
        else:
            sp_d2X_gains.append(float(tmp[1]) / float(tmp[3]))
            sp_d4X_gains.append(float(tmp[4]) / float(tmp[3]))
            sp_d8X_gains.append(float(tmp[2]) / float(tmp[3]))

        #d2X_gains.append(float(tmp[1])/ float(tmp[4]));
        #d8X_gains.append(float(tmp[2])/ float(tmp[4]));
        if(tmp[0]=='xapian'):
            appNames.append('')
            DDR_ipcs.append(0)
            d2X_ipcs.append(0) 
            d4X_ipcs.append(0)
            d8X_ipcs.append(0)                
            d2X_gains.append(0) 
            d4X_gains.append(0)
            d8X_gains.append(0)

        
        line=f.readline();

    print('toparr populated')
    print(appNames)

    matplotlib.rcParams.update({'font.size': 20})

    DDR_arrs=[]
    CXL_arrs=[]

    appNames.append('')
    DDR_ipcs.append(0)
    d2X_ipcs.append(0) 
    d4X_ipcs.append(0)
    d8X_ipcs.append(0)                
    d2X_gains.append(0) 
    d4X_gains.append(0)
    d8X_gains.append(0)

    gm_sa_2X_gain=getGeomean(sa_d2X_gains)
    gm_sa_4X_gain=getGeomean(sa_d4X_gains)
    gm_sa_8X_gain=getGeomean(sa_d8X_gains)

    gm_sp_2X_gain=getGeomean(sp_d2X_gains)
    gm_sp_4X_gain=getGeomean(sp_d4X_gains)
    gm_sp_8X_gain=getGeomean(sp_d8X_gains)

    d2X_gains.append(gm_sa_2X_gain)
    d2X_gains.append(gm_sp_2X_gain)
    d4X_gains.append(gm_sa_4X_gain)
    d4X_gains.append(gm_sp_4X_gain)
    d8X_gains.append(gm_sa_8X_gain)
    d8X_gains.append(gm_sp_8X_gain)




    #appNames.append('')
    appNames.append('gm_server')
    appNames.append('gm_desktop')
    appNames.append('gm_all')

    GM_DDR_ipcs= getGeomean(DDR_ipcs)
    GM_2X_ipcs= getGeomean(d2X_ipcs)
    GM_4X_ipcs= getGeomean(d4X_ipcs)
    GM_8X_ipcs= getGeomean(d8X_ipcs)
    

    DDR_ipcs.append(GM_DDR_ipcs)
    d2X_ipcs.append(GM_2X_ipcs)
    d4X_ipcs.append(GM_4X_ipcs)
    d8X_ipcs.append(GM_8X_ipcs)

    #print(str(GM_DDR_ipcs))
    #print(str(GM_2X_ipcs))
    d2X_gains.append(GM_2X_ipcs / GM_DDR_ipcs)
    d4X_gains.append(GM_4X_ipcs/GM_DDR_ipcs)
    d8X_gains.append(GM_8X_ipcs/GM_DDR_ipcs)
   
    if(is2X):
        print('gm perfgain all 2X: '+str(GM_2X_ipcs / GM_DDR_ipcs))
        print('gm perfgain server 2X: '+str(gm_sa_2X_gain))
        print('gm perfgain all 8x: '+str(GM_8X_ipcs / GM_DDR_ipcs))
        print('gm perfgain server 8X: '+str(gm_sa_8X_gain))


    else:
        print('gm perfgain all 10ns: '+str(GM_2X_ipcs / GM_DDR_ipcs))
        print('gm perfgain server 10ns: '+str(gm_sa_2X_gain))
        print('gm perfgain all 50ns: '+str(GM_8X_ipcs / GM_DDR_ipcs))
        print('gm perfgain server 50ns: '+str(gm_sa_8X_gain))


    #d2X_gains.append(GM_2X_ipcs / GM_4X_ipcs)
    #d8X_gains.append(GM_8X_ipcs/GM_4X_ipcs)


    ifig,iax=plt.subplots()
    #iax.set_title(field_names[i])
    #X_axis = np.arange(pslen*rblen)
    X_axis = np.arange(len(appNames))
    #print(str(len(appNames)))
    #print(str(len(d2X_gains)))
    #print(d2X_gains)

    barwidth = 0.33
    alval=1

    ###plot all bars normalized to DDR
    #ddr_bar = iax.bar(X_axis-(barwidth/2), DDR_arrs[ii],edgecolor='black',alpha=alval, color=color_list[0],label='DDR Memory', width=barwidth, zorder=5)
    #d2X_bar = iax.bar(X_axis-(barwidth), d2X_gains,edgecolor='black',alpha=alval, color=color_list[4],label=legend_labels[0], width=barwidth, zorder=5)
    d4X_bar = iax.bar(X_axis, d4X_gains,edgecolor='black',alpha=alval, color=color_list[4],label=legend_labels[1], width=barwidth, zorder=5)
    d8X_bar = iax.bar(X_axis+(barwidth), d8X_gains,edgecolor='black',alpha=alval, color=color_list[5],label= legend_labels[2], width=barwidth, zorder=5)

    plt.axhline(y=1, color='black', zorder=5, linestyle=':')
    ###plotting normalized to 4X
    #d2X_bar = iax.bar(X_axis-(barwidth/2), d2X_gains,edgecolor='black',alpha=alval, color=color_list[4],label='2X', width=barwidth, zorder=6)
    #d8X_bar = iax.bar(X_axis+(barwidth/2), d8X_gains,edgecolor='black',alpha=alval, color=color_list[7],label='8X', width=barwidth, zorder=5)
    

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
 
    plt.xticks(X_axis, appNames, fontsize=8)
    my_yticks=np.arange(0,4,0.5)
    plt.yticks(my_yticks)
    #iax.set_yticks(np.arange(0, 3, 0.5))

    #iax.legend(ncol=3,bbox_to_anchor=[0.5,1.15], loc='center')
    iax.legend(ncol=3,bbox_to_anchor=[1,0.9], loc='right', fontsize=16)

    #plt.setp(iax.get_xticklabels(), rotation=35, horizontalalignment='center')
    plt.setp(iax.get_xticklabels(), rotation=55, ha='right', fontsize=16)
    dx =0.1; dy = 0 
    offset = matplotlib.transforms.ScaledTranslation(dx, dy, ifig.dpi_scale_trans) 
    for label in iax.xaxis.get_majorticklabels():
        label.set_transform(label.get_transform() + offset)

    #ifig.set_size_inches(10,4)
    ifig.set_size_inches(10,4)
    #plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int)
    plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int, axis='y', alpha=0.4)
    #plt.ylabel('Performance (IPC) Relative to \nCXL baseline(4X)',fontsize=15)
    plt.ylabel('Normalized Performance',fontsize=17, labelpad=10)

    iax.tick_params(axis='both', which='major', labelsize=14)
    if(is2X):
        ifig.savefig('2X8X_plot.png', bbox_inches='tight')
    else:
        ifig.savefig('1050ns_plot_1col.png', bbox_inches='tight')
        ifig.savefig('1050ns_plot_1col.pdf', bbox_inches='tight')


    

exit
    
