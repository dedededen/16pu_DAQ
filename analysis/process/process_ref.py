

import numpy as np
import matplotlib.pyplot as plt
import os

from process import decode_process

def plot_process_ref(file_name):
    mom = decode_process.read_process_file(file_name)
    #mom = remove(mom)
    num = int(len(mom[:,0]) * 0.9)
    
    for j in range(16):
        plt.subplot(4,4,j+1)
        plt.scatter(mom[:num:9,j]*constant,mom[2:num+2:9,j]*constant,label=str(j))
        
    plt.ylabel('bunch2')
    plt.xlabel('bunch0')
    plt.title(os.path.split(file_name)[1])
    #plt.legend(loc="upper center", ncol=4)
    plt.show()
