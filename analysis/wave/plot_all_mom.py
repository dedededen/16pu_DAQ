
import numpy as np
import matplotlib.pyplot as plt
import os

from cal_mom import cal_mom
from wave import decode_wave

teibai  = 52


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
        for ch in range(16):
            vol_ft = np.abs(np.fft.fft(vol[ch]))/num*2
            index,vol_peak[ch] = extract_peak(vol_ft,rf_harmonic=2)
            print('peak index number : '+str(index))
        mom = cal_mom.moment(vol_peak,num_mon=mon)
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
    ax1.grid()

    ax2 = fig.add_subplot(1, 2, 2)
    for i in range(num_list):
        ax2.plot(all_mom[i][3],all_mom[i][4],label=os.path.split(file_name[i])[1],marker='o')
    #ax2.legend()
    ax2.set_xlabel('sigma_x^2 - sigma_y^2[mm^2]')
    ax2.set_ylabel('sigma_xy[mm^2]')
    ax2.grid()

    plt.show()
    
    
