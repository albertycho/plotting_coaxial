#!/usr/bin/env python3

import os
import sys 
import csv 
import math
import statistics
import numpy as np
from os.path import exists
import matplotlib
import matplotlib.pyplot as plt 
import argparse

#%raw data: DDR avg, DDR stdev, CXL avg, CXL stdev
#% perlbench: 55.4	49.9	81.7	46.9
#% Moses: 262.5	222.0	124.0	99.9
#% mcf: 71.5	75.0	81.7	49.9
#% bfs: 81.3	89.3	84.6	53.6
#% bc: 135.2	165.0	92.2	64.8


#parser = argparse.ArgumentParser()
##parser.add_argument('--app', type=str, default='')  
##parser.add_argument('--ylabel', type=str, default='IPC')  
#args = parser.parse_args()
#appname = args.app
#btext=''
#if 'moses' in appname:
#    #btext='Baseline mean, stdev: 262, 222\nCoaXiaL  mean, stdev: 124, 100'
#    btext='    Baseline, CoaXiaL\nmean: 355, 124\nstdev: 355, 100'
#if 'bfs' in appname:
#    #btext='Baseline mean, stdev:   81,   90\nCoaXiaL  mean, stdev:   84,   53'
#    btext='    Baseline, CoaXiaL\nmean: 81, 84\nstdev: 90, 53'
#if 'bc' in appname:
#    #btext='Baseline mean, stdev: 135, 165\nCoaXiaL  mean, stdev:   92,   65'
#    btext='    Baseline, CoaXiaL\nmean: 135, 92\nstdev: 165, 65'
#if 'mcf' in appname:
#    #btext='Baseline mean, stdev:   71,   75\nCoaXiaL  mean, stdev:   82,   50'
#    btext='    Baseline, CoaXiaL\nmean: 71, 82\nstdev: 75, 50'
#if 'perlbench' in appname:
#    #btext='Baseline mean, stdev:   55,   50\nCoaXiaL  mean, stdev:   82,   47'
#    btext='    Baseline, CoaXiaL\nmean: 55, 82\nstdev: 50, 47'


apps=['moses','bc','bfs','mcf','perlbench']
btexts=['    Baseline, CoaXiaL\nmean: 355, 124\nstdev: 355, 100',
         '    Baseline, CoaXiaL\nmean: 135, 92\nstdev: 165, 65',
         '    Baseline, CoaXiaL\nmean: 81, 84\nstdev: 90, 53',
         '    Baseline, CoaXiaL\nmean: 71, 82\nstdev: 75, 50',
         '    Baseline, CoaXiaL\nmean: 55, 82\nstdev: 50, 47']



cdf_DDRs=[]
cdf_CXLs=[]
DDR_amats=[]
CXL_amats=[]






