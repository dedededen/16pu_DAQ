

import numpy as np

def goertzel(x,k):
    num = len(x)
    omega = 2 * np.pi * k / num
    s = np.zeros(num)
    for i in range(num):
        if i ==0:
            s[0] = x[0]
        elif i ==1:
            s[1] = x[1] +  2 * np.cos(omega) * s[0]
        else:
            s[i] = x[i] + 2 * np.cos(omega) * s[i-1] - s[i-2]
    re = s[63] - np.cos(omega) * s[62]
    im = np.sin(omega) * s[62]
    ans = np.sqrt(re**2 + im**2)
    return ans
