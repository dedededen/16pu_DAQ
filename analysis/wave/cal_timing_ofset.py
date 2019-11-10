
import numpy as np
def cal_offset(vol,teibai=52): ## timing
    off = teibai*9*10
    aaa = []
    min_power = 1000
    for i in range(teibai*9):
        if np.sum(np.abs(vol[0][off+i-teibai+1:off+i]-np.mean(vol[0]))) < min_power:
            aaa.append(i)
    for i in aaa:
        if np.abs(vol[0][off+i] - vol[0][off+i+10]) > 50 :
            break
    for j in range(10):
        if np.sum(np.abs(vol[0][i+j*teibai*9:i+j*teibai*9+teibai]-np.mean(vol[0]))) > min_power*0.1:
            break
    print(i,j)
    return i-2,j    
