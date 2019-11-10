
import numpy as np
import matplotlib.pyplot as plt
from cal_mom import cal_mom

def process_mom(file_name,vol):
    num = vol.shape[0] -10
    moment = [ [] for i in range(9)]
    if "address15" in file_name[0]:
        mon = 0
    else:
        mon = 1
    for i in range(num):
        mom = cal_mom.moment(vol[i],num_mon=mon)
        moment[i%9].append(mom)
    moment = [ np.array(moment[i]) for i in range(9)]
    return moment
