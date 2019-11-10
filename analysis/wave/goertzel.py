

import numpy as np
def goertzel(x,k,x_1=0):

    num = len(x)
    omega = 2 * np.pi * k / num
    s = np.zeros(num)
    for i in range(num):
        if i ==0:
            s[0] = x[0] + 2 * np.cos(omega) * x_1
        elif i ==1:
            s[1] = x[1] +  2 * np.cos(omega) * s[0] - x_1
        else:
            s[i] = x[i] + 2 * np.cos(omega) * s[i-1] - s[i-2]
    re = s[num-1] - np.cos(omega) * s[num-2]
    im = np.sin(omega) * s[num-2]
    ans = np.sqrt(re**2 + im**2)/num*2

    return ans/num*2,np.arctan(im/re)
