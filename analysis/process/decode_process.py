
### python2 & python3 OK
import  numpy as np
import struct
from reflectance import extract_ref

DataLength = 65528
timestamplength = 19
headerLength = 6

Header = b"TRANSVERSE MOMENTs measured with sixteen-pu-monitor at address 15"
Footer = b"DATA"# processed with the 16-pu-monitor circuit"
constant = 1/64e6 *52/64

def read_process_file(fName):
    mom = []
    fid = open(fName, "rb")
    fid.seek(0)
    timestamp = struct.unpack('19s',fid.read(19))[0]
    if Header!=struct.unpack('65s',fid.read(65))[0]:
        print('Error: Header')
        return
    #print('Gain: ')
    for ch in range(16):
        g = 2**(-15)* (struct.unpack('B',fid.read(1))[0]*256 + struct.unpack('B',fid.read(1))[0])
        #print('ch: ' + str(g))
    data_amount =  struct.unpack('B',fid.read(1))[0]*65536 + struct.unpack('B',fid.read(1))[0]*256 + struct.unpack('B',fid.read(1))[0]
    print('data amount: ' + str(data_amount))

    for i in range(data_amount):
        data_per_bunch = np.zeros(16)
        data_number = struct.unpack('B',fid.read(1))[0]*256+struct.unpack('B',fid.read(1))[0];
        #print(data_number)
        if data_number != i:
            break
        for j in range(16):
            data_0 = struct.unpack('B',fid.read(1))[0] 
            #print(data_0)
            exp = ( data_0 & 0x7c) >> 2
            #print(exp)
            frac = ( data_0 & 0x03) * 65536 + struct.unpack('B',fid.read(1))[0] * 256 + struct.unpack('B',fid.read(1))[0]
            if (data_0>0):
                data_per_bunch[j] =  frac * 2**exp * constant
            else:
                data_per_bunch[j] = frac * 2**exp *(-1) * constant
        mom.append(data_per_bunch)

    #if Footer != struct.unpack('45s',fid.read(45))[0]:
    if Footer != struct.unpack('4s',fid.read(4))[0]:
        print('Error: Footer')        
        #return
    mom = np.array(mom)
    if 'address13' in fName:
        buf  = np.copy(mom[:,10])
        mom[:,10] = mom[:,11]
        mom[:,11] = buf
    elif 'address15' in fName:
        pass
    elif 'address0' in fName:
        pass
    else:
        pass
    #mom = extract_ref.remove_ref(mom,fName)
    return mom
    
if __name__=='__main__':
    ifile ='./data/wave_data/wave_822.dat'
    if '.dat' in ifile: pass
    else:
        print("Usage   : python decode_wave.py [filename]")
        print("example : python decode_wave.py wave_1789_07_14_12_15_30")

    import time
    start = time.time()
    v = read_wave_file(ifile)
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    
    import matplotlib.pyplot as plt





    
