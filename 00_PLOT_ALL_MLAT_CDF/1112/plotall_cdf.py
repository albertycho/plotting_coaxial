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
dir_list=os.listdir('.')
print (dir_list)
for dd in dir_list:
    if (os.path.isdir(dd)):
        #os.system('cd '+dd)
        os.chdir(dd)
        os.system('rm mem_lat* stat_summary.txt')
        os.system('~/CXL_WD/plot_mlatCDF_CMP.py')
        os.system('cd ..')
        os.chdir('..')
