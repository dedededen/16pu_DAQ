import numpy as np
import matplotlib.pyplot as plt
import os
from wave import decode_wave
from process import decode_process


def wave_noise(file_name):
    vol = decode_wave.read_wave_file(file_name)
    for ch in range(16):
        vol_max = np.max(vol[ch])
        vol_min = np.min(vol[ch])
        print('ch '+str(ch) + '\t Max '+str(vol_max) + '\t Min '+str(vol_min) +'\t p-p '+str(vol_max-vol_min))
    num = len(vol[0])
    plt.figure(figsize=(15,9))
    x = np.linspace(0, 1.7*52, num)
    for ch in range(16):
        vol_ft = np.abs(np.fft.fft(vol[ch]))/num*2
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

def process_noise(file_name):
    vol = decode_process.read_process_file(file_name)
    fig = plt.figure()#figsize=(15,9))
    plt.title(os.path.split(file_name)[1], fontsize=20)
    plt.subplots_adjust(top=0.9)

    for i in range(16):
        plt.hist(vol[:,i],label=str(i),histtype='step')
    plt.legend()
    plt.xscale('log')
    plot_process(vol,file_name)

def plot_process(mom,file_name):
    num = len(mom[:,0])
    
    x = range(num)
    fig = plt.figure()#figsize=(15,9))

    for j in range(16):
        plt.plot(x,mom[:,j],linewidth=0.5,marker='v',markersize=1,label=str(j))
        print('ch: ' + str(j) +'\tmean: ' + str(np.mean(mom[0:,j])) + '\tstd: ' + str(np.std(mom[0:,j])))
        #plt.ylim(0,16*2**14)

    plt.yscale('log')
    #plt.legend()
    
    plt.ylabel('ADC count')
    plt.xlabel('bunch number')
    plt.title(os.path.split(file_name)[1])
    #plt.legend(loc="upper center", ncol=4)

    plt.show()
