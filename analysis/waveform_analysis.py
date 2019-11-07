

import numpy as np
import matplotlib.pyplot as plt
import os
import decode_wave
import cal_mom

teibai  = 52

def cal_offset(vol,teibai=52): ## timing
    off = teibai*9*10
    aaa = []
    min_power = 1000
    for i in range(teibai*9):
        if np.sum(np.abs(vol[0][off+i-teibai+1:off+i]-np.mean(vol[0]))) < min_power:
            aaa.append(i)
    for i in aaa:
        if np.abs(vol[0][off+i] - vol[0][off+i+10]) > 50 :
            break
    for j in range(10):
        if np.sum(np.abs(vol[0][i+j*teibai*9:i+j*teibai*9+teibai]-np.mean(vol[0]))) > min_power*0.1:
            break
    print(i,j)
    return i-2,j    

def goertzel(x,k,x_1=0):

    num = len(x)
    omega = 2 * np.pi * k / num
    s = np.zeros(num)
    for i in range(num):
        if i ==0:
            s[0] = x[0] + 2 * np.cos(omega) * x_1
        elif i ==1:
            s[1] = x[1] +  2 * np.cos(omega) * s[0] - x_1
        else:
            s[i] = x[i] + 2 * np.cos(omega) * s[i-1] - s[i-2]
    re = s[num-1] - np.cos(omega) * s[num-2]
    im = np.sin(omega) * s[num-2]
    ans = np.sqrt(re**2 + im**2)/num*2

    return ans/num*2,np.arctan(im/re)

def plot_wave(file_name):
    if 'address15' in file_name:
        teibai = 64
        mon = 0
    else : 
        teibai = 52
        mon = 1
    vol = decode_wave.read_wave_file(file_name)
    offset,off2 = cal_offset(vol,teibai)
    num = len(vol[0])
    num_range = teibai*9
    #x = range(num)
    x = range(num_range)        
    fig = plt.figure(figsize=(15,9))
    for ch in range(16):
        vol_max = np.max(vol[ch])
        vol_min = np.min(vol[ch])
        print('ch '+str(ch)),
        print('Max '+str(vol_max)),
        print('Min '+str(vol_min)),
        print('p-p '+str(vol_max-vol_min))
        # plt.text(num_range*1.,2**13+2**14*ch,'ch '+str(ch))
        #plt.text(num_range*1.05,2**13+2**14*ch,'Max '+str(vol_max))
        #plt.text(num_range*1.05,2**12+2**14*ch,'Min '+str(vol_min))
        #plt.text(num_range*1.05,2**10+2**14*ch,'p-p '+str(vol_max-vol_min))
        plt.subplot(4,4,ch+1)
        [ plt.plot(x,vol[ch][offset+i*num_range:offset +(i+1)*num_range],c='blue',linewidth=0.5)  for i in range(off2,int(num/num_range-1 - off2))]
        [ plt.axvline(x=52*(i+1),color='black',alpha=0.5 )for i in range(9)]
    fig.suptitle(os.path.split(file_name)[1], fontsize=20)
    plt.ylabel('ADC count')
    plt.xlabel('sampling number % 1 turn')
    
    #plt.show()
    plot_bunch_moment(os.path.split(file_name)[1],vol,mon)
    return vol



def cal_bunch_moment(vol,teibai=52,mon=0):
    #vol = decode_wave.read_wave_file(file_name)
    bunch_of,off2 =cal_offset(vol)
    num = int((len(vol[0])-bunch_of)/teibai) - off2*9 - 1
    moment = []
    
    for i in range(num):
        hoge = off2*teibai*9 + bunch_of +teibai*i

        buf= [ goertzel(vol[ch][hoge:hoge+teibai],2)[0]
              for ch in range(16)]# 11/4[4,3,2,1,0,15,14,13,12,11,10,9,8,7,6,5]]
#range(16)]
        
        buf2 = cal_mom.cal_mom(buf,num_mon=mon)
        moment.append(buf2)
    return np.array(moment)

def cal_reflectance(vol,teibai=52,mon=0):
    #vol = decode_wave.read_wave_file(file_name)
    amplitude= []
    phase = []
    num = int((len(vol[0]))/teibai)
    for i in range(num):
        hoge = teibai*i
        ch = 14
        buf= goertzel(vol[ch][hoge:hoge+teibai],2)
        amplitude.append(buf[0])
        phase.append(buf[1])
    return np.array(amplitude),np.array(phase)

def plot_relation_reflectance(file_name):
    if 'address15' in file_name:
        teibai = 64
        mon = 0
    else : 
        teibai = 52
        mon = 1
    vol = decode_wave.read_wave_file(file_name)
    amp , pha = cal_reflectance(vol,52,mon)
    fig = plt.figure(figsize=(15,9))
    plt.scatter(amp[0:1000:9]/amp[2:1002:9],abs(pha[:1000:9]-amp[2:1002:9]))
    fig.suptitle(os.path.split(file_name)[1], fontsize=20)
    #plt.ylabel('ADC count')
    #plt.xlabel('sampling number % 1 turn')
    
    plt.show()

    #return vol

