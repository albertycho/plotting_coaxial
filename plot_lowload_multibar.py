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
parser.add_argument('--infile', type=str, default='all_ll_stats.csv')  
parser.add_argument('--ll', type=int, default=0)  
#parser.add_argument('--ylabel', type=str, default='IPC')  
args = parser.parse_args()
infile = args.infile
ll=args.ll
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
fields = ['IPC', 'Memory BW Utilization', 'IPC_gains']

d1p_DDR_ipcs=[]
d1p_CXL_ipcs=[]
d1p_IPC_gains=[]

d16p_DDR_ipcs=[]
d16p_CXL_ipcs=[]
d16p_IPC_gains=[]

d32p_DDR_ipcs=[]
d32p_CXL_ipcs=[]
d32p_IPC_gains=[]

d64p_DDR_ipcs=[]
d64p_CXL_ipcs=[]
d64p_IPC_gains=[]

#d128p_DDR_ipcs=[]
#d128p_CXL_ipcs=[]
d128p_IPC_gains=[]



sa_d1p_DDR_ipcs=[]
sa_d1p_CXL_ipcs=[]
sa_d1p_IPC_gains=[]
sa_d16p_DDR_ipcs=[]
sa_d16p_CXL_ipcs=[]
sa_d16p_IPC_gains=[]
sa_d32p_DDR_ipcs=[]
sa_d32p_CXL_ipcs=[]
sa_d32p_IPC_gains=[]
sa_d64p_DDR_ipcs=[]
sa_d64p_CXL_ipcs=[]
sa_d64p_IPC_gains=[]
sa_d128p_IPC_gains=[]

sp_d1p_DDR_ipcs=[]
sp_d1p_CXL_ipcs=[]
sp_d1p_IPC_gains=[]
sp_d16p_DDR_ipcs=[]
sp_d16p_CXL_ipcs=[]
sp_d16p_IPC_gains=[]
sp_d32p_DDR_ipcs=[]
sp_d32p_CXL_ipcs=[]
sp_d32p_IPC_gains=[]
sp_d64p_DDR_ipcs=[]
sp_d64p_CXL_ipcs=[]
sp_d64p_IPC_gains=[]
sp_d128p_IPC_gains=[]




server_apps=['moses','imgdnn','xapian','sphinx','masstree','mica','bc','pr','bfs','tc','sssp','cc','monetDB']
#toparr = [[[[[] for m in range(cxlen)] for l in range(mclen)] for k in range(ptlen)] for j in range(rblen)]

ddr5_BW = 38.4