#### handle DDR
for app in apps:
    zsimout_DDR='zsim.out_DDR_'+app
    
    zsimout = open(zsimout_DDR)
    
    memlathist_exist=False;
    memlathist_DDR=[0]*200;
    memlathist_CXL=[0]*200;
    
    DDR_amat=0;
    CXL_amat=0;
    
    CXL_DELAY = 60
    
    
    wr_lat_total=0
    rd_lat_total=0
    rd_count=0
    wr_count=0
    accesses=0
    l3misses=0;
    l3hits=0;
    total_insts=0
    total_cycles=0
    
    #sancheck counter
    num_mem_con=0
    num_llc_banks=0
    
    
    
    line = zsimout.readline()
    while line:
        if 'OCore1-' in line:
            line=zsimout.readline()
            if not ' cycles:' in line:
                print('expected cycles for core but didnt find\n')
            tmp1=line.split(': ')[1]
            tmp2=int(tmp1.split(' #')[0])
            total_cycles +=tmp2
            
            line=zsimout.readline()
            line=zsimout.readline()
            
            if not 'instrs:' in line:
                print('expected instrs for core but didnt find\n')
            tmp1=line.split(': ')[1]
            tmp2=int(tmp1.split(' #')[0])
            total_insts +=tmp2
    
        if 'mem-' in line:
            #rd=0;
            #wr=0;
            #rdlat=0;
            #wrlat=0;
    
            wr_lat_total=0
            rd_lat_total=0
            rd_count=0
            wr_count=0
    
    
            rdl=zsimout.readline()
            wrl=zsimout.readline()
            rdlatl=zsimout.readline()
            wrlatl=zsimout.readline()
            if not 'rd:' in rdl:
                print('expected rd: in mem but not found\n')
            if not 'wr:' in wrl:
                print('expected wr: in mem but not found\n')
            if not 'rdlat:' in rdlatl:
                print('expected rdlat: in mem but not found\n')
            if not 'wrlat:' in wrlatl:
                print('expected wrlat: in mem but not found\n')
            tmp=rdl.split('rd:')[1]
            tmp=tmp.split('#')[0]
            rd_count=int(tmp)
            tmp=wrl.split('wr:')[1]
            tmp=tmp.split('#')[0]
            wr_count=int(tmp)
            tmp=rdlatl.split('rdlat:')[1]
            tmp=tmp.split('#')[0]
            rd_lat_total=int(tmp)
            tmp=wrlatl.split('wrlat:')[1]
            tmp=tmp.split('#')[0]
            wr_lat_total=int(tmp)
    
            memlatl=zsimout.readline()
            if 'atHist' in memlatl:
                memlathist_exist=True;
                for a in range(200):
                    latline=zsimout.readline()
                    tmp=latline.split(":")
                    assert(a==int(tmp[0]))
                    memlathist_DDR[a]+=int(tmp[1])
    
    
            
    
    
    
        if 'l3-' in line:
            num_llc_banks+=1
            while not 'hGETS' in line:
                line=zsimout.readline()
            tmp1=line.split(': ')[1]
            tmp2=int(tmp1.split(' #')[0])
            l3hits += tmp2
            line=zsimout.readline()
            if not 'hGETX' in line:
                print('expected hGETX but didnt find\n')
            tmp1=line.split(': ')[1]
            tmp2=int(tmp1.split(' #')[0])
            l3hits += tmp2
            line=zsimout.readline()
    
            while not 'mGETS' in line:
                line=zsimout.readline()
            if not 'mGETS' in line:
                print('expected mGETS but didnt find\n')
            tmp1=line.split(': ')[1]
            tmp2=int(tmp1.split(' #')[0])
            l3misses += tmp2
            line=zsimout.readline()
            if not 'mGETXIM' in line:
                print('expected mGEXIM but didnt find\n')
            tmp1=line.split(': ')[1]
            tmp2=int(tmp1.split(' #')[0])
            l3misses += tmp2
    
                
    
    
        line=zsimout.readline()
    
    zsimout.close()
    if(wr_count!=0):
        wr_lat_avg = wr_lat_total/wr_count
    else:
        print('no wr count logged')
        wr_lat_avg = 0
        
    if(rd_count!=0):
        rd_lat_avg = rd_lat_total/rd_count
    else:
        print('no rd count logged')
        rd_lat_avg = 0
    
    all_lat_avg=0
    if(rd_count+wr_count!=0):
        all_lat_avg = (rd_lat_total+wr_lat_total) / (rd_count+wr_count)
    
    DDR_amat=all_lat_avg/2 #divide by 2 to convert from cycle to ns
    DDR_amats.append(DDR_amat)
    
    mpki=0
    if(total_insts!=0):
        mpki= (l3misses*1000) / total_insts;
    
    ipc_all = 0
    if(total_cycles!=0):
        ipc_all=total_insts / total_cycles
    
    l3miss_rate = 0
    if((l3misses+l3hits)!=0):
        l3miss_rate=l3misses/ (l3misses+l3hits)
    
    #rdlat_avg=0
    #wrlat_avg=0
    #if(rd!=0):
    #    rdlat_avg = rdlat/rd;
    
    
    if(memlathist_exist):
        allacc = sum(memlathist_DDR)
        #mlat_pdf = memlathist / sum(memlathist)
        mlat_pdf_DDR = [x / allacc for x in memlathist_DDR]
        mlat_cdf_DDR = np.cumsum(mlat_pdf_DDR)
        cdf_DDRs.append(mlat_cdf_DDR)
        
        p99=0
        p95=0
        p90=0
        p80=0
        p70=0
        median=0
        
        for a in range(200):
            cd=mlat_cdf_DDR[a]
            if(cd>=0.99):
                if(p99==0):
                    p99=a*10;
            if(cd>=0.95):
                if(p95==0):
                    p95=a*10;
            if(cd>=0.90):
                if(p90==0):
                    p90=a*10;
            if(cd>=0.80):
                if(p80==0):
                    p80=a*10;
            if(cd>=0.70):
                if(p70==0):
                    p70=a*10;
            if(cd>=0.50):
                if(median==0):
                    median=a*10;
        
    
        m_sum=0
        for i in range(200):
            a=mlat_pdf_DDR[i]*(i*5)
            m_sum=m_sum+a
        print('DDR mean: '+str(m_sum))
    
        
        a_sum=0
        for i in range(200):
            #a=mlat_pdf_DDR[i]*(((i*5)-(all_lat_avg/2)) * ((i*5)-(all_lat_avg/2)) )
            a=mlat_pdf_DDR[i]*(((i*5)-m_sum) * ((i*5)-(m_sum)) )
            a_sum=a_sum+a
        stdev_DDR=math.sqrt(a_sum)
        print('DDR stdev: '+str(stdev_DDR)) 
    
    
    #### NOW repeat for CXL
    zsimout_CXL = 'zsim.out_CXL_'+app
    zsimout = open(zsimout_CXL)
    
    wr_lat_total=0
    rd_lat_total=0
    rd_count=0
    wr_count=0
    accesses=0
    l3misses=0;
    l3hits=0;
    total_insts=0
    total_cycles=0
    
    #sancheck counter
    num_mem_con=0
    num_llc_banks=0
    
    
    
    line = zsimout.readline()
    while line:
        if 'OCore1-' in line:
            line=zsimout.readline()
            if not ' cycles:' in line:
                print('expected cycles for core but didnt find\n')
            tmp1=line.split(': ')[1]
            tmp2=int(tmp1.split(' #')[0])
            total_cycles +=tmp2
            
            line=zsimout.readline()
            line=zsimout.readline()
            
            if not 'instrs:' in line:
                print('expected instrs for core but didnt find\n')
            tmp1=line.split(': ')[1]
            tmp2=int(tmp1.split(' #')[0])
            total_insts +=tmp2
    
        if 'mem-' in line:
            #rd=0;
            #wr=0;
            #rdlat=0;
            #wrlat=0;
    
            wr_lat_total=0
            rd_lat_total=0
            rd_count=0
            wr_count=0
    
    
            rdl=zsimout.readline()
            wrl=zsimout.readline()
            rdlatl=zsimout.readline()
            wrlatl=zsimout.readline()
            if not 'rd:' in rdl:
                print('expected rd: in mem but not found\n')
            if not 'wr:' in wrl:
                print('expected wr: in mem but not found\n')
            if not 'rdlat:' in rdlatl:
                print('expected rdlat: in mem but not found\n')
            if not 'wrlat:' in wrlatl:
                print('expected wrlat: in mem but not found\n')
            tmp=rdl.split('rd:')[1]
            tmp=tmp.split('#')[0]
            rd_count=int(tmp)
            tmp=wrl.split('wr:')[1]
            tmp=tmp.split('#')[0]
            wr_count=int(tmp)
            tmp=rdlatl.split('rdlat:')[1]
            tmp=tmp.split('#')[0]
            rd_lat_total=int(tmp)
            tmp=wrlatl.split('wrlat:')[1]
            tmp=tmp.split('#')[0]
            wr_lat_total=int(tmp)
    
            memlatl=zsimout.readline()
            if 'atHist' in memlatl:
                memlathist_exist=True;
                for a in range(200):
                    latline=zsimout.readline()
                    tmp=latline.split(":")
                    assert(a==int(tmp[0]))
                    cxl_offset = int(CXL_DELAY/10)
                    a_offset = a+cxl_offset
                    if(a_offset > 199):
                        a_offset = 199
                    memlathist_CXL[a_offset]+=int(tmp[1])
    
    
            
    
    
    
        if 'l3-' in line:
            num_llc_banks+=1
            while not 'hGETS' in line:
                line=zsimout.readline()
            tmp1=line.split(': ')[1]
            tmp2=int(tmp1.split(' #')[0])
            l3hits += tmp2
            line=zsimout.readline()
            if not 'hGETX' in line:
                print('expected hGETX but didnt find\n')
            tmp1=line.split(': ')[1]
            tmp2=int(tmp1.split(' #')[0])
            l3hits += tmp2
            line=zsimout.readline()
    
            while not 'mGETS' in line:
                line=zsimout.readline()
            if not 'mGETS' in line:
                print('expected mGETS but didnt find\n')
            tmp1=line.split(': ')[1]
            tmp2=int(tmp1.split(' #')[0])
            l3misses += tmp2
            line=zsimout.readline()
            if not 'mGETXIM' in line:
                print('expected mGEXIM but didnt find\n')
            tmp1=line.split(': ')[1]
            tmp2=int(tmp1.split(' #')[0])
            l3misses += tmp2
    
                
    
    
        line=zsimout.readline()
    
    zsimout.close()
    if(wr_count!=0):
        wr_lat_avg = wr_lat_total/wr_count
    else:
        print('no wr count logged')
        wr_lat_avg = 0
        
    if(rd_count!=0):
        rd_lat_avg = rd_lat_total/rd_count
    else:
        print('no rd count logged')
        rd_lat_avg = 0
    
    all_lat_avg=0
    if(rd_count+wr_count!=0):
        all_lat_avg = (rd_lat_total+wr_lat_total) / (rd_count+wr_count)
    
    CXL_amat=all_lat_avg /2 #divide by 2 to convert from cycle to ns
    CXL_amat = CXL_amat + (CXL_DELAY/2)
    CXL_amats.append(CXL_amat)
    
    mpki=0
    if(total_insts!=0):
        mpki= (l3misses*1000) / total_insts;
    
    ipc_all = 0
    if(total_cycles!=0):
        ipc_all=total_insts / total_cycles
    
    l3miss_rate = 0
    if((l3misses+l3hits)!=0):
        l3miss_rate=l3misses/ (l3misses+l3hits)
    
    #rdlat_avg=0
    #wrlat_avg=0
    #if(rd!=0):
    #    rdlat_avg = rdlat/rd;
    
    
    if(memlathist_exist):
        allacc = sum(memlathist_CXL)
        #mlat_pdf = memlathist / sum(memlathist)
        mlat_pdf_CXL = [x / allacc for x in memlathist_CXL]
        mlat_cdf_CXL = np.cumsum(mlat_pdf_CXL)
        cdf_CXLs.append(mlat_cdf_CXL)
        
        p99=0
        p95=0
        p90=0
        p80=0
        p70=0
        median=0
        
        for a in range(200):
            cd=mlat_cdf_CXL[a]
            if(cd>=0.99):
                if(p99==0):
                    p99=a*10;
            if(cd>=0.95):
                if(p95==0):
                    p95=a*10;
            if(cd>=0.90):
                if(p90==0):
                    p90=a*10;
            if(cd>=0.80):
                if(p80==0):
                    p80=a*10;
            if(cd>=0.70):
                if(p70==0):
                    p70=a*10;
            if(cd>=0.50):
                if(median==0):
                    median=a*10;
        
    


