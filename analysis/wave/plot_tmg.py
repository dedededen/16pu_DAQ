
import os
import numpy as np
import matplotlib.pyplot as plt

from wave import  cal_timing_ofset 
from wave import decode_wave

def plot_timing(file_name):
    vol = decode_wave.read_wave_file(file_name)
    a = cal_timing_ofset.cal_offset(vol)
    print('clk delay  :' +str(a[0]+a[1]*52*9))
    num_range = 52 * 9
    x = range(num_range)
    ch  = 0
    plt.figure(figsize=(15,9))
    [ plt.plot(x,vol[ch][num_range*i:num_range*(i+1) ],linewidth=0.5,marker='v',markersize=1,c='blue',label=str(ch)) for i in range(120)]
    ch  = 12
    [ plt.plot(x,vol[ch][num_range*i:num_range*(i+1) ],linewidth=0.5,marker='v',markersize=1,c='red',label=str(ch)) for i in range(120)]
    [ plt.axvline(x=52*(i+1),color='black',alpha=0.5 )for i in range(9)]
    plt.title(os.path.split(file_name)[1])
    plt.ylabel('ADC count')
    plt.xlabel('sampling num')
    plt.show()