def plot_bunch_moment(file_name,vol,mon):#,file_name):
    moment = cal_bunch_moment(vol,mon=mon)#file_name)
    fig = plt.figure()#figsize=(15,9))
    fig.suptitle(os.path.split(file_name)[1], fontsize=20)
    plt.subplots_adjust(top=0.9)
    num_bun = 1
    ax1 = fig.add_subplot(2, 2, 1)
    for i in range(num_bun):
        x = range(len(moment[i:1000:9,1]))
        ax1.plot(x,moment[i:1000:9,1],label='bunch: '+str(i),marker='o')
    ax1.legend()
    ax1.set_ylabel('x[mm]')
    ax1.set_xlabel('turn')
    #ax1.get_xaxis().get_major_formatter().set_useOffset(False)
    #ax1.get_yaxis().get_major_formatter().set_useOffset(False)
    ax1.grid()
    
    ax1_1 = fig.add_subplot(2, 2, 2)
    for i in range(num_bun):    
        x = range(len(moment[i:1000:9,2]))
        ax1_1.plot(x,moment[i:1000:9,2],label='bunch: '+str(i)+' y',marker='o')
    ax1_1.legend()
    ax1_1.set_ylabel('y[mm]')
    ax1_1.set_xlabel('turn')
    #ax1.get_xaxis().get_major_formatter().set_useOffset(False)
    #ax1.get_yaxis().get_major_formatter().set_useOffset(False)
    ax1_1.grid()

    ax2 = fig.add_subplot(2, 2, 3)
    for i in range(num_bun):
        x = range(len(moment[i:1000:9,1]))
        ax2.plot(x,moment[i:1000:9,3],label='bunch: '+str(i)+' x',marker='o')
        
    ax2.legend()
    ax2.set_ylabel('sigma_x^2 - sigma_y^2[mm^2]')
    ax2.set_xlabel('turn')
    #ax1.get_xaxis().get_major_formatter().set_useOffset(False)
    #ax1.get_yaxis().get_major_formatter().set_useOffset(False)
    ax2.grid()

    ax3 = fig.add_subplot(2, 2, 4)
    for i in range(num_bun):
        x = range(len(moment[i:1000:9,4]))
        ax3.plot(x,moment[i:1000:9,4],label='bunch: '+str(i)+' x',marker='o')
        
    ax3.legend()
    ax3.set_ylabel('sigma_xy[mm^2]')
    ax3.set_xlabel('turn')
    #ax1.get_xaxis().get_major_formatter().set_useOffset(False)
    #ax1.get_yaxis().get_major_formatter().set_useOffset(False)
    ax2.grid()

    #plt.show()
    return


def extract_peak(vol_ft,rf_harmonic=2):
    sampling_freq = 52 * 1.7e6
    sample = len(vol_ft)
    interval_freq = sampling_freq /sample
    eye_star_index = int(1.7e6 * rf_harmonic / interval_freq)
    peak_index = eye_star_index - 100 + np.argmax(vol_ft[eye_star_index - 100 : eye_star_index + 100])
    return peak_index , vol_ft[peak_index]

def all_moment(file_name):
    num_list = len(file_name)
    result = []
    if "address13" in file_name[0]:
        mon = 1
    else:
        mon = 0
        
    for ifile in range(num_list):
        vol = decode_wave.read_wave_file(file_name[ifile])
        num = len(vol[0])
        vol_peak = np.ones(16)
        for ch in [8,9,10,11,12,13,14,15,0,1,2,3,4,5,6,7]:#range(16)]range(16):
            vol_ft = np.abs(np.fft.fft(vol[ch]))/num*2
            index,vol_peak[ch] = extract_peak(vol_ft,rf_harmonic=2)
            print('peak index number : '+str(index))
        mom = cal_mom.cal_mom(vol_peak,num_mon=mon)

        result.append(mom)
    return np.array(result)

def plot_mom(file_name):
    num_list = len(file_name)
    all_mom = all_moment(file_name)
    fig = plt.figure()#figsize=(15,9))
    #plt.title()
    ax1 = fig.add_subplot(1, 2, 1)
    for i in range(num_list):
        ax1.plot(all_mom[i][1],all_mom[i][2],label=os.path.split(file_name[i])[1],marker='o')
    ax1.legend()
    ax1.set_ylabel('y[mm]')
    ax1.set_xlabel('x[mm]')
    #ax1.get_xaxis().get_major_formatter().set_useOffset(False)
    #ax1.get_yaxis().get_major_formatter().set_useOffset(False)
    ax1.grid()

    ax2 = fig.add_subplot(1, 2, 2)
    for i in range(num_list):
        ax2.plot(all_mom[i][3],all_mom[i][4],label=os.path.split(file_name[i])[1],marker='o')
    #ax2.legend()
    ax2.set_xlabel('sigma_x^2 - sigma_y^2[mm^2]')
    ax2.set_ylabel('sigma_xy[mm^2]')
    #ax2.get_xaxis().get_major_formatter().set_useOffset(False)
    #ax2.get_yaxis().get_major_formatter().set_useOffset(False)
    ax2.grid()

    plt.show()
    
    
def plot_fft(file_name,vol):
    num = len(vol[0])
    plt.figure(figsize=(15,9))
    x = np.linspace(0, 1.7*52, num)
    for ch in range(16):
        vol_ft = np.abs(np.fft.fft(vol[ch]))/num*2
        #A = extract_peak(vol_ft)
        #print(A)
        plt.plot(x,vol_ft,linewidth=0.5,label=str(ch))
    plt.legend()
    plt.yscale('log')
    plt.ylim(1e-4,2**14)
    plt.xlim(0,x[-1]/2)
    plt.title(os.path.split(file_name)[1])
    plt.ylabel('ADC count')
    plt.xlabel('Frequecy[MHz]')
    plt.grid()
    plt.show()