#print(mlat_pdf_DDR)
#print(mlat_pdf_CXL)
print("apps : "+str(apps))
print("DDR_amats: "+str(DDR_amats))
#print("DDR_cdfs: "+str(cdf_DDRs))

#########################################################################
########################START PLOTTING###################################
#########################################################################
color_list=[ '#ABBFB0', '#799A82', '#3D5A45','darkslategrey', '#A89AE4', '#7C67D6', 'darkslateblue','#42347E']
####### Plotting CDF
#cdf_x_axis=[10*x for x in range(100)]
matplotlib.rcParams.update({'font.size': 60})

cdf_x_axis=[5*x for x in range(200)] #10*x in cycles, but / 2 to convert ot NS
linewidth=12


ifig = plt.figure(figsize=(20, 4))
grid = plt.GridSpec(1, 5, wspace=1, hspace=0.1)


iax0=plt.subplot(grid[0, 0])
iax1=plt.subplot(grid[0, 1])
iax2=plt.subplot(grid[0, 2])
iax3=plt.subplot(grid[0, 3])
iax4=plt.subplot(grid[0, 4])

iaxs=[]
iaxs.append(iax0)
iaxs.append(iax1)
iaxs.append(iax2)
iaxs.append(iax3)
iaxs.append(iax4)

