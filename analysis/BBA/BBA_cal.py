

import numpy as np
import os
import datetime
import matplotlib.pyplot as plt
from myROOT import fit_po1

# extract setting
from BBA import extract_BBA
import time

def plot_hist(res,bunch=1,horv=0):
    ans = np.ones((15,2,2))
    if horv==0:
        index = [15,16,17,18,19,0,1,2,3,4,10,11,12,13,14]
        label = ['x[mm]','dx/dI[mm/A]','  horizontal','_h']
        turnend = 286
    elif horv==1:
        index = [5,6,7,8,9,0,1,2,3,4,20,21,22,23,24]
        label = ['y[mm]','dy/dI[mm/A]','  vertical','_v']
        turnend = 465

    for j in range(15):
        for mon in range(2):
            min = np.min(res[index[j]][mon]) - 0.05
            max = np.max(res[index[j]][mon]) + 0.05
            fig = plt.figure(figsize=[20,10])
            fig.suptitle('Mon.:  '+str(mon)+', shot: '+str(index[j])+label[2])
            for i in range(bunch):
                plt.subplot(bunch,2,1+2*i)
                turn = range(len(res[index[j]][mon][i::bunch]))
                plt.plot(turn,res[index[j]][mon][i::bunch])
                plt.axhline(np.mean(res[index[j]][mon][i:turnend:bunch]), ls = "--", color = "navy")
                plt.xlabel('turn')
                plt.ylabel(label[0])
                plt.ylim(min,max)

                if i == 0:
                    ans[j][mon][0] = np.mean(res[index[j]][mon][i:turnend:bunch])
                    ans[j][mon][1] = np.std(res[index[j]][mon][i:turnend:bunch])/np.sqrt(turnend)
                text = str(round(np.mean(res[index[j]][mon][i:turnend:bunch]),3)) +'+/-' + str(round(np.std(res[index[j]][mon][i:turnend:bunch]),3)) + '[mm]'
                # print(text)
                # text = str(round(np.mean(res[index[j]][mon][i::bunch]),3)) +'+/-' + str(round(np.std(res[index[j]][mon][i::bunch]),3)) + '[mm]'
                # print(text)
                plt.text(300,min+0.05,text)
        
                plt.subplot(bunch,2,2+2*i)            
                numbin = int((max-min)/0.01) + 1
                plt.hist(res[index[j]][mon][i:turnend:bunch],histtype="step", orientation="horizontal",
                    range = [min,max],bins=numbin)
                plt.axhline(np.mean(res[index[j]][mon][i:turnend:bunch]), ls = "--", color = "navy")

            plt.savefig('/jkdata/jkpublic/accbmon/mrbmon/16pu_data/16pu_DAQ/analysis/BBA/pic/MON'+str(mon)+'_shot'+str(index[j])+label[3]+'.png')
            plt.close()
    return ans
def plot(res, mon=13,horv=0):
    I = np.array([ 5 -2.5*i for i  in range(5)])
    
    if mon == 13:
        num_mon = 0
    elif mon == 15:
        num_mon = 1

    if horv==0:
        index = [15,16,17,18,19,0,1,2,3,4,10,11,12,13,14]
        label = ['x[mm]','dx/dI[mm/A]','  horizontal  :',
                 '/jkdata/jkpublic/accbmon/mrbmon/16pu_data/16pu_DAQ/analysis/BBA/x0_'+str(mon)+'.txt',
                 'blue'
                 ]
    elif horv==1:
        index = [5,6,7,8,9,0,1,2,3,4,20,21,22,23,24]
        label = ['y[mm]','dy/dI[mm/A]','  vertical  :',
                 '/jkdata/jkpublic/accbmon/mrbmon/16pu_data/16pu_DAQ/analysis/BBA/y0_'+str(mon)+'.txt',
                 'red'
                 ]


    dxdi = [np.zeros(3) for i in range(2)]
    x0 = [np.zeros(3) for i in range(2)]
    fig = plt.figure(figsize=(20,6))
    plt.rcParams["font.size"] = 16    
    #plt.suptitle('#'+str(mon) +label[2])
    for i in range(3):
        y = [res[5*i+j][num_mon][0] for j in range(5)]
        ey = [res[5*i+j][num_mon][1] for j in range(5)]

        plt.subplot(1,3,1+i)
        plt.errorbar(I,y,yerr=ey,fmt='v',capsize=5, fmt='.', markersize=1, ecolor=label[4], markeredgecolor = label[4], ,label=label[2])
        plt.grid()
        a, b = fit_po1.po1(I,y,ey=ey)
        dxdi[0][i] = a[0]
        dxdi[1][i] = b[0]
        x0[0][i] = np.mean(y)
        x0[1][i] = ey[2]
        plt.plot(I,I*dxdi[0][i]+a[1])
        plt.xlabel('I[A]')
        if i ==0: plt.ylabel(label[0])
        
    fig = plt.figure(figsize=(20,6))
    plt.rcParams["font.size"] = 16    

    plt.errorbar(x0[0],dxdi[0][::],xerr=x0[1],yerr=dxdi[1][::],fmt='v')
    #a, b = fit_po1.po1(x0[0],dxdi[0],ex=x0[1],ey=dxdi[1])
    a, b = fit_po1.po1([x0[0][0],x0[0][2]],[dxdi[0][0],dxdi[0][2]],ex=[x0[1][0],x0[1][2]],ey=[dxdi[1][0],dxdi[1][2]])
    plt.plot(x0[0],a[0]*x0[0]+a[1])
    ans = [-1 *a[1]/a[0], np.abs(a[1]/a[0]) * np.sqrt(b[0]**2/a[0]**2 +b[1]**2/a[1]**2 ) ]
    text = '#'+str(mon) +label[2]+'\n'+str(round(ans[0],3)) +'  +/-  ' + str(round(ans[1],3)) 
    print('#'+str(mon) +label[2]+ str(ans[0]) +'  +/-  ' + str(ans[1]) )
    plt.text(0,0,text)
    plt.xlabel(label[0])
    plt.ylabel(label[1])
    np.savetxt(label[3],x0)
    return ans,x0,dxdi
    
def extract_cal_vol():
    num = 550
    resx ,resy = extract_BBA.extract_data(turn=[1,1+num],bunch=[[1,2,3,4],[1,2,3,4]])
    resx = plot_hist(resx,bunch=4,horv=0)
    resy = plot_hist(resy,bunch=4,horv=1)
    res13h = plot(resx,mon=13,horv=0)
    res15h = plot(resx,mon=15,horv=0)
    res13v = plot(resy,mon=13,horv=1)
    res15v = plot(resy,mon=15,horv=1)
    ans = np.array([[res13h[0][0],res13v[0][0],res13h[0][1],res13v[0][1]]
          ,[res15h[0][0],res15v[0][0],res15h[0][1],res15v[0][1]]])
    np.savetxt('/jkdata/jkpublic/accbmon/mrbmon/16pu_data/16pu_DAQ/analysis/cal_mom/alighment.txt',ans)
    plt.show()

    return 

