
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
    for ch in range(16):
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
    if 'address13' in fName:
        buf = np.copy(vol[10])
        vol[10] = vol[11]
        vol[11] = buf
    elif 'address15' in fName:
        pass
    elif 'address0' in fName:
        pass
    else:
        buf = np.copy(vol[10])
        vol[10] = vol[11]
        vol[11] = buf

    return np.array(vol)

def readX( fid, fmt, adr=None ):
    """ extract a byte / word / float / double from the binary file """
    nBytes = struct.calcsize( fmt )
    fid.seek( adr )
    s = struct.unpack( fmt, fid.read( nBytes ) )
    return s[0]
    
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
    x = range(len(v[0]))
    plt.plot(x,v[0])
    plt.plot(x,v[1])
    plt.plot(x,v[2])
    plt.plot(x,v[3])
    plt.show()