for i in range(len(apps)):
    
    appname=apps[i]

    ifig,iax=plt.subplots()
    plt.plot(cdf_x_axis,cdf_DDRs[i], label="Baseline", linewidth=linewidth, color=color_list[2], linestyle='--')
    plt.plot(cdf_x_axis,cdf_CXLs[i], label="CoaXiaL", linewidth=linewidth , color=color_list[5])
    
    plt.axvline(x = DDR_amats[i], color = color_list[2], linewidth=linewidth, linestyle='--')
    plt.axvline(x = CXL_amats[i], color = color_list[5], linewidth=linewidth)
    
    fs_legend=140
    fs1=150
    
    iax.set_xlim(xmin=0)
    iax.set_ylim(ymin=0)
    iax.set_xlim(xmax=600)
    iax.legend(ncol=1,fontsize=fs_legend)
    plt.ylabel('Cumulative Probability',fontsize=fs1, labelpad=45)
    plt.xlabel('Memory Access Latency (ns)',fontsize=fs1, labelpad=45)
    iax.yaxis.set_label_coords(-0.15, 0.65)
    iax.xaxis.set_label_coords(0.45, -0.1)
    plt.grid(color='gray', linestyle='--', linewidth=0.2, zorder=0)
    iax.tick_params(axis='both', which='major', labelsize=80)
    #props = dict(boxstyle='round', facecolor='white', alpha=0.7)
    #props = dict(boxstyle='square,pad=0.1',facecolor='white', alpha=0.7)
    props = dict(facecolor='white', alpha=0.8)
    #iax.text(-145,1.1,btext,zorder=5, fontsize=fs1, ha='left',bbox=props);
    iax.text(300,1.1,btexts[i],zorder=5, fontsize=fs1, ha='center',bbox=props);
    #%raw data: DDR avg, DDR stdev, CXL avg, CXL stdev
    #% perlbench: 55.4	49.9	81.7	46.9
    #% Moses: 262.5	222.0	124.0	99.9
    #plt.setp(iax.get_yticklabels()[0], visible=False)
    #plt.setp(iax.get_yticklabels()[-1], visible=True)
    labels = iax.yaxis.get_major_ticks()
    labels[0].set_visible(False)
    #labels[0]=lables[-1]=""
    #iax.set_yticklabels(labels)
    iax.tick_params(axis='both', which='major', labelsize=120)
    ifig.set_size_inches(33,23)
    #plt.subplots_adjust(top=1.1)
    ifig.savefig('mem_lat_cdf_cut600_'+appname+'.png', bbox_inches='tight')
    ifig.tight_layout(pad=0)


