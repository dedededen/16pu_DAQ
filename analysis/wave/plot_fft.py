
import numpy as np
import matplotlib.pyplot as plt
import os

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

