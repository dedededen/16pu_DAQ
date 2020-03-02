
import numpy as np
path ='/jkdata/jkpublic/accbmon/mrbmon/16pu_data/16pu_DAQ/analysis/cal_mom/matrix/'

fre = ['_1-7MHz','_3-4MHz','_5-1MHz']
mon = ['_1st.txt','_2nd.txt']
gain = [np.loadtxt(path+'../gain/gain_1st.txt'),np.loadtxt(path+'../gain/gain_2nd.txt'),np.ones(16)]
gain = [np.loadtxt(path+'../gain_20200120_b/gain_1st.txt'),np.loadtxt(path+'../gain_20200120_b/gain_2nd.txt'),np.ones(16)] ## BBA

#gain = [np.ones(16),np.ones(16)]
pos_off = [[-0.25069580086359916,1.0363901454673603],
           [0.7799954861648153 ,-0.17114181002093012]]
           
def moment(vol,num_fre=1,num_mon=1):
    invA = np.loadtxt(path+'invA'+fre[num_fre]+mon[num_mon])
    mom = np.dot(invA , vol*gain[num_mon])
    #mom = np.dot(invA , vol*gain[num_mon]/np.sum(gain[num_mon]*vol[:]))
    mom[1:] /= mom[0]

    mom[3] -= mom[1]**2 - mom[2]**2
    mom[4] -= 2 * mom[1]*mom[2]
    #mom[1] -= pos_off[num_mon][0]
    #mom[2] -= pos_off[num_mon][1]
    return mom

def true_moment(vol,num_fre=1,num_mon=1):
    invA = np.loadtxt(path+'invA'+fre[num_fre]+mon[num_mon])
    mom = np.dot(invA , vol*gain[num_mon])
    mom[1:] /= mom[0]
    return mom

def moment_sub(vol,num_fre=1,num_mon=1):
    invA = np.loadtxt(path+'invA'+fre[num_fre]+mon[num_mon])
    mom_buf = np.dot(invA , vol*gain[num_mon])
    mom = np.copy(mom_buf)
    mom[1:] /= mom[0]
    mom[3] -= mom_buf[1]**2 - mom_buf[2]**2
    mom[4] -= 2 * mom_buf[1]*mom_buf[2]
    mom[5] -=   3 * mom_buf[1] * mom_buf[3] - 6 * mom_buf[2] * mom_buf[4] + 2 * (mom_buf[1]**3 - 3*mom_buf[1]*mom_buf[2]**2)
    mom[6] -= - 3 * mom_buf[2] * mom_buf[3] + 6 * mom_buf[1] * mom_buf[4] - 2 * (mom_buf[2]**3 - 3*mom_buf[2]*mom_buf[1]**2)
    return mom

def moment_8(vol,num_fre=1,num_mon=1,num=0):
    invA = np.loadtxt(path+'invA_8pu_'+str(num)+fre[num_fre]+mon[num_mon])
    mom = np.dot(invA , vol*gain[num_mon][num::2])
    mom[1:] /= mom[0]
    mom[3] -= mom[1]**2 - mom[2]**2
    mom[4] -= mom[1]*mom[2]
    mom[1] -= pos_off[num_mon][0]
    mom[2] -= pos_off[num_mon][1]
    return mom

