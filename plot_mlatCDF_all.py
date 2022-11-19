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


f_mem_lat = open('mem_lats.csv','w')

memlathist_exist=False;

#memlathists=[]
mlat_pdfs=[]
mlat_cdfs=[]
#memlathist_DDR=[0]*200;
#memlathist_CXL=[0]*200;

DDR_amat=0;
CXL_amat=0;


CXL_DELAY = 60
#CXL_DELAY = 0


#### handle DDR

zsimouts=[]
setups=[]

for ff in os.listdir():
    if('zsim.out' in ff):
        zsimouts.append(ff)

for ff in zsimouts:
    memlathist=[0]*200;
    zsimout = open(ff)
    tmp=ff.split('.out_')[1]
    setups.append(tmp)

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
                    memlathist[a]+=int(tmp[1])
    
    
            
    
    
    
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
        allacc = sum(memlathist)
        #mlat_pdf = memlathist / sum(memlathist)
        mlat_pdf = [x / allacc for x in memlathist]
        mlat_cdf = np.cumsum(mlat_pdf)
        
        p99=0
        p95=0
        p90=0
        p80=0
        p70=0
        median=0
        
        for a in range(200):
            cd=mlat_cdf[a]
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
        
    
    
    
    
    #f_mem_lat.write('\n######### DDR #########\n')
    f_mem_lat.write(ff+'\n')
    f_mem_lat.write('\nMEM:\n')
    
    #f_mem_lat.write('\nwr_lat_avg, '+str(wr_lat_avg)+',\n')
    #f_mem_lat.write('rd_lat_avg, '+str(rd_lat_avg)+',\n')
    f_mem_lat.write('all_lat_avg, '+str(all_lat_avg)+' ('+str(int(all_lat_avg/2))+'ns) ,\n')
    if(memlathist_exist):
        f_mem_lat.write('median, '+str(median)+' ('+str(int((median)/2))+'ns) ,\n')
        f_mem_lat.write('p70, '+str(p70)+' ('+str(int(p70/2))+'ns),\n')
        f_mem_lat.write('p80, '+str(p80)+' ('+str(int(p80/2))+'ns),\n')
        f_mem_lat.write('p90, '+str(p90)+' ('+str(int(p90/2))+'ns),\n')
        f_mem_lat.write('p95, '+str(p95)+' ('+str(int(p95/2))+'ns),\n')
        f_mem_lat.write('p99, '+str(p99)+' ('+str(int(p99/2))+'ns),\n')
    
    
        #f_mem_lat.write('median, '+str(median)+',\n')
        #f_mem_lat.write('p99, '+str(p99)+',\n')
        #f_mem_lat.write('p95, '+str(p95)+',\n')
        #f_mem_lat.write('p90, '+str(p90)+',\n')
        #f_mem_lat.write('p80, '+str(p80)+',\n')
        #f_mem_lat.write('p70, '+str(p70)+',\n')
    
    f_mem_lat.write('\nL3:\n')
      
    
    f_mem_lat.write('l3_miss_rate , '+str(l3miss_rate)+',\n')
    f_mem_lat.write('l3misses ,    '+str(l3misses)+',\n')
    
    #f_mem_lat.write('\nmem accesses        ,'+str(accesses)+',\n')
    
    f_mem_lat.write('\nMPKI: '+str(mpki)+',\n')
    f_mem_lat.write('IPC_ALL: '+str(ipc_all)+',\n')

    mlat_pdfs.append(mlat_pdf)
    mlat_cdfs.append(mlat_cdf)

f_mem_lat.close()

#print(mlat_pdf_DDR)
#print(mlat_pdf_CXL)

## print cdf raw data into a file
#f_cdf_rawd = open('raw_cdf.csv','w')
#f_cdf_rawd.write('DDR,\n')
#for ii in range(int(len(mlat_cdf_DDR) / 2 )):
#    #f_cdf_rawd.write(str(ii)+','+str(mlat_cdf_DDR[ii*2])+',\n')
#    f_cdf_rawd.write(str(ii*10)+','+"{:.2f}".format(mlat_cdf_DDR[ii*2])+',\n')
#f_cdf_rawd.write('CXL,\n')
#for ii in range(int(len(mlat_cdf_CXL) / 2 )):
#    f_cdf_rawd.write(str(ii*10)+','+"{:.2f}".format(mlat_cdf_CXL[ii*2])+',\n')
#
#f_cdf_rawd.close()




os.system('cat mem_lats.csv')

color_list=[ '#ABBFB0', '#799A82', '#3D5A45','darkslategrey', '#A89AE4', '#7C67D6', 'darkslateblue','#42347E']
####### Plotting CDF
#cdf_x_axis=[10*x for x in range(100)]
matplotlib.rcParams.update({'font.size': 30})
cdf_x_axis=[5*x for x in range(200)] #10*x in cycles, but / 2 to convert ot NS
ifig,iax=plt.subplots()
linewidth=3
for jj in range(len(setups)):
    #plt.plot(cdf_x_axis,mlat_cdfs[jj], label=setups[jj], linewidth=linewidth, color=color_list[jj])
    plt.plot(cdf_x_axis,mlat_pdfs[jj], label=setups[jj], linewidth=linewidth)

#plt.axvline(x = DDR_amat, color = color_list[2], linewidth=linewidth)
#plt.axvline(x = CXL_amat, color = color_list[5], linewidth=linewidth)

iax.legend(ncol=1)
#plt.ylabel('Cumulative Probability \n')
plt.ylabel('Probability \n')
plt.xlabel('\nMemory Access Latency (ns)')
plt.grid(color='gray', linestyle='--', linewidth=0.2, zorder=0)


ifig.set_size_inches(20,12)

ifig.savefig('mem_lat_pdf.png', bbox_inches='tight')



ifig,iax=plt.subplots()
linewidth=3
for jj in range(len(setups)):
    #plt.plot(cdf_x_axis,mlat_cdfs[jj], label=setups[jj], linewidth=linewidth, color=color_list[jj])
    plt.plot(cdf_x_axis,mlat_cdfs[jj], label=setups[jj], linewidth=linewidth)

#plt.axvline(x = DDR_amat, color = color_list[2], linewidth=linewidth)
#plt.axvline(x = CXL_amat, color = color_list[5], linewidth=linewidth)

iax.legend(ncol=1)
#plt.ylabel('Cumulative Probability \n')
plt.ylabel('Probability \n')
plt.xlabel('\nMemory Access Latency (ns)')
plt.grid(color='gray', linestyle='--', linewidth=0.2, zorder=0)


ifig.set_size_inches(20,12)

ifig.savefig('mem_lat_cdf.png', bbox_inches='tight')


