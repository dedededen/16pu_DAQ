
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
## python2&3  ok
import  numpy as np
import struct

DataLength = 65528
timestamplength = 19
headerLength = 6

def read_wave_file(fName):
    vol = []
    fid = open(fName, "rb")
    index = timestamplength
    for ch in range(1):
        #if b'wave' not in readX(fid,"4s",index) : print("ERROR: Header")
        while b'wave'+bytearray([ch]) != readX(fid,"5s",index):
            index += 1
        header_index = index
        fotter_index = header_index + headerLength + DataLength * 2
        #print(readX(fid,"10s",fotter_index+6))
        if b'data' != readX(fid,"4s",fotter_index) :
            print("ERROR: Data length is not match.")
        index = fotter_index #+ headerLength
        data_number = int( (-header_index + fotter_index - 6)/2)
        print('sampling number: '+str(data_number) +' ch:' + str(ch))
        fid.seek(header_index+6)
        vol.append(
            [ struct.unpack('B',fid.read(1))[0] * 64 +
             struct.unpack('B',fid.read(1))[0] /4 for i in range(data_number)]
            )
    return np.array(vol[0])

def readX( fid, fmt, adr=None ):
    """ extract a byte / word / float / double from the binary file """
    nBytes = struct.calcsize( fmt )
    fid.seek( adr )
    s = struct.unpack( fmt, fid.read( nBytes ) )
    return s[0]

def extract_peak(filename,buf,num=10):
    vol = read_wave_file(filename)
    vol_ft = np.abs(fft(vol))/len(vol)*2

    buf_ind = int(buf /108.8 *len(vol))
    vol_peak = np.max(vol_ft[buf_ind-5:buf_ind+5])
    
    index = np.argmax(vol_ft[buf_ind-5:buf_ind+5])+buf_ind-5
    freq = 108.8 * (index)/len(vol)

    peaks = []
    dt = int(108.8/buf+1) *num
    print(dt)
    num = len(vol)//dt
    for i in range(num):
        buf = (np.max(vol[i*dt:(i+1)*dt]) - np.min(vol[i*dt:(i+1)*dt]))/2
        peaks.append(buf)
        
    vol_peak1 = (np.max(vol) - np.min(vol))/2

    return vol_peak,vol_peak1,freq,np.mean(peaks),np.std(peaks)

ofset = '/jkdata/jkpublic/accbmon/mrbmon/16pu_data/data/20191014/wave_data/'
file_list = [
             'wave_2019_10_14_17_39_01.dat', ## 0.1
             'wave_2019_10_14_17_38_11.dat', ## 0.5
             'wave_2019_10_14_17_37_16.dat', ## 1
             'wave_2019_10_14_17_36_21.dat', ## 5
             'wave_2019_10_14_17_31_28.dat', ## 10
             'wave_2019_10_14_17_27_44.dat', ## 20
             'wave_2019_10_14_17_26_53.dat', ## 30
             'wave_2019_10_14_17_26_05.dat', ## 40
             'wave_2019_10_14_17_24_43.dat', ## 50
             'wave_2019_10_14_17_23_53.dat', ## 60
             'wave_2019_10_14_17_22_46.dat', ## 70
             'wave_2019_10_14_17_12_40.dat', ## 80
             'wave_2019_10_14_17_17_58.dat', ## 90
             'wave_2019_10_14_17_18_55.dat', ## 100
             'wave_2019_10_14_17_20_01.dat', ## 105
             ]

x = [0.1,0.5,1,5,10,20,30,40,50,60,70,80,90,100,105]
x_1 = []
y = []
y1 = []
y2 = []
ey2 = []
vo = 2**12
i = 0
for file in file_list:
    buf = extract_peak(ofset+file,x[i])
    x_1.append(buf[2])
    y.append(20*np.log10(buf[0]/vo))
    y1.append(20*np.log10(buf[1]/vo))
    y2.append(20*np.log10(buf[3]/vo))
    print(buf[3],buf[4])
    ey2.append(20*buf[4]/buf[3]/np.log(10))
    i += 1
#plt.plot(x,y)
plt.figure(figsize=(16,14))
plt.rcParams["font.size"] = 24
plt.tight_layout()
#plt.errorbar(x_1, y,  capsize=1, fmt='o', markersize=10, label='FFT peak')#yerr = y_err,
#plt.errorbar(x_1, y1,  capsize=1, fmt='o', markersize=10,label='peak-to-peak')#yerr = y_err,
plt.errorbar(x_1, y2,yerr=ey2,  capsize=1, fmt='o', markersize=7,label='peak-to-peak')#yerr = y_err,
#plt.xscale('log')
#plt.yscale('log')
#plt.legend()

print(x_1)
plt.grid()
plt.xlabel('[MHz]')
plt.ylabel('Amplitude[dB]')
#plt.xlim(0.5,105)
plt.savefig('/mnt/c/Users/pkpkp/Desktop/adc_fre.pdf')
plt.show()
