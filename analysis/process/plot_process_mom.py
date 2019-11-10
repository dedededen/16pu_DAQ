

import numpy as np
import matplotlib.pyplot as plt
import os


from process import cal_process_mom

def plot_process_mom(file_name,vol):
    moment = cal_process_mom.process_mom(file_name,vol)
    
    fig = plt.figure()#figsize=(15,9))
    fig.suptitle(os.path.split(file_name)[1], fontsize=20)
    plt.subplots_adjust(top=0.9)
    num_bun = 2
    ax1 = fig.add_subplot(2, 2, 1)
    for i in range(num_bun):
        x = range(len(moment[i][:,1]))
        ax1.plot(x,moment[i][:,1],label='bunch: '+str(i),marker='o',markersize =7) 
    ax1.legend()
    ax1.set_ylabel('x[mm]')
    ax1.set_xlabel('turn')
    ax1.grid()

    ax1_1 = fig.add_subplot(2, 2, 2)
    for i in range(num_bun):
        x = range(len(moment[i][:,2]))
        ax1_1.plot(x,moment[i][:,2],label='bunch: '+str(i),marker='o',markersize =7) 
    ax1_1.legend()
    ax1_1.set_ylabel('y[mm]')
    ax1_1.set_xlabel('turn')
    ax1_1.grid()

    ax2 = fig.add_subplot(2, 2, 3)
    for i in range(num_bun):
        x = range(len(moment[i][:,3]))
        ax2.plot(x,moment[i][:,3],label='bunch: '+str(i),marker='o',markersize =7)         
    ax2.legend()
    ax2.set_ylabel('sigma_x^2 - sigma_y^2[mm^2]')
    ax2.set_xlabel('turn')
    ax2.grid()

    ax3 = fig.add_subplot(2, 2, 4)
    for i in range(num_bun):
        x = range(len(moment[i][:,4]))
        ax3.plot(x,moment[i][:,4],label='bunch: '+str(i),marker='o',markersize =7) 
    ax3.legend()
    ax3.set_ylabel('sigma_xy[mm^2]')
    ax3.set_xlabel('turn')
    ax2.grid()
    plt.show()

