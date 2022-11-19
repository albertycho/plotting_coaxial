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
parser.add_argument('--outdir', type=str, default='cxl_plots')
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
mbw_cxl_cap = DDR_BW * num_ddr_cont*4



#mcs = ['8','16']
#cxl_delays=['0','60','120','200','300']
#
#mclen=len(mcs)
#cxlen=len(cxl_delays)
#
##toparr = [[[[] for l in range(ddioslen)] for j in range(wlen)] for k in range(qdlen)]
#toparr = [[[] for i in range(cxlen)] for j in range(mclen)]


#mcs=['DDR','CXL_60','CXL_120','CXL_200']
#mcs=['DDR','CXL_60','CXL_120']
mcs=['DDR','CXL_60']
mclen=len(mcs)
toparr = [[] for i in range(mclen)]


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
field_names.append('IPC')
field_names.append('MBW')
field_names.append('MBW_UTIL')
field_names.append('MPKI')
field_names.append('L3_MR')
field_names.append('wr_lat_avg')
field_names.append('rd_lat_avg')
field_names.append('all_lat_avg')
#field_names.append('svc_time_avg')
color_list=[ '#ABBFB0', '#799A82', '#3D5A45','darkslategrey', '#A89AE4', '#7C67D6', 'darkslateblue','#42347E']
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
        tmp=line.split(',')
        #### parse setup
        su=tmp[0]
        mc_type=su.split('C_')[1]
        #su = tmp[0].split('_')
        #nmc=su[0].replace('mc','')
        #cxd=su[1].replace('cxd','')

 
        #print(mc)
        ##### get indexes in array
        mci = getindex(mc_type,mcs)
        #cxi = getindex(cxd,cxl_delays)

        validSetup=True
        if mci==-1:
            line=f.readline();
            continue


        if (len(toparr[mci])!=0):
            print('ERROR: duplicate setup found, '+tmp[0])

        bw_multiplier = 1;
        if('CXL' in mcs[mci]):
            bw_multiplier = 4 ;
        mbw_cap = DDR_BW * num_ddr_cont* bw_multiplier

        wrlat_in_ns = float(tmp[5])/freq_in_GHz
        rdlat_in_ns = float(tmp[6])/freq_in_GHz
        alllat_in_ns = float(tmp[7])/freq_in_GHz
        
        if'CXL_60' in mc_type:
            wrlat_in_ns = wrlat_in_ns+30
            rdlat_in_ns = rdlat_in_ns+30
            alllat_in_ns=alllat_in_ns+30
        
        toparr[mci].append(float(tmp[1]))   ##0 IPC
        toparr[mci].append(float(tmp[2]) * 2 * num_ddr_cont * bw_multiplier )   ##1 MBW, *2 for DDR5 (2 logical channel, printed stat is for 1 logical channel)
        toparr[mci].append((float(tmp[2]) * 2) / DDR_BW)   ##2 MBW UTIL
        toparr[mci].append(float(tmp[3]))   ##3 MPKI
        toparr[mci].append(float(tmp[4]))   ##4 L3MR
        toparr[mci].append(wrlat_in_ns)   ##5 wrlat
        toparr[mci].append(rdlat_in_ns)   ##6 rdlat
        toparr[mci].append(alllat_in_ns)   ##7 all lat
        #toparr[mci].append(float(tmp[8]))   ##8 Service Time

        #print(str(mci)+str(qdi)+str(dsi))

        line=f.readline();

    print('toparr populated')
    
    os.system('mkdir '+outdir)
    os.chdir(outdir)

    matplotlib.rcParams.update({'font.size': 50})

    xtick_labels=[]
    xtick_labels.append('DDR')
    for k in range(1,mclen):
        tmp_del_cycle = float(mcs[k].split('CXL_')[1])
        #tmp_del_cycle = 60
        del_in_ns = str(int(tmp_del_cycle / freq_in_GHz))
        xtick_labels.append('CXL_'+del_in_ns+'ns')



    for i in range(len(field_names)):

        #tmparr = [[[] for l in range(ddioslen)] for k in range(qdlen)]
        #tmparr = [[] for l in range(ddioslen)]

        #Making two arrays(CXL and DDR), just for color coding plot
        #   For DDR, put 0 for CXL values, and vice versa for CXL
        
        tmparr = []
        tmparr_CXL=[]
        tmparr_baselineDDR=[]
        tmparr_CXL.append(0)
        tmparr_baselineDDR.append(toparr[0][i])
        tmparr.append(toparr[0][i])
        for j in range(1,mclen,1):
            #print(str(j)+','+str(i))
            tmparr.append(toparr[j][i])
            tmparr_CXL.append(toparr[j][i])
            tmparr_baselineDDR.append(0)


        #for j in range(mclen):
        #    for k in range(cxlen):
        #        tmparr.append(toparr[j][k][i])
        #        #if ((j==0 and k==0) or (j==1 and (k==1 or k==2))):
        #        #if ((j==0 and k==0) or ((j==1) and (k!=0))):
        #        if ((j==1) and (k!=0)):
        #            tmparr_CXL.append(toparr[j][k][i])
        #            tmparr_baselineDDR.append(0)
        #        else:
        #            if((plotAll) and (not (j==0 and k==0))):
        #                tmparr_CXL.append(0)
        #                tmparr_baselineDDR.append(0)

        
        ifig,iax=plt.subplots()
        #iax.set_title(field_names[i])
        X_axis = np.arange(mclen)

        barwidth = 0.6
        ### just plot one ideal mc

        #for j in range(1,len(mcs)):
        #    for k in range(len(ddio_setups)):
        alval=1
        #if(plotAll):
        #    iax.bar(X_axis, tmparr, edgecolor='black', alpha=alval, hatch='', color=color_list[0], width=barwidth, zorder=0)
        iax.bar(X_axis, tmparr_baselineDDR, edgecolor='black', alpha=alval, hatch='/', color=color_list[0], label='DDR BW: '+str(int(mbw_ddr_cap))+'GB', width=barwidth, zorder=5)
        iax.bar(X_axis, tmparr_CXL, edgecolor='black', alpha=alval, hatch='/', color=color_list[4], label='CXL  BW: '+str(int(mbw_cxl_cap))+'GB', width=barwidth, zorder=5)

        plt.xticks(X_axis, xtick_labels, rotation=50, horizontalalignment='right')
        iax.legend(bbox_to_anchor=(0.5,1.2) , ncol=1, loc='center')#, columnspacing=)
        plt.setp(iax.get_xticklabels(), horizontalalignment='right')
        #ifig.set_size_inches(16,3)
        ifig.set_size_inches(20,16.5)
        #plt.subplots_adjust(bottom=0.2)
        plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int, zorder=0, axis='y')

        plt.xlabel('\nType_Delay(ns)')

        plt.ylabel(field_names[i] + '\n')
        ####Y LABELS#####
        if 'IPC' in field_names[i]:
            plt.ylabel('IPC\n')
        if 'MBW' in field_names[i]:
            plt.ylabel('Memory Bandwidth (GB/s)\n')
        if 'MBW_UTIL' in field_names[i]:
            plt.ylabel('MBW Utilization')
        if 'wr_lat_avg' in field_names[i]:
            plt.ylabel('wr_lat_avg (ns) \n')
        if 'rd_lat_avg' in field_names[i]:
            plt.ylabel('rd_lat_avg (ns) \n')
        if 'all_lat_avg' in field_names[i]:
            plt.ylabel('all_lat_avg (ns) \n')




        ifig.savefig('CXL_'+field_names[i]+'.png', bbox_inches='tight')
        #ifig.savefig(field_names[i]+'.png',dpi=1000)
        


exit
    
