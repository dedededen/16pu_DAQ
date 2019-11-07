

import numpy as np
import matplotlib.pyplot as plt
import os
import decode_process
import cal_mom

constant = 1/64e6
#constant = 1/2e6
def remove(vol_goe):
    result = np.copy(vol_goe)
    num = 10
    try_num = int(len(vol_goe[:,0])/num)
    for i in range(try_num):
        for ch in range(16):
            me = np.mean(vol_goe[num*i:num*(i+1),ch])
            std = np.std(vol_goe[num*i:num*(i+1),ch])
            for j in range(num):
                if vol_goe[num*i+j,ch] < (me -5* std) or vol_goe[num*i+j,ch] > (me + 5*std):
                    print(ch,num*i+j)
                    result[num*i+j,ch] = None#1/constant
    return result

def process_mom(file_name):
    vol = decode_process.read_process_file(file_name)
    num = vol.shape[0] -1
    moment = [ [] for i in range(9)]
    if "address13" in file_name[0]:
        mon = 1
    else:
        mon = 0
    for i in range(num):
        mom = cal_mom.cal_mom(vol[i+1],num_mon=mon)
        moment[i%9].append(mom)
    moment = [ np.array(moment[i]) for i in range(9)]
    return moment

def plot_process_mom(file_name):
    moment = process_mom(file_name)
    fig = plt.figure()#figsize=(15,9))
    fig.suptitle(os.path.split(file_name)[1], fontsize=20)
    plt.subplots_adjust(top=0.9)

    ax1 = fig.add_subplot(1, 2, 1)
    for i in range(9):
        #print(moment.shape)
        ax1.plot(moment[i][:,1],moment[i][:,2],label=str(i),marker='o')
    ax1.legend()
    ax1.set_ylabel('y[mm]')
    ax1.set_xlabel('x[mm]')
    #ax1.get_xaxis().get_major_formatter().set_useOffset(False)
    #ax1.get_yaxis().get_major_formatter().set_useOffset(False)
    ax1.grid()

    ax2 = fig.add_subplot(1, 2, 2)
    for i in range(9):
        ax2.plot(moment[i][:,3],moment[i][:,4],label=str(i),marker='o')
    #ax2.legend()
    ax2.set_ylabel('sigma_x^2 - sigma_y^2[mm^2]')
    ax2.set_xlabel('sigma_xy[mm^2]')
    #ax2.get_xaxis().get_major_formatter().set_useOffset(False)
    #ax2.get_yaxis().get_major_formatter().set_useOffset(False)
    ax2.grid()

    #plt.show()

    
def plot_process(file_name):
    mom = decode_process.read_process_file(file_name)
    #mom = remove(mom)
    #num = len(mom[:,0])
    
    for j in range(16):
        for k in range(9):
            plt.subplot(3,3,k+1)
            plt.plot(range(len(mom[k+1::9,j])),mom[k+1::9,j]*constant,linewidth=0.5,marker='v',markersize=1,label=str(j))
        print('ch: ' + str(j) +'\tmean: ' + str(constant*np.mean(mom[0:,j])) + '\tstd: ' + str(constant*np.std(mom[0:,j])))
    #print(constant*mom[:,4])
    #plt.ylim(0,16*2**14)
    #plt.yscale('log')
    #plt.legend()
    plt.ylabel('ADC count')
    plt.xlabel('turn number')
    #plt.title(os.path.split(file_name)[1])
    #plt.legend(loc="upper center", ncol=4)
    plt.show()

def plot_process_ref(file_name):
    mom = decode_process.read_process_file(file_name)
    #mom = remove(mom)
    num = int(len(mom[:,0]) * 0.9)
    
    for j in range(16):
        plt.subplot(4,4,j+1)
        plt.scatter(mom[:num:9,j]*constant,mom[2:num+2:9,j]*constant,label=str(j))
        
    plt.ylabel('bunch2')
    plt.xlabel('bunch0')
    plt.title(os.path.split(file_name)[1])
    #plt.legend(loc="upper center", ncol=4)
    plt.show()

def plot_process_before(file_name):
    mom = decode_process.read_process_file(file_name)
    mom = remove(mom)
    num = len(mom[:,0])
    
    x = range(num)

    for j in range(16):
        plt.plot(x,mom[:,j]*constant,linewidth=0.5,marker='v',markersize=1,label=str(j))
        print('ch: ' + str(j) +'\tmean: ' + str(constant*np.mean(mom[1:,j])) + '\tstd: ' + str(constant*np.std(mom[1:,j])))
        print('ch: ' + str(j) +'\tmean: ' + str(constant*np.mean(mom[0:,j])) + '\tstd: ' + str(constant*np.std(mom[0:,j])))
        #plt.ylim(0,16*2**14)

    plt.yscale('log')
    plt.legend()
    
    plt.ylabel('ADC count')
    plt.xlabel('bunch number')
    plt.title(os.path.split(file_name)[1])
    #plt.legend(loc="upper center", ncol=4)

    plt.show()
