
import numpy as np
import matplotlib.pyplot as plt
from cal_mom import cal_mom

def process_mom(file_name,vol):
    bunch_on = np.zeros(9)
    num = vol.shape[0] -10
    moment = [ [] for i in range(9)]
    if "address15" in file_name:
        mon = 0
    else:
        mon = 1
    for i in range(num):
        if np.min(vol[i]) > 1:
            bunch_on[i%9] = 1
        mom = cal_mom.moment(vol[i],num_mon=mon)
        moment[i%9].append(mom)
    moment = [ np.array(moment[i]) for i in range(9)]
    return moment,bunch_on

def process_mom_bunch(file_name,vol,bunch_num):
    num = vol.shape[0] -10
    moment = []
    if "address15" in file_name:
        mon = 0
    else:
        mon = 1
    for i in range(num):
        if i%9 == bunch_num:
            mom = cal_mom.moment(vol[i],num_mon=mon)
            moment.append(mom)
    return np.array(moment)

def process_mom_true(file_name,vol):
    bunch_on = np.zeros(9)
    num = vol.shape[0] -10
    moment = [ [] for i in range(9)]
    if "address15" in file_name:
        mon = 0
    else:
        mon = 1
    for i in range(num):
        if np.min(vol[i]) > 1:
            bunch_on[i%9] = 1
        mom = cal_mom.true_moment(vol[i],num_mon=mon)
        moment[i%9].append(mom)
    moment = [ np.array(moment[i]) for i in range(9)]
    return moment,bunch_on
