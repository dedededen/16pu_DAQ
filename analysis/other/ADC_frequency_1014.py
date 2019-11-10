
import decode_wave
import numpy as np
import matplotlib.pyplot as plt
#from scipy.fftpack import fft

def extract_peak(filename):
    vol = decode_wave.read_wave_file(filename)
    vol_ft = np.fft.fft(vol[0])
    vol_ft = np.abs(vol_ft) / len(vol[0])*2
    vol_peak = np.max(vol_ft[1:])
    index = np.argmax(vol_ft[1:])
    freq = 108.8/len(vol[0]) * (index+1)
    return vol_peak,freq


file_list = [
             '../data/20191014/wave_data/wave_2019_10_14_17_39_01.dat', ## 0.1
             '../data/20191014/wave_data/wave_2019_10_14_17_38_11.dat', ## 0.5
             '../data/20191014/wave_data/wave_2019_10_14_17_37_16.dat', ## 1
             '../data/20191014/wave_data/wave_2019_10_14_17_36_21.dat', ## 5
             '../data/20191014/wave_data/wave_2019_10_14_17_31_28.dat', ## 10
             '../data/20191014/wave_data/wave_2019_10_14_17_27_44.dat', ## 20
             '../data/20191014/wave_data/wave_2019_10_14_17_26_53.dat', ## 30
             '../data/20191014/wave_data/wave_2019_10_14_17_26_05.dat', ## 40
             '../data/20191014/wave_data/wave_2019_10_14_17_24_43.dat', ## 50
             '../data/20191014/wave_data/wave_2019_10_14_17_23_53.dat', ## 60
             '../data/20191014/wave_data/wave_2019_10_14_17_22_46.dat', ## 70
             '../data/20191014/wave_data/wave_2019_10_14_17_12_40.dat', ## 80
             '../data/20191014/wave_data/wave_2019_10_14_17_17_58.dat', ## 90
             '../data/20191014/wave_data/wave_2019_10_14_17_18_55.dat', ## 100
             '../data/20191014/wave_data/wave_2019_10_14_17_20_01.dat', ## 105
             ]

x = [0.1,0.5,1,5,10,20,30,40,50,60,70,80,90,100,105]
x_1 = []
y = []
vo = 2**12
for file in file_list:
    buf = extract_peak(file)
    x_1.append(buf[1])
    y.append(20*np.log10(buf[0]/vo))
plt.plot(x,y)
plt.xscale('log')
#plt.yscale('log')
print(x_1)
plt.show()