def getindex(elem, arr):
    for i in range(len(arr)):
        if str(arr[i])==elem:
            return i
    print('didnt find elem '+elem+' in arr')
    exit
    return -1
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
#def getGeomean(iarr):
#    a=np.array(iarr);
#    #np.delete(a, 0)
#    na=a;
#    for i in range(len(a)):
#        if(a[i]==0):
#            na=np.delete(a,[i])
#    return na.prod()**(1.0/len(na))

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
#color_list=[ '#ABBFB0', '#799A82', '#3D5A45','#DA70D6', '#A89AE4', '#7C67D6', 'darkslateblue','#42347E']



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
        d1p_DDR_ipcs.append(float(tmp[1]));
        d1p_CXL_ipcs.append(float(tmp[2]));
        if((float(tmp[1]) * float(tmp[2]))==0):
            d1p_IPC_gains.append(0)
        else:
            d1p_IPC_gains.append(((float(tmp[2]) / float(tmp[1]))))
        
        d16p_DDR_ipcs.append(float(tmp[3]));
        d16p_CXL_ipcs.append(float(tmp[4]));
        if((float(tmp[3]) * float(tmp[4]))==0):
            d16p_IPC_gains.append(0)
        else:
            d16p_IPC_gains.append(((float(tmp[4]) / float(tmp[3]))))
        
        d32p_DDR_ipcs.append(float(tmp[5]));
        d32p_CXL_ipcs.append(float(tmp[6]));
        if((float(tmp[5]) * float(tmp[6]))==0):
            d32p_IPC_gains.append(0)
        else:
            d32p_IPC_gains.append(((float(tmp[6]) / float(tmp[5]))))
       
        d64p_DDR_ipcs.append(float(tmp[7]));
        d64p_CXL_ipcs.append(float(tmp[8]));
        if((float(tmp[7]) * float(tmp[8]))==0):
            d64p_IPC_gains.append(0)
        else:
            d64p_IPC_gains.append(((float(tmp[8]) / float(tmp[7]))))

        d128p_IPC_gains.append(float(tmp[9]))

        if(is_SA):
            sa_d1p_DDR_ipcs.append(float(tmp[1]));
            sa_d1p_CXL_ipcs.append(float(tmp[2]));
            if((float(tmp[1]) * float(tmp[2]))==0):
                sa_d1p_IPC_gains.append(0)
            else:
                sa_d1p_IPC_gains.append(((float(tmp[2]) / float(tmp[1]))))
            
            sa_d16p_DDR_ipcs.append(float(tmp[3]));
            sa_d16p_CXL_ipcs.append(float(tmp[4]));
            if((float(tmp[3]) * float(tmp[4]))==0):
                sa_d16p_IPC_gains.append(0)
            else:
                sa_d16p_IPC_gains.append(((float(tmp[4]) / float(tmp[3]))))
            
            sa_d32p_DDR_ipcs.append(float(tmp[5]));
            sa_d32p_CXL_ipcs.append(float(tmp[6]));
            if((float(tmp[5]) * float(tmp[6]))==0):
                sa_d32p_IPC_gains.append(0)
            else:
                sa_d32p_IPC_gains.append(((float(tmp[6]) / float(tmp[5]))))
       
            sa_d64p_DDR_ipcs.append(float(tmp[7]));
            sa_d64p_CXL_ipcs.append(float(tmp[8]));
            if((float(tmp[7]) * float(tmp[8]))==0):
                sa_d64p_IPC_gains.append(0)
            else:
                sa_d64p_IPC_gains.append(((float(tmp[8]) / float(tmp[7]))))

            sa_d128p_IPC_gains.append(float(tmp[9]))

        else: ## geomean for non server app
            sp_d1p_DDR_ipcs.append(float(tmp[1]));
            sp_d1p_CXL_ipcs.append(float(tmp[2]));
            if((float(tmp[1]) * float(tmp[2]))==0):
                sp_d1p_IPC_gains.append(0)
            else:
                sp_d1p_IPC_gains.append(((float(tmp[2]) / float(tmp[1]))))
            
            sp_d16p_DDR_ipcs.append(float(tmp[3]));
            sp_d16p_CXL_ipcs.append(float(tmp[4]));
            if((float(tmp[3]) * float(tmp[4]))==0):
                sp_d16p_IPC_gains.append(0)
            else:
                sp_d16p_IPC_gains.append(((float(tmp[4]) / float(tmp[3]))))
            
            sp_d32p_DDR_ipcs.append(float(tmp[5]));
            sp_d32p_CXL_ipcs.append(float(tmp[6]));
            if((float(tmp[5]) * float(tmp[6]))==0):
                sp_d32p_IPC_gains.append(0)
            else:
                sp_d32p_IPC_gains.append(((float(tmp[6]) / float(tmp[5]))))
       
            sp_d64p_DDR_ipcs.append(float(tmp[7]));
            sp_d64p_CXL_ipcs.append(float(tmp[8]));
            if((float(tmp[7]) * float(tmp[8]))==0):
                sp_d64p_IPC_gains.append(0)
            else:
                sp_d64p_IPC_gains.append(((float(tmp[8]) / float(tmp[7]))))     
            sp_d128p_IPC_gains.append(float(tmp[9]))
        
        ## add empty entry to split server app and spec
        if(tmp[0]=='xapian'):
            appNames.append('')
            d1p_DDR_ipcs.append(0) 
            d1p_CXL_ipcs.append(0)
            d1p_IPC_gains.append(0)
            
            d16p_DDR_ipcs.append(0)
            d16p_CXL_ipcs.append(0)
            d16p_IPC_gains.append(0)
            
            d32p_DDR_ipcs.append(0)
            d32p_CXL_ipcs.append(0)
            d32p_IPC_gains.append(0)
            
            d64p_DDR_ipcs.append(0)
            d64p_CXL_ipcs.append(0)
            d64p_IPC_gains.append(0)
            d128p_IPC_gains.append(0)

        line=f.readline();

    print('toparr populated')
    print(appNames)


    
    appNames.append('')
    d1p_DDR_ipcs.append(0) 
    d1p_CXL_ipcs.append(0)
    d1p_IPC_gains.append(0)
    
    d16p_DDR_ipcs.append(0)
    d16p_CXL_ipcs.append(0)
    d16p_IPC_gains.append(0)
    
    d32p_DDR_ipcs.append(0)
    d32p_CXL_ipcs.append(0)
    d32p_IPC_gains.append(0)
    
    d64p_DDR_ipcs.append(0)
    d64p_CXL_ipcs.append(0)
    d64p_IPC_gains.append(0)
    d128p_IPC_gains.append(0)

    GM_d1p_ipcg= getGeomean(d1p_IPC_gains)
    GM_d16p_ipcg= getGeomean(d16p_IPC_gains)
    GM_d32p_ipcg= getGeomean(d32p_IPC_gains)
    GM_d64p_ipcg= getGeomean(d64p_IPC_gains)
    GM_d128p_ipcg= getGeomean(d128p_IPC_gains)

    GM_sa_d1p_ipcg= getGeomean(sa_d1p_IPC_gains)
    GM_sa_d16p_ipcg= getGeomean(sa_d16p_IPC_gains)
    GM_sa_d32p_ipcg= getGeomean(sa_d32p_IPC_gains)
    GM_sa_d64p_ipcg= getGeomean(sa_d64p_IPC_gains)
    GM_sa_d128p_ipcg= getGeomean(sa_d128p_IPC_gains)

    GM_sp_d1p_ipcg= getGeomean(sp_d1p_IPC_gains)
    GM_sp_d16p_ipcg= getGeomean(sp_d16p_IPC_gains)
    GM_sp_d32p_ipcg= getGeomean(sp_d32p_IPC_gains)
    GM_sp_d64p_ipcg= getGeomean(sp_d64p_IPC_gains)
    GM_sp_d128p_ipcg= getGeomean(sp_d128p_IPC_gains)


    d1p_IPC_gains.append(GM_sa_d1p_ipcg)
    d16p_IPC_gains.append(GM_sa_d16p_ipcg)
    d32p_IPC_gains.append(GM_sa_d32p_ipcg)
    d64p_IPC_gains.append(GM_sa_d64p_ipcg)
    d128p_IPC_gains.append(GM_sa_d128p_ipcg)



    d1p_IPC_gains.append(GM_sp_d1p_ipcg)
    d16p_IPC_gains.append(GM_sp_d16p_ipcg)
    d32p_IPC_gains.append(GM_sp_d32p_ipcg)
    d64p_IPC_gains.append(GM_sp_d64p_ipcg)
    d128p_IPC_gains.append(GM_sp_d128p_ipcg)


    d1p_IPC_gains.append(GM_d1p_ipcg)
    d16p_IPC_gains.append(GM_d16p_ipcg)
    d32p_IPC_gains.append(GM_d32p_ipcg)
    d64p_IPC_gains.append(GM_d64p_ipcg)
    d128p_IPC_gains.append(GM_d128p_ipcg)

    print(d64p_IPC_gains)
    print('gmean_1P: '+str(GM_d1p_ipcg))
    print('gmean_16P: '+str(GM_d16p_ipcg))
    print('gmean_32P: '+str(GM_d32p_ipcg))
    print('gmean_64P: '+str(GM_d64p_ipcg))
   
    print('server gmean_1P: '+str(GM_sa_d1p_ipcg))
    print('server gmean_16P: '+str(GM_sa_d16p_ipcg))
    print('server gmean_32P: '+str(GM_sa_d32p_ipcg))
    print('server gmean_64P: '+str(GM_sa_d64p_ipcg))

    #exit (0)

    matplotlib.rcParams.update({'font.size': 20})



        #### Server Apps GeoMean



    appNames.append('gm_server')
    appNames.append('gm_cpu')
    appNames.append('gm_all')

    
    
    #color_list=[ '#ABBFB0', '#799A82', '#3D5A45','#DA70D6', '#A89AE4', '#7C67D6', 'darkslateblue','#42347E']
    #color_list=[ '#8c5279', '#bf77be', '#A89AE4','#7C67D6', '#42347E' ]
    color_list=[ 'lavender', '#bf77be', '#A89AE4','#7C67D6', '#42347E' ]

    ifig,iax=plt.subplots()
    #iax.set_title(field_names[i])
    #X_axis = np.arange(pslen*rblen)
    X_axis = np.arange(len(appNames))
    print(len(appNames))
    print(len(d1p_IPC_gains))
    print(len(d128p_IPC_gains))
    
    barwidth=0.15
    alval=1
    iax.bar(X_axis-(barwidth*2), d1p_IPC_gains,edgecolor='black',alpha=alval, color=color_list[0],label='1 core    (<1% util.)', width=barwidth, zorder=5)
    iax.bar(X_axis-(barwidth*1), d16p_IPC_gains,edgecolor='black',alpha=alval, color='thistle',label='16 cores (12.5% util.)', width=barwidth, zorder=5)
    iax.bar(X_axis+(barwidth*0), d32p_IPC_gains,edgecolor='black',alpha=alval, color=color_list[2],label='32 cores (25% util.)', width=barwidth, zorder=5)
    iax.bar(X_axis+(barwidth*1), d64p_IPC_gains,edgecolor='black',alpha=alval, color=color_list[3],label='64 cores (50% util.)', width=barwidth, zorder=5)
    iax.bar(X_axis+(barwidth*2), d128p_IPC_gains,edgecolor='black',alpha=alval, color=color_list[4],label='128 cores (100% util.)', width=barwidth, zorder=5)
  
    iax.margins(x=0.01)
    iax.set_ylim(ymax=2.05)
    iax.text(0.3,2.1,str(round(d128p_IPC_gains[0],1)),zorder=5, fontsize=12, ha='center')#, rotation=45);
    iax.text(1.3,2.1,str(round(d128p_IPC_gains[1],1)),zorder=5, fontsize=12, ha='center')#, rotation=45);

    plt.axhline(y=1, color='black', zorder=5, linestyle=':')
    plt.ylabel('Normalized Performance', fontsize=15.5)
    #iax.legend(ncol=2,bbox_to_anchor=[0.5,1.15], loc='center', fontsize=18)
    iax.legend(ncol=2, loc='best', fontsize=15, framealpha=0.4)
    plt.xticks(X_axis, appNames, fontsize=13)
    #iax.set_xticks(X_axis+0.1)
    labels = iax.get_xticklabels()

    #plt.xticks(X_axis, gm_x_axis_label, fontsize=10)
    #iax.legend(ncol=2, reversed(handles), reversed(labels), loc='upper left')

    #plt.setp(iax.get_xticklabels(), rotation=90, horizontalalignment='center', fontsize=14)
    plt.setp(iax.get_xticklabels(), rotation=45, ha='right', fontsize=14)
    #labels[len(labels)-1].set_fontsize(11)
    #labels[len(labels)-1].set_fontweight('bold')
    #for app in labels:
    #    if (getindex(app._text,server_apps)!=-1):
    #        app.set_fontweight('bold')
    #        app.set_fontsize(13)
    
    dx = 0.1; dy = 0.05 
    offset = matplotlib.transforms.ScaledTranslation(dx, dy, ifig.dpi_scale_trans) 
    # apply offset transform to all x ticklabels.
    for label in iax.xaxis.get_majorticklabels():
        label.set_transform(label.get_transform() + offset)

    ifig.set_size_inches(20,4)
    plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int, axis='y', alpha=0.4)
    #major_ticks = np.arange(0, max(max(d32p_IPC_gains),max(d64p_IPC_gains)), 0.2)
    major_ticks = np.arange(0,2.2, 0.2)
    iax.set_yticks(major_ticks)
    iax.tick_params(axis='both', which='major', labelsize=14)

    #ifig.savefig('lowload_multibar.png', bbox_inches='tight')
    ifig.savefig('lowload_multibar.pdf', bbox_inches='tight')
    ifig.savefig('lowload_multibar.png', bbox_inches='tight')

    

exit
    
