


import numpy as np
path ='/jkdata/jkpublic/accbmon/mrbmon/16pu_data/16pu_DAQ/analysis/cal_mom/matrix/'

fre = ['_1-7MHz','_3-4MHz']
mon = ['_1st.txt','_2nd.txt']
gain = np.loadtxt(path+'../gain/gain_2nd.txt')
#gain = np.ones(16)

def moment(vol,num_fre=1,num_mon=1):
    invA = np.loadtxt(path+'invA'+fre[num_fre]+mon[num_mon])
    mom = np.dot(invA , vol*gain)
    mom[1:] /= mom[0]
    mom[3] -= mom[1]**2 - mom[2]**2
    mom[4] -= 2 * mom[1]*mom[2]
    return mom

def moment_8(vol,num_fre=1,num_mon=0,num=0):
    invA = np.loadtxt(path+'invA_8pu_'+str(num)+fre[num_fre]+mon[num_mon])
    mom = np.dot(invA , vol)
    mom[1:] /= mom[0]
    mom[3] -= mom[1]**2 - mom[2]**2
    mom[4] -= mom[1]*mom[2]
    return mom

