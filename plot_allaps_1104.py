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

DDR_ipcs=[]
CXL_ipcs=[]
perf_gains=[]
IPC_gains=[]

DDR_mbws=[]
CXL_mbws=[]

DDR_mlats=[]
CXL_mlats=[]

server_apps=['moses','imgdnn','xapian','sphinx','masstree','mica','bc','pr','bfs','tc','sssp','cc','monetDB']

sa_DDR_ipcs=[]
sa_CXL_ipcs=[]
sa_DDR_mbws=[]
sa_CXL_mbws=[]
sa_DDR_mlats=[]

sp_DDR_ipcs=[]
sp_CXL_ipcs=[]
sp_DDR_mbws=[]
sp_CXL_mbws=[]

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
#    #np.delete(a, 0)
#    na=a;
#    for i in range(len(a)):
#        if(a[i]==0):
#            na=np.delete(a,[i])
#    return na.prod()**(1.0/len(na))
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
def getArithmean(iarr):
    a=np.array(iarr);
    #a=iarr
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
    return na.sum()/(len(na))

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
        DDR_ipcs.append(float(tmp[1]));
        CXL_ipcs.append(float(tmp[2]));
        perf_gains.append(str(int((float(tmp[2]) / float(tmp[1]) -1)*100)))
        IPC_gains.append(((float(tmp[2]) / float(tmp[1]))))

        if('bfs' in tmp[0]):
            print('bfs IPC gain: '+str((float(tmp[2]) / float(tmp[1]))))
        if('lbm' in tmp[0]):
            print('lbm IPC gain: '+str((float(tmp[2]) / float(tmp[1]))))

        #mbw
        DDR_mbws.append((float(tmp[3]) ) / ddr5_BW);
        CXL_mbws.append((float(tmp[4]) ) / ddr5_BW);

        if(is_SA):
            sa_DDR_ipcs.append(float(tmp[1]));
            sa_CXL_ipcs.append(float(tmp[2]));
            sa_DDR_mbws.append((float(tmp[3]) ) / ddr5_BW);
            sa_CXL_mbws.append((float(tmp[4]) ) / ddr5_BW);
            sa_DDR_mlats.append(float(tmp[5])/2);
        else: ## geomean for non server app
            sp_DDR_ipcs.append(float(tmp[1]));
            sp_CXL_ipcs.append(float(tmp[2]));
            sp_DDR_mbws.append((float(tmp[3]) ) / ddr5_BW);
            sp_CXL_mbws.append((float(tmp[4]) ) / ddr5_BW);
       
        

        #mem latency in cycles, convert to ns by /2
        DDR_mlats.append(float(tmp[5])/2);
        CXL_mlats.append( (float(tmp[6]) + cxl_delay )/2);
        
        ## add empty entry to split server app and spec
        if(tmp[0]=='xapian'):
            appNames.append('')
            DDR_ipcs.append(0)
            CXL_ipcs.append(0)
            DDR_mbws.append(0)
            CXL_mbws.append(0)
            IPC_gains.append(0)
            perf_gains.append('')

        line=f.readline();

    print('toparr populated')
    print(appNames)

    matplotlib.rcParams.update({'font.size': 20})

    DDR_arrs=[]
    CXL_arrs=[]

    appNames.append('')
    #appNames.append('')


        #### Server Apps GeoMean
    sa_GM_DDR_ipcs= getGeomean(sa_DDR_ipcs)
    sa_GM_CXL_ipcs= getGeomean(sa_CXL_ipcs)
    sa_GM_DDR_mbw= getGeomean(sa_DDR_mbws)
    sa_GM_CXL_mbw= getGeomean(sa_CXL_mbws)
    sa_GM_DDR_mlat = getGeomean(sa_DDR_mlats)

    sa_GM_perf_gain = (sa_GM_CXL_ipcs / sa_GM_DDR_ipcs)
    sa_GM_perf_gain_str = str(int((100*sa_GM_perf_gain) - 100))
    print('Server App geoMean perfgain: '+str(sa_GM_perf_gain))

    #### Spec Apps GeoMean
    sp_GM_DDR_ipcs= getGeomean(sp_DDR_ipcs)
    sp_GM_CXL_ipcs= getGeomean(sp_CXL_ipcs)
    sp_GM_DDR_mbw= getGeomean(sp_DDR_mbws)
    sp_GM_CXL_mbw= getGeomean(sp_CXL_mbws)

    sp_GM_perf_gain = (sp_GM_CXL_ipcs / sp_GM_DDR_ipcs)
    sp_GM_perf_gain_str = str(int((100*sp_GM_perf_gain) - 100))
    print('Spec App geoMean perfgain: '+str(sp_GM_perf_gain))




    appNames.append('gmean_server')
    appNames.append('gmean_desktop')
    appNames.append('gmean_all')
    GM_DDR_ipcs= getGeomean(DDR_ipcs)
    #print(str(GM_DDR_ipcs))
    GM_CXL_ipcs= getGeomean(CXL_ipcs)

    GM_DDR_mbw= getGeomean(DDR_mbws)
    GM_CXL_mbw= getGeomean(CXL_mbws)

    GM_DDR_mlat= getGeomean(DDR_mlats)
    GM_CXL_mlat= getGeomean(CXL_mlats)

    ### give space bewtween geomean and the rest
    perf_gains.append(' ')
    DDR_ipcs.append(0) 
    CXL_ipcs.append(0)
    IPC_gains.append(0)
    
    DDR_mbws.append(0)
    CXL_mbws.append(0)
    
    DDR_mlats.append(0) 
    CXL_mlats.append(0)
    
    perf_gains.append(sa_GM_perf_gain_str)
    IPC_gains.append(sa_GM_perf_gain)
    DDR_ipcs.append(sa_GM_DDR_ipcs)
    CXL_ipcs.append(sa_GM_CXL_ipcs)
    
    DDR_mbws.append(sa_GM_DDR_mbw)
    CXL_mbws.append(sa_GM_CXL_mbw)


    perf_gains.append(sp_GM_perf_gain_str)
    IPC_gains.append(sp_GM_perf_gain)
    DDR_ipcs.append(sp_GM_DDR_ipcs)
    CXL_ipcs.append(sp_GM_CXL_ipcs)
    
    DDR_mbws.append(sp_GM_DDR_mbw)
    CXL_mbws.append(sp_GM_CXL_mbw)


    DDR_ipcs.append(GM_DDR_ipcs)
    CXL_ipcs.append(GM_CXL_ipcs)
    
    DDR_mbws.append(GM_DDR_mbw)
    CXL_mbws.append(GM_CXL_mbw)

    DDR_mlats.append(GM_DDR_mlat)
    CXL_mlats.append(GM_CXL_mlat)
    
    print('ddr_ipc gm: '+str(GM_DDR_ipcs))
    print('cxl_ipc gm: '+str(GM_CXL_ipcs))
    
    print('ddr_ipc gm SERVER: '+str(sa_GM_DDR_ipcs))
    print('cxl_ipc gm SERVER: '+str(sa_GM_CXL_ipcs))


    GM_perf_gain2 =  (GM_CXL_ipcs / GM_DDR_ipcs)
    GM_perf_gain_str = str(int((100*GM_perf_gain2) - 100))
    print('geoMean perfgain: '+str(GM_perf_gain2))
    print(GM_perf_gain_str)
    perf_gains.append(GM_perf_gain_str)
    IPC_gains.append(GM_perf_gain2)
   
    #print('gmean ipc_gain desktop app: '+str(sp_GM_perf_gain))
    
    print('baseline gmean mbw server app: '+str(sa_GM_DDR_mbw))
    print('baseline gmean mbw all app: '+str(GM_DDR_mbw))

    print('coaxial gmean mbw server app: '+str(sa_GM_CXL_mbw))
    print('coaxial gmean mbw all app: '+str(GM_CXL_mbw))
    
    am_mbw_all_app = getArithmean(DDR_mbws)
    am_mbw_sv_app = getArithmean(sa_DDR_mbws)
    cxlam_mbw_all_app = getArithmean(CXL_mbws)
    cxlam_mbw_sv_app = getArithmean(sa_CXL_mbws)
    print('baseline am mbw all app: ' + str(am_mbw_all_app))
    print('baseline am mbw server app: ' + str(am_mbw_sv_app))

    print('coaxial am mbw all app: ' + str(cxlam_mbw_all_app))
    print('coaxial am mbw server app: ' + str(cxlam_mbw_sv_app))
    
    print('geman_mlat server app: '+str(sa_GM_DDR_mlat))
    print('arithmean_mlat server app: '+str( sum(sa_DDR_mlats) / len(sa_DDR_mlats) ))

    #perf_gains.append(str(int((float(tmp[2]) / float(tmp[1]) -1)*100)))

    DDR_arrs.append(DDR_ipcs)
    DDR_arrs.append(DDR_mbws)
    DDR_arrs.append(DDR_mlats)
       
    CXL_arrs.append(CXL_ipcs)
    CXL_arrs.append(CXL_mbws)
    CXL_arrs.append(CXL_mlats)
    
    ### build separate geomean x axis label
    gm_x_axis_label=[]
    for ii in range(len(appNames) - 1 ):
        gm_x_axis_label.append('')
    gm_x_axis_label.append('Geo\nMean')


    for ii in range(len(fields)):

        ifig,iax=plt.subplots()
        #iax.set_title(field_names[i])
        #X_axis = np.arange(pslen*rblen)
        X_axis = np.arange(len(appNames))

        
        if(fields[ii]=='IPC_gains'):
            barwidth=0.5
            iax.bar(X_axis, IPC_gains,edgecolor='black',alpha=alval, color=color_list[4],label='IPC gain', width=barwidth, zorder=5)
            if(max(IPC_gains) > 2):
                iax.set_ylim(ymax=2.3)
                iax.text(0,2.32,str(round(IPC_gains[0],1)),zorder=5, fontsize=12, ha='center', rotation=45);
                iax.text(1,2.32,str(round(IPC_gains[1],1)),zorder=5, fontsize=12, ha='center', rotation=45);
            plt.ylabel('Normalized Performance',labelpad=10)
            #plt.axhline(0, color='black2)
        else:
            barwidth = 0.3
            alval=1
            ddr_bar = iax.bar(X_axis-(barwidth/2), DDR_arrs[ii],edgecolor='black',alpha=alval, color=color_list[0],label='DDR Memory', width=barwidth, zorder=5)
            cxl_bar = iax.bar(X_axis+(barwidth/2), CXL_arrs[ii],edgecolor='black',alpha=alval, color=color_list[4],label='CXL Memory', width=barwidth, zorder=5)
            if(ii==0):
                iax.margins(y=0.2)
                print('dummy')
                tmp_count=0
                for jj in range(len(cxl_bar)):
                    cxl_h = cxl_bar[jj].get_height();
                    ddr_h = ddr_bar[jj].get_height();
                    height = max(cxl_h, ddr_h)
                    iax.text(x=ddr_bar[jj].get_x()+(barwidth*1),y=height+0.05, s="{}".format(perf_gains[jj]), fontsize=13, horizontalalignment='center')
            #if(ll==0):
            #    for p in cxl_bar: ## for main eval
            #        height = p.get_height();
            #        iax.text(x=p.get_x() - (barwidth*0.25), y=height+0.05, s="{}".format(perf_gains[tmp_count]), fontsize=12, horizontalalignment='center')
            #        tmp_count=tmp_count+1
            #else: 
            #    for p in ddr_bar: ## for low load
            #        height = p.get_height();
            #        iax.text(x=p.get_x() + (barwidth*1), y=height+0.05, s="{}".format(perf_gains[tmp_count]), fontsize=14, horizontalalignment='center')
            #        tmp_count=tmp_count+1

            
            plt.ylabel(fields[ii])
            iax.legend(ncol=2,bbox_to_anchor=[0.5,1.15], loc='center', fontsize=18)
        plt.xticks(X_axis, appNames, fontsize=10)
        #iax.set_xticks(X_axis+0.1)
        labels = iax.get_xticklabels()

        #plt.xticks(X_axis, gm_x_axis_label, fontsize=10)
        #iax.legend(ncol=2, reversed(handles), reversed(labels), loc='upper left')

        #plt.setp(iax.get_xticklabels(), rotation=90, horizontalalignment='center', fontsize=14)
        plt.setp(iax.get_xticklabels(), rotation=45, ha='right', fontsize=13)
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

        ifig.set_size_inches(10,4)
        plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int)

        ifig.savefig(fields[ii]+'.png', bbox_inches='tight')

    

exit
    
