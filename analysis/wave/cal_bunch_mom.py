
import numpy as np

from wave import cal_timing_ofset
from wave import goertzel
from cal_mom import cal_mom

def cal_bunch_moment(vol,teibai=52,mon=0):
    bunch_of,off2 =cal_timing_ofset.cal_offset(vol)
    num = int((len(vol[0])-bunch_of)/teibai) - off2*9 - 11
    moment = []
    
    for i in range(num):
        hoge = off2*teibai*9 + bunch_of +teibai*i
        buf= [ goertzel.goertzel(vol[ch][hoge:hoge+teibai],2)[0]
              for ch in range(16)]# 11/4[4,3,2,1,0,15,14,13,12,11,10,9,8,7,6,5]]
#range(16)]
        
        buf2 = cal_mom.moment(buf,num_mon=mon)
        moment.append(buf2)
    return np.array(moment)
