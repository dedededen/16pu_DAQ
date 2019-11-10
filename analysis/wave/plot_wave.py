

import numpy as np
import matplotlib.pyplot as plt
import os

from wave import decode_wave

def plot_wave(file_name):
    if 'address15' in file_name:
        teibai = 64
        mon = 0
    else : 
        teibai = 52
        mon = 1
    vol = decode_wave.read_wave_file(file_name)
    #offset,off2 = cal_offset(vol,teibai)
    num = len(vol[0])
    num_range = teibai * 9
    #x = range(num)
    x = range(num_range)        
    fig = plt.figure(figsize=(15,9))
    for ch in range(16):
        vol_max = np.max(vol[ch])
        vol_min = np.min(vol[ch])
        print('ch '+str(ch) +
              '\t Max '+str(vol_max) +
              '\t Min '+str(vol_min) +
              '\tp-p '+str(vol_max-vol_min))
        plt.subplot(4,4,ch+1)
        [ plt.plot(x,vol[ch][i*num_range:(i+1)*num_range],c='blue',linewidth=0.5)  for i in range(10)]
        [ plt.axvline(x=52*(i+1),color='black',alpha=0.5 )for i in range(9)]
    fig.suptitle(os.path.split(file_name)[1], fontsize=20)
    plt.ylabel('ADC count')
    plt.xlabel('sampling number per a turn')
    #plt.show()
    return vol,mon
