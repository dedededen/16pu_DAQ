

import numpy as np
path ='/jkdata/jkpublic/accbmon/mrbmon/16pu_data/16pu_DAQ/analysis/matrix/'

fre = ['_1-7MHz','_3-4MHz']
mon = ['_1st.txt','_2nd.txt']

def cal_mom(vol,num_fre=1,num_mon=0):
    invA = np.loadtxt(path+'invA'+fre[num_fre]+mon[num_mon])
    mom = np.dot(invA , vol)
    mom[1:] /= mom[0]
    mom[3] -= mom[1]**2 - mom[2]**2
    mom[4] -= mom[1]*mom[2]
    return mom

def cal_mom_8(vol,num_fre=1,num_mon=0,num=0):
    invA = np.loadtxt(path+'invA_8pu_'+str(num)+fre[num_fre]+mon[num_mon])
    mom = np.dot(invA , vol)
    mom[1:] /= mom[0]
    mom[3] -= mom[1]**2 - mom[2]**2
    mom[4] -= mom[1]*mom[2]
    return mom

