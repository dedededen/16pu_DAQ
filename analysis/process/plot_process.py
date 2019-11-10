
import numpy as np
import matplotlib.pyplot as plt
import os

from process import decode_process

def plot_process(file_name):
    mom = decode_process.read_process_file(file_name)
    fig = plt.figure(figsize=(15,9))
    for j in range(16):
        for k in range(9):
            plt.subplot(3,3,k+1)
            plt.plot(range(len(mom[k:-10:9,j])),mom[k:-10:9,j],linewidth=0.5,marker='v',markersize=1,label=str(j))
    #plt.legend()
    plt.ylabel('ADC count')
    plt.xlabel('turn number')
    fig.suptitle(os.path.split(file_name)[1], fontsize=20)
    #plt.legend(loc="upper center", ncol=4)
    #plt.show()
    return mom
