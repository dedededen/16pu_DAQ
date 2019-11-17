

import numpy as np
import matplotlib.pyplot as plt
import os
import cmath


from process import cal_process_mom

def plot_process_mom(file_name,vol):
    moment,bunch_on = cal_process_mom.process_mom(file_name,vol)
    
    fig = plt.figure()#figsize=(15,9))
    fig.suptitle(os.path.split(file_name)[1], fontsize=20)
    plt.subplots_adjust(top=0.9)
    num_bun = 9
    ax1 = fig.add_subplot(2, 2, 1)
    for i in range(num_bun):
        if bunch_on[i] == 0:
            continue
        x = range(len(moment[i][:,1]))
        ax1.plot(x,moment[i][:,1],label='bunch: '+str(i),marker='o',markersize =7) 
    ax1.legend()
    ax1.set_ylabel('x[mm]')
    ax1.set_xlabel('turn')
    ax1.grid()

    ax1_1 = fig.add_subplot(2, 2, 2)
    for i in range(num_bun):
        if bunch_on[i] == 0:
            continue
        x = range(len(moment[i][:,2]))
        ax1_1.plot(x,moment[i][:,2],label='bunch: '+str(i),marker='o',markersize =7) 
    ax1_1.legend()
    ax1_1.set_ylabel('y[mm]')
    ax1_1.set_xlabel('turn')
    ax1_1.grid()

    ax2 = fig.add_subplot(2, 2, 3)
    for i in range(num_bun):
        if bunch_on[i] == 0:
            continue
        x = range(len(moment[i][:,3]))
        ax2.plot(x,moment[i][:,3],label='bunch: '+str(i),marker='o',markersize =7)         
    ax2.legend()
    ax2.set_ylabel('sigma_x^2 - sigma_y^2[mm^2]')
    ax2.set_xlabel('turn')
    ax2.grid()

    ax3 = fig.add_subplot(2, 2, 4)
    for i in range(num_bun):
        if bunch_on[i] == 0:
            continue
        x = range(len(moment[i][:,4]))
        ax3.plot(x,moment[i][:,4],label='bunch: '+str(i),marker='o',markersize =7) 
    ax3.legend()
    ax3.set_ylabel('sigma_xy[mm^2]')
    ax3.set_xlabel('turn')
    ax3.grid()

    ### FFT
    fft_num = len(moment[i][:,1]) -1
    fig = plt.figure()#figsize=(15,9))
    fig.suptitle(os.path.split(file_name)[1], fontsize=20)
    plt.subplots_adjust(top=0.9)
    num_bun = 9
    ax1 = fig.add_subplot(2, 2, 1)
    for i in range(num_bun):
        if bunch_on[i] == 0:
            continue
        fft = np.fft.fft(moment[i][:fft_num,1])
        fft_abs = np.abs(fft) /fft_num*2
        max_index = np.argmax(fft_abs[int(fft_num*0.2):int(fft_num*0.5)]) + int(fft_num*0.2)
        x = np.linspace(0,1,len(moment[i][:fft_num,2]))#range(len(moment[i][:,1]))
        print('Dip. x Osc. max: ' + str(fft_abs[max_index])+'   Tune: ' + str(x[max_index])+ '   phase: ' + str(cmath.phase(fft[max_index])))
        ax1.plot(x,fft_abs,label='bunch: '+str(i),marker='o',markersize =7) 
        ax1.set_xlim(x[1],0.5)
    ax1.legend()
    ax1.set_yscale('log')
    #ax1.set_ylabel('x[mm]')
    #ax1.set_xlabel('turn')
    ax1.grid()

    ax1_1 = fig.add_subplot(2, 2, 2)
    for i in range(num_bun):
        if bunch_on[i] == 0:
            continue
        fft = np.fft.fft(moment[i][:fft_num,2])
        fft_abs = np.abs(fft) /fft_num*2
        max_index = np.argmax(fft_abs[int(fft_num*0.2):int(fft_num*0.5)]) + int(fft_num*0.2)
        x = np.linspace(0,1,len(moment[i][:fft_num,2]))#range(len(moment[i][:,1]))
        print('Dip. y Osc. max: ' + str(fft_abs[max_index])+'   Tune: ' + str(x[max_index])+ '   phase: ' + str(cmath.phase(fft[max_index])))
        ax1_1.plot(x,fft_abs,label='bunch: '+str(i),marker='o',markersize =7) 
        ax1_1.set_xlim(x[1],0.5)
    ax1_1.legend()

    ax1_1.set_yscale('log')
    #ax1_1.set_ylabel('y[mm]')
    #ax1_1.set_xlabel('turn')
    ax1_1.grid()

    fft_num = 15
    ax2 = fig.add_subplot(2, 2, 3)
    for i in range(num_bun):
        if bunch_on[i] == 0:
            continue
        x = np.linspace(0,1,len(moment[i][:fft_num,3]))#range(len(moment[i][:,1]))
        fft = np.fft.fft(moment[i][:fft_num,3])
        fft_abs = np.abs(fft) /fft_num*2
        max_index = np.argmax(fft_abs[3:]) + 3
        print('Quad. Osc. max: ' + str(fft_abs[max_index])+'   Tune: ' + str(x[max_index])+ '   phase: ' + str(cmath.phase(fft[max_index])))
        ax2.plot(x, fft_abs,label='bunch: '+str(i),marker='o',markersize =7) 
        ax2.set_xlim(x[1],0.5)
    ax2.legend()
    #ax2.set_ylabel('sigma_x^2 - sigma_y^2[mm^2]')
    #ax2.set_xlabel('turn')

    ax2.set_yscale('log')
    ax2.grid()
    plt.show()
