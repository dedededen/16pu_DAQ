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

def process_noise(file_name,saveon=0):
    vol = decode_process.read_process_file(file_name)
    fig = plt.figure()#figsize=(15,9))
    plt.title(os.path.split(file_name)[1], fontsize=20)
    plt.subplots_adjust(top=0.9)
    noise = np.zeros(16)
    for i in range(16):
        plt.hist(vol[:,i],label=str(i),histtype='step',bins=100)
        noise[i] = np.mean(vol[0:,i])
        print('ch: ' + str(i) +'\tmean: ' + str(noise[i]) + '\tstd: ' + str(np.std(vol[0:,i])))
    plt.legend()
    plt.xscale('log')
    if saveon ==1:
        if 'address13' in file_name:
            ofile = '/jkdata/jkpublic/accbmon/mrbmon/16pu_data/16pu_DAQ/analysis/noise/par/noise_address13'
        else:
            ofile = '/jkdata/jkpublic/accbmon/mrbmon/16pu_data/16pu_DAQ/analysis/noise/par/noise_address15'
        plt.savefig(ofile+'.png')
        np.savetxt(ofile+'.txt',noise)
        plt.show()
        return
    plot_process(vol,file_name,saveon)

def plot_process(mom,file_name,saveon):
    num = len(mom[:,0])
    
    x = range(num)
    fig = plt.figure()#figsize=(15,9))

    for j in range(16):
        plt.plot(x,mom[:,j],linewidth=0.5,marker='v',markersize=1,label=str(j))
        #plt.ylim(0,16*2**14)

    plt.yscale('log')
    #plt.legend()
    
    plt.ylabel('ADC count')
    plt.xlabel('bunch number')
    plt.title(os.path.split(file_name)[1])
    #plt.legend(loc="upper center", ncol=4)

    plt.show()

if __name__=='__main__':
    import sys
    args = sys.argv
    process_noise(args[1])
