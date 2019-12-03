
import numpy as np
import os
from process import decode_process
import datetime
from cal_mom import cal_mom
import matplotlib.pyplot as plt
from myROOT import fit_po1

# extract setting
import time
def extract_cal_vol():
    datapath = '/jkdata/jkpublic/accbmon/mrbmon/16pu_data/20191128/BBA_data/process_2019_11_28_'
    datamid =[# data pos I[A]
        ### pos 0  (0,0)
        ['04_33_56',5],
        ['04_35_21',2.5],
        ['04_29_24',0], 
        ['04_36_28',-2.5],
        ['04_37_47',-5],

        ### pos 1  (0,4)
        ['04_43_27',5], 
        ['04_42_05',2.5],
        ['04_41_08',0],
        ['04_40_38',-2.5],
        ['04_40_06',-5],

        ### pos 2 (-4,0) 
        ['04_58_39',5], 
        ['04_59_46',2.5],
        ['05_00_48',0],
        ['05_01_21',-2.5],
        ['05_02_10',-5],

        ### pos 3  (4,0)
        ['05_06_50',5], 
        ['05_07_30',2.5],
        ['05_04_27',0],
        ['05_03_59',-2.5],
        ['05_03_27',-5],

        ### pos 4  (0,4)
        ['05_08_37',5], 
        ['05_09_09',2.5],
        ['05_10_06',0],
        ['05_10_56',-2.5],
        ['05_11_38',-5]
    ]
    dataend = ['_address13.dat','_address15.dat']
    
    resx  = []
    resy  = []
    shot_num = 25
    for i in range(shot_num):
        file13  = datapath + datamid[i][0] + dataend[0]
        file15  = datapath + datamid[i][0] + dataend[1]
        print(file13,file15)
        vol13 = decode_process.read_process_file(file13)
        vol15 = decode_process.read_process_file(file15)
        
        
        turn_start = 1
        turn_end   = 501
        nbunch     = 1
        x = [[],[]]#13,15
        y = [[],[]]#13,15
        for j in range(turn_start,turn_end):
            mom13 = cal_mom.moment(vol13[j*9+nbunch-1],num_mon=1)
            mom15 = cal_mom.moment(vol15[j*9+nbunch-1],num_mon=0)
            
            x[0].append(mom13[1])
            x[1].append(mom15[1])
            y[0].append(mom13[2])
            y[1].append(mom15[2])
            
        resx.append(x)
        resy.append(y)
    ### shot 1315bunch turn
    resx = np.array(resx)
    resy = np.array(resy)
    
    I = np.array([ 5 -2.5*i for i  in range(5)])
    xK13 = np.zeros([2,3])
    yK13 = np.zeros([2,3])
    xK15 = np.zeros([2,3])
    yK15 = np.zeros([2,3])
    

    ## pos 0
    x13 = [ np.mean(resx[i][0]) for i in range(5)]
    x15 = [ np.mean(resx[i][1]) for i in range(5)]
    y13 = [ np.mean(resy[i][0]) for i in range(5)]
    y15 = [ np.mean(resy[i][1]) for i in range(5)]
    ex13 = [ np.std(resx[i][0]) for i in range(5)]
    ex15 = [ np.std(resx[i][1]) for i in range(5)]
    ey13 = [ np.std(resy[i][0]) for i in range(5)]
    ey15 = [ np.std(resy[i][1]) for i in range(5)]
    plt.figure()

    plt.subplot(2,2,1)
    plt.errorbar(I,x13,yerr=ex13,fmt='v')
    xK13[1][0], b = np.polyfit(I, x13, 1)
    plt.plot(I,I*xK13[1][0]+b)
    xK13[0][0] = x13[2]
    plt.xlabel('I[A]')
    plt.ylabel('x[mm]')

    plt.subplot(2,2,2)
    plt.errorbar(I,x15,yerr=ex15,fmt='v')
    xK15[1][0], b = np.polyfit(I, x15, 1)
    plt.plot(I,I*xK15[1][0]+b)
    xK15[0][0] = x15[2]
    plt.xlabel('I[A]')
    plt.ylabel('x[mm]')

    plt.subplot(2,2,3)
    plt.errorbar(I,y13,yerr=ey13,fmt='v')
    yK13[1][0], b = np.polyfit(I, y13, 1)
    plt.plot(I,I*yK13[1][0]+b)
    yK13[0][0] = y13[2]
    plt.xlabel('I[A]')
    plt.ylabel('y[mm]')

    plt.subplot(2,2,4)
    plt.errorbar(I,y15,yerr=ey15,fmt='v')
    yK15[1][0], b = np.polyfit(I, y15, 1)
    plt.plot(I,I*xK15[1][0]+b)
    yK15[0][0] = y15[2]
    plt.xlabel('I[A]')
    plt.ylabel('y[mm]')

    
    # ## pos2,3
    x13 = [ np.mean(resx[10+i][0]) for i in range(5)]
    x15 = [ np.mean(resx[10+i][1]) for i in range(5)]
    y13 = [ np.mean(resx[15+i][0]) for i in range(5)]
    y15 = [ np.mean(resx[15+i][1]) for i in range(5)]
    ex13 = [ np.std(resx[10+i][0]) for i in range(5)]
    ex15 = [ np.std(resx[10+i][1]) for i in range(5)]
    ey13 = [ np.std(resy[15+i][0]) for i in range(5)]
    ey15 = [ np.std(resy[15+i][1]) for i in range(5)]
    plt.figure()
    plt.subplot(2,2,1)
    plt.errorbar(I,x13,yerr=ex13,fmt='v')
    xK13[1][1], b = np.polyfit(I, x13, 1)
    plt.plot(I,I*xK13[1][1]+b)
    xK13[0][1] = x13[2]
    plt.xlabel('I[A]')
    plt.ylabel('x[mm]')

    plt.subplot(2,2,2)
    plt.errorbar(I,x15,yerr=ex15,fmt='v')
    xK15[1][1], b = np.polyfit(I, x15, 1)
    plt.plot(I,I*xK15[1][1]+b)
    xK15[0][1] = x15[2]
    plt.xlabel('I[A]')
    plt.ylabel('x[mm]')

    plt.subplot(2,2,3)
    plt.errorbar(I,y13,yerr=ey13,fmt='v')
    xK13[1][2], b = np.polyfit(I, y13, 1)
    plt.plot(I,I*xK13[1][2]+b)
    xK13[0][2] = y13[2]
    plt.xlabel('I[A]')
    plt.ylabel('x[mm]')

    plt.subplot(2,2,4)
    plt.errorbar(I,y15,yerr=ey15,fmt='v')
    xK15[1][2], b = np.polyfit(I, y15, 1)
    plt.plot(I,I*xK15[1][2]+b)
    xK15[0][2] = y13[2]
    plt.xlabel('I[A]')
    plt.ylabel('x[mm]')

    # ## pos1,4
    x13 = [ np.mean(resy[5+i][0]) for i in range(5)]
    x15 = [ np.mean(resy[5+i][1]) for i in range(5)]
    y13 = [ np.mean(resy[20+i][0]) for i in range(5)]
    y15 = [ np.mean(resy[20+i][1]) for i in range(5)]
    ex13 = [ np.std(resx[5+i][0]) for i in range(5)]
    ex15 = [ np.std(resx[5+i][1]) for i in range(5)]
    ey13 = [ np.std(resy[20+i][0]) for i in range(5)]
    ey15 = [ np.std(resy[20+i][1]) for i in range(5)]
    fig = plt.figure()

    plt.subplot(2,2,1)
    plt.errorbar(I,x13,yerr=ex13,fmt='v')
    yK13[1][1], b = np.polyfit(I, x13, 1)
    plt.plot(I,I*yK13[1][1]+b)
    yK13[0][1] = x13[2]
    plt.xlabel('I[A]')
    plt.ylabel('y[mm]')

    plt.subplot(2,2,2)
    plt.errorbar(I,x15,yerr=ex15,fmt='v')
    yK15[1][1], b = np.polyfit(I, x15, 1)
    plt.plot(I,I*yK15[1][1]+b)
    yK15[0][1] = x15[2]
    plt.xlabel('I[A]')
    plt.ylabel('y[mm]')

    plt.subplot(2,2,3)
    plt.errorbar(I,y13,yerr=ey13,fmt='v')
    yK13[1][2], b = np.polyfit(I, y13, 1)
    plt.plot(I,I*yK13[1][2]+b)
    yK13[0][2] = y13[2]
    plt.xlabel('I[A]')
    plt.ylabel('y[mm]')

    plt.subplot(2,2,4)
    plt.errorbar(I,y15,yerr=ey15,fmt='v')
    yK15[1][2], b = np.polyfit(I, y15, 1)
    plt.plot(I,I*yK15[1][2]+b)
    yK15[0][2] = y15[2]
    plt.xlabel('I[A]')
    plt.ylabel('y[mm]')

    ##res
    plt.figure()
    plt.subplot(2,2,1)
    #plt.errorbar(I,x13,yerr=ex13,fmt='v')
    plt.scatter(xK13[0],xK13[1])
    a, b = fit_po1.po1(xK13[0],xK13[1])
    print(-1 *a[1]/a[0])
    a, b = np.polyfit(xK13[0],xK13[1], 1)
    print(-1 *b/a)
    plt.xlabel('x[mm]')
    #plt.ylabel('y[mm]')

    plt.subplot(2,2,2)
    #plt.errorbar(I,x13,yerr=ex13,fmt='v')
    plt.scatter(xK15[0],xK15[1])
    plt.xlabel('x[mm]')
    #plt.ylabel('y[mm]')

    plt.subplot(2,2,3)
    #plt.errorbar(I,x13,yerr=ex13,fmt='v')
    plt.scatter(yK13[0],yK13[1])
    plt.xlabel('y[mm]')
    #plt.ylabel('y[mm]')

    plt.subplot(2,2,4)
    #plt.errorbar(I,x13,yerr=ex13,fmt='v')
    plt.scatter(yK15[0],yK15[1])
    plt.xlabel('y[mm]')
    #plt.ylabel('y[mm]')
    
    plt.show()
    return 

