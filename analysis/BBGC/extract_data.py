
import numpy as np
import os

import decode_process

data_path = '/jkdata/jkpublic/accbmon/mrbmon/16pu_data/temp/'
bunch_num = 1
data_start = 1
data_end = 100

def extract_vol():
    measure_vol = []
    files = os.listdir(data_path)
    for file_name in files:
        print(file_name)
        vol_buf = decode_process.read_process_file(data_path + file_name)
        for i in range(data_start,data_end):
            measure_vol.append(vol_buf[i*9 + (bunch_num-1)])
    np.savetxt('./vol.txt',measure_vol)
    measure_vol = np.array(measure_vol)
    print(measure_vol.shape)
    return measure_vol

extract_vol()    
