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
server_apps=['moses','imgdnn','xapian','sphinx','masstree','mica','bc','pr','bfs','tc','sssp','cc','monetDB']
cxl_delay = 60

appNames=[]

ipc_gains=[]
sa_ipc_gains=[]
sp_ipc_gains=[]
#fields = ['IPC', 'Memory BW Utilization', 'Average Memory Latency']


DDR_mbws=[]
DDR_mlats=[]
lowload_mlats=[]
dummy_for_MBW_label=[]

CXL_mbws=[]
CXL_mlats=[]
#toparr = [[[[[] for m in range(cxlen)] for l in range(mclen)] for k in range(ptlen)] for j in range(rblen)]

ddr5_BW = 38.4


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
        is_SA = True; ## is server app?
        if ('####' in line):
            line=f.readline();
            continue
        tmp=line.split(',')
        appNames.append(tmp[0]);
        SA_i = getindex(tmp[0], server_apps)
        if (SA_i==-1):
            is_SA=False;


        DDR_mbws.append((float(tmp[1])) / ddr5_BW)
        DDR_mlats.append(float(tmp[2]) /2)
        CXL_mbws.append((float(tmp[4])) / ddr5_BW)
        CXL_mlats.append((float(tmp[5])+cxl_delay) /2)

        lowload_mlats.append(float(tmp[3]) /2)
        dummy_for_MBW_label.append(0)
        
        ipc_gains.append(float(tmp[6]))
        if(is_SA):
            sa_ipc_gains.append(float(tmp[6]))
        else:
            sp_ipc_gains.append(float(tmp[6]))


        ## add empty entry to split server app and spec
        if(tmp[0]=='xapian'):
            appNames.append('');
            DDR_mbws.append(0)
            DDR_mlats.append(0)
            CXL_mbws.append(0)
            CXL_mlats.append(0)
            
            ipc_gains.append(0)

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
    
    gm_sa_ipc_gain=getGeomean(sa_ipc_gains)
    gm_sp_ipc_gain=getGeomean(sp_ipc_gains)
    gm_ipc_gain=getGeomean(ipc_gains)

    ipc_gains.append(0)
    ipc_gains.append(gm_sa_ipc_gain)
    ipc_gains.append(gm_sp_ipc_gain)
    ipc_gains.append(gm_ipc_gain)

    ################# PLOT latency breakdown ##################3

    cxl_30nsdel=[]
    for i in range(len(lowload_mlats)):
        if(lowload_mlats[i]!=0):
            cxl_30nsdel.append(30)
        else:
            cxl_30nsdel.append(0)

    ### overlapping mlat with low lowad lat makes the plot fat...
    DDR_QD =[]
    for i in range(len(DDR_mlats)):
            DDR_QD.append(DDR_mlats[i] - lowload_mlats[i])
    CXL_QD =[]
    CXL_QD_bottom=[]
    for i in range(len(CXL_mlats)):
        if(lowload_mlats[i]!=0):
            CXL_QD.append((CXL_mlats[i] - lowload_mlats[i])-30)
            CXL_QD_bottom.append(lowload_mlats[i]+30)
        else:
            CXL_QD.append(0)
            CXL_QD_bottom.append(0)

    ##making empty space to sync with IPC plot
    for i in range(4):
        lowload_mlats.append(0)
        DDR_QD.append(0)
        cxl_30nsdel.append(0)
        CXL_QD.append(0)
        CXL_QD_bottom.append(0)

        DDR_mbws.append(0)
        CXL_mbws.append(0)

    appNames.append('')
    appNames.append('gm_server')
    appNames.append('gm_desktop')
    appNames.append('gm_all')

    #ifig,iax=plt.subplots()
    ifig,(iax0,iax1,iax2)=plt.subplots(3, gridspec_kw={'height_ratios': [1,1,1]})
    ylabel_size=15
    

    ##### plot IPC gains
    X_axis = np.arange(len(appNames))
    barwidth = 0.5
    alval=1
    iax0.bar(X_axis, ipc_gains, edgecolor='black', alpha=alval, color=color_list[5], width=barwidth, zorder=5)
    
    #if(max(ipc_gains) > 2):
    iax0.set_ylim(ymax=2.3)
    iax0.text(0,2.32,str(round(ipc_gains[0],1)),zorder=5, fontsize=12, ha='center');
    iax0.text(1,2.32,str(round(ipc_gains[1],1)),zorder=5, fontsize=12, ha='center');
    iax0.text(28,ipc_gains[28]+0.1,str(round(ipc_gains[28],1)),zorder=5, fontsize=12, ha='center');
    iax0.text(29,ipc_gains[29]+0.1,str(round(ipc_gains[29],1)),zorder=5, fontsize=12, ha='center');
    iax0.text(30,ipc_gains[30]+0.1,str(round(ipc_gains[30],1)),zorder=5, fontsize=12, ha='center');
    #gm_text='geoemeans:\n server\n  desktop\n   all'
    props = dict(boxstyle='round', facecolor=color_list[4], alpha=0.5)
    #iax0.text(28,1.9,'geoemans',zorder=5, fontsize=12, ha='left', bbox=props);
    #iax0.text(28,0.9,'server',zorder=5, fontsize=12, ha='left', bbox=props);

    iax0.set_xticks([], [])
    iax0.set_ylabel('Normalized\nPerformance', fontsize=ylabel_size)
    #iax0.set_ylim(0,200)

    #plt.setp(iax1.get_xticklabels(), rotation=45, ha='right', fontsize=13)
    #plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int, zorder=1)
    major_ticks = np.arange(0, 2.5, 0.5)
    iax0.set_yticks(major_ticks)
    iax0.grid(color='gray', linestyle='--', linewidth=0.2, markevery=float, zorder=1)


    ##### plot mlat breakdown for qd and st

    X_axis = np.arange(len(appNames))

    barwidth = 0.3
    alval=1
    iax1.bar(X_axis-(barwidth*0.55), lowload_mlats,edgecolor='black',alpha=alval, color=color_list[0],label='Access Service Time', width=barwidth, zorder=5)
    iax1.bar(X_axis-(barwidth*0.55), DDR_QD,edgecolor='black',alpha=alval, color=color_list[4],label='Queuing Delay', width=barwidth, zorder=4, bottom=lowload_mlats)
    iax1.bar(X_axis+(barwidth*0.55), cxl_30nsdel,edgecolor='black',alpha=alval, color='#bb7900',label='CXL Interface Delay', width=barwidth, zorder=4, bottom=lowload_mlats)
    iax1.bar(X_axis+(barwidth*0.55), CXL_QD,edgecolor='black',alpha=alval, color=color_list[4], width=barwidth, zorder=4, bottom=CXL_QD_bottom)
    iax1.bar(X_axis+(barwidth*0.55), lowload_mlats,edgecolor='black',alpha=alval, color=color_list[0], width=barwidth, zorder=5) #redundant, no label, use same color

    #iax1.bar(X_axis, dummy_for_MBW_label,edgecolor='black',alpha=alval, color='cornflowerblue',label='MBW Utilization', width=barwidth, zorder=5)
            
 
    #plt.xticks(X_axis, appNames, fontsize=10)
    #iax1.legend(ncol=3,bbox_to_anchor=[0.5,1.3], loc='center', fontsize=16)
    #iax1.legend(ncol=1,bbox_to_anchor=[1,0.9], loc='right', fontsize=16)
    #iax1.legend(ncol=3,loc='best')
    iax1.legend(ncol=1,loc='best',fontsize=15)
    iax1.set_xticks([], [])
    iax1.set_ylabel('Average Memory\nAccess Latency (ns)', fontsize=ylabel_size)
    iax1.set_ylim(0,200)
    iax1.text(0,181,'356ns',zorder=5, fontsize=12)

    #plt.setp(iax1.get_xticklabels(), rotation=45, ha='right', fontsize=13)
    #plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int, zorder=1)
    iax1.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int, zorder=1)

    #ifig.savefig('mlat_qd_st_DDR.png', bbox_inches='tight')



    ################# PLOT MBW ##################3

    #ifig,iax=plt.subplots()
    #iax.set_title(field_names[i])
    #X_axis = np.arange(pslen*rblen)
    X_axis = np.arange(len(appNames))

    alval=1
    iax2.bar(X_axis-(barwidth*0.55), DDR_mbws,edgecolor='black',alpha=alval,label='DDR', width=barwidth, zorder=5, color='cornflowerblue')
    iax2.bar(X_axis+(barwidth*0.55), CXL_mbws,edgecolor='black',alpha=alval,label='CXL', width=barwidth, zorder=5, color='#27557b')
    #iax2.bar(X_axis, DDR_mbws,edgecolor='black',alpha=alval,label='MBW Utilization', width=barwidth, zorder=5, color='cornflowerblue')
 
    plt.xticks(X_axis, appNames, fontsize=10)
    #iax.legend(ncol=2, reversed(handles), reversed(labels), loc='upper left')
    iax2.legend(ncol=1,loc='best',fontsize=15)
    #iax3=iax2.twinx()
    #iax3.set_ylabel('Memory Bandwidth\nUtilization')
    iax2.set_ylabel('Memory Bandwidth\nUtilization', fontsize=ylabel_size)
    #iax.set_ylabel('Memory Bandwidth Utilization')
    #iax.set_ylim(0,200)
    #iax.text(-0.5,201,'356ns',zorder=5, fontsize=10)

    #plt.setp(iax.get_xticklabels(), rotation=35, horizontalalignment='center')
    plt.setp(iax2.get_xticklabels(), rotation=45, ha='right', fontsize=13)
    dx = 0.1; dy = 0.05 
    offset = matplotlib.transforms.ScaledTranslation(dx, dy, ifig.dpi_scale_trans) 

    
    #iax2.text(26,-0.6,'(geomeans only for performance)',zorder=5, fontsize=12)
    
    iax2.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int, zorder=1, axis='y')
    ifig.set_size_inches(20,8)
    #plt.ylabel(fields[ii])


    #ifig.savefig('all_apps_mbw_DDR.png', bbox_inches='tight')
    ifig.savefig('mlat_bd_and_mbw_CMP.png', bbox_inches='tight')




exit
    
