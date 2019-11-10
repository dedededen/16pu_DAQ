
from wave import goertzel
from wave import decode_wave

import numpy as np
import matplotlib.pyplot as plt
import os


def cal_reflectance(vol,teibai=52,mon=0):
    #vol = decode_wave.read_wave_file(file_name)
    amplitude= []
    phase = []
    num = int((len(vol[0]))/teibai-2)
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
