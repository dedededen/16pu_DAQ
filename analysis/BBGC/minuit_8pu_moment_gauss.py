
import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit

### data
measure_vol = np.loadtxt("vol.txt")

### matrix  invA_8pu_1_1-7MHz_1st.txt*
inv_A_8 = [ np.loadtxt("./matrix/invA_8pu_"+str(i) +"_3-4MHz_2nd.txt") for i in range(2) ]

mom_num = 10
try_num = 1 
initial_par = [1. for i in range(16)]
error = [1e-4 for i in range(16)]
fix_par = [False  for i in range(16)]
fix_par[0] = True
limit_par = [[0.95,1.05] for i in range(16)]

    
def pos(par):
    sum_mom  = [0 for i in range(mom_num)]
    shot_num = measure_vol.shape[0]
    #mom_8_0 = np.array([np.dot(inv_A_8[0],par[::2]*measure_vol[n][::2]/np.sum(par[::2]*measure_vol[n][::2])) for n in range(shot_num)])
    #mom_8_1 = np.array([np.dot(inv_A_8[1],par[1::2]*measure_vol[n][1::2]/np.sum(par[1::2]*measure_vol[n][1::2])) for n in range(shot_num)])
    mom_8_0 = np.array([np.dot(inv_A_8[0],par[::2]*measure_vol[n][::2]) for n in range(shot_num)])
    mom_8_1 = np.array([np.dot(inv_A_8[1],par[1::2]*measure_vol[n][1::2]) for n in range(shot_num)])
    sum_mom[0] = np.sum((mom_8_0[:,0]-mom_8_1[:,0])**2)
    sum_mom[1] = np.sum((mom_8_0[:,1]-mom_8_1[:,1])**2)
    sum_mom[2] = np.sum((mom_8_0[:,2]-mom_8_1[:,2])**2)
    sum_mom[3] = np.sum((mom_8_0[:,3]-mom_8_1[:,3])**2)
    sum_mom[4] = np.sum((mom_8_0[:,4] - 2 * mom_8_0[:,1] * mom_8_0[:,2] /mom_8_0[:,0])**2)
    sum_mom[5] = np.sum((mom_8_1[:,4] - 2 * mom_8_1[:,1] * mom_8_1[:,2] /mom_8_1[:,0])**2)
    sum_mom[6] = np.sum((mom_8_0[:,5] - 3 * mom_8_0[:,1] * mom_8_0[:,3] / mom_8_0[:,0] + 2 * mom_8_0[:,1]**3 / mom_8_0[:,0]**2) **2)
    sum_mom[7] = np.sum((mom_8_1[:,5] - 3 * mom_8_1[:,1] * mom_8_1[:,3] / mom_8_1[:,0] + 2 * mom_8_1[:,1]**3 / mom_8_1[:,0]**2) **2)
    sum_mom[8] = np.sum((mom_8_0[:,6] - 3 * mom_8_0[:,2] * mom_8_0[:,3] / mom_8_0[:,0] - 2 * mom_8_0[:,2]**3 / mom_8_0[:,0]**2) **2)
    sum_mom[9] = np.sum((mom_8_1[:,6] - 3 * mom_8_1[:,2] * mom_8_1[:,3] / mom_8_1[:,0] - 2 * mom_8_1[:,2]**3 / mom_8_1[:,0]**2) **2)
    #sum_mom[10] = np.sum((mom_8_0[:,7] - 3 * mom_8_0[:,3] **2/ mom_8_0[:,0] + 2 * mom_8_0[:,1]**4 / mom_8_0[:,0]**3+ 2 * mom_8_0[:,2]**4 / mom_8_0[:,0]**3) **2)
    return sum_mom[0] * sum_mom[1] * sum_mom[2] * sum_mom[3] * sum_mom[4] * sum_mom[5] * sum_mom[6] *sum_mom[7]*sum_mom[8]*sum_mom[9] #*sum_mom[10]

def minimum(flag):
    print('init '+ str(pos(initial_par)))
    m_pos = Minuit.from_array_func( pos,initial_par, error, fix=fix_par, limit=limit_par, errordef=0.5) #1
    #print(m_pos.get_param_states())
    print('Get minimum!!!!')
    for i in range(try_num):
        m_pos.migrad()
        print('end '+str(i)+'  ' + str(pos(m_pos.np_values())))
        m_pos = Minuit.from_array_func(pos,m_pos.np_values(), error, fix=fix_par, limit=limit_par, errordef=0.5) #1
        print(m_pos.np_values())
    gain = m_pos.np_values()
    gain_e = m_pos.np_errors()
    return gain,gain_e

def plot_gain():
    gain,gain_e = minimum(0)
    np.savetxt('./gain_2nd.txt',gain)
    np.savetxt('./gain_e_2nd.txt',gain_e)
    print(gain,gain_e)
    
if __name__ == '__main__':
    plot_gain()
    
