
import numpy as np
import matplotib.pyplot as plt

from wave import decode_wave
from wave import goertzel
from process import decode_process

def plot_delay(self,file_name):
    vol = decode_wave.read_wave_file(file_name)

    num_range = 52
    x = range(num_range)
        
    goertzel_out = [np.zeros(num_range) for i in range(16)]
    for i in range(num_range):
        for ch in range(16):
            #goertzel_out[ch][i] = goertzel.goertzel(vol[ch][i:64+i],2)
            goertzel_out[ch][i] = goertzel.goertzel(vol[ch][64*10 + i:64*10 + 64+i],2,vol[ch][64*10+i-1])
                
    print(goertzel_out[0])
    plt.figure(figsize=(15,9))
    for ch in range(16):
        plt.plot(x,goertzel_out[ch],linewidth=0.5,marker='v',markersize=1,label=str(ch))
        
    #plt.ylim(0,16*2**14)
    plt.xlim(0,num_range)
    plt.title(os.path.split(file_name)[1])
    #plt.tight_layout()
    plt.ylabel('ADC count')
    plt.xlabel('Delay clk')
    plt.grid()
    
    file_name = file_name.replace('/wave_','/process_')
    mom = decode_process.read_process_file(file_name)
    constant = 1/64e6 
    for ch in range(16):
        print(mom[10][ch]*constant) 
        
    plt.show()

