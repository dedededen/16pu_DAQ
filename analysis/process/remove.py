
import numpy as np

def remove(vol_goe):
    result = np.copy(vol_goe)
    num = 10
    try_num = int(len(vol_goe[:,0])/num)
    for i in range(try_num):
        for ch in range(16):
            me = np.mean(vol_goe[num*i:num*(i+1),ch])
            std = np.std(vol_goe[num*i:num*(i+1),ch])
            for j in range(num):
                if vol_goe[num*i+j,ch] < (me -5* std) or vol_goe[num*i+j,ch] > (me + 5*std):
                    print(ch,num*i+j)
                    result[num*i+j,ch] = None#1/constant
    return result
