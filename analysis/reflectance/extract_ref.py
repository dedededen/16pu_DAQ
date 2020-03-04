
import numpy as np

def remove_ref(vol,fName):
    vol_true = np.copy(vol)
    if 'address13' in fName:
        ref_par = np.loadtxt('/jkdata/jkpublic/accbmon/mrbmon/16pu_data/16pu_DAQ/analysis/reflectance/address13_ref.txt')
        ref_delay = 2
        print('13')
    elif 'address15' in fName:
        ref_par = np.loadtxt('/jkdata/jkpublic/accbmon/mrbmon/16pu_data/16pu_DAQ/analysis/reflectance/address15_ref.txt')
        ref_delay = 1
        print('15')
    num = len(vol[:,0])

    for i in range(num-2):
        if vol[i][0] > 10:
            for ch in range(16):
                vol_true[i+ref_delay][ch] = vol_true[i][ch] * ref_par[0][ch]  *(
                    -1* np.cos(ref_par[2][ch]) +
                     np.sqrt(
                        np.cos(ref_par[2][ch])**2+
                        (vol[i+ref_delay][ch]/vol_true[i][ch] / ref_par[0][ch])**2
                        - 1
                        )
                     )
        
    return vol_true
