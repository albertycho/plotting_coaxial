import os
import sys 
import csv 
import math
import statistics
import numpy as np
from os.path import exists
import matplotlib
import matplotlib.pyplot as plt 

#curdir = 
os.system('mkdir allcdfs')
dir_list=os.listdir('.')
print (dir_list)
for dd in dir_list:
    print(dd)
    if (os.path.isdir(dd)):
        #os.system('cd '+dd)
        os.chdir(dd)
        os.system('rm mem_lat* stat_summary.txt')
        os.system('~/CXL_WD/plot_mlatCDF_CMP.py')
        os.system('cp mem_lat_cdf_cut600.png ../allcdfs/mem_lat_cdf_cut600_'+dd+'.png')
        os.system('cd ..')
        os.chdir('..')
