
import numpy as np
#beta = np.array([[39.7,-5.9],[14.6,-30.6]]) #13,15
beta = np.array([[39.822,-6.717],[15.595,-29.998]]) #13,15
#beta = np.array([[1,-1],[1./2.73,-1./0.216]]) #13,15
inv_beta = np.linalg.inv(beta)
num_bun = 9

def emittance(mom13,mom15):
    num = len(mom13[0][:,3])
    emi = [[] for i in range(num_bun)] 
    for i in range(num_bun):
        for j in range(num-1):
            quad = np.array([mom13[i][j,3],mom15[i][j,3]])
            emi[i].append(np.dot(inv_beta,quad))
        emi[i] = np.array(emi[i])
    return emi,beta

def emittance0(mom13,mom15):
    quad = np.array([mom13,mom15])
    emi = np.dot(inv_beta,quad)
    return emi
    
