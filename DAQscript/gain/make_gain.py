

import numpy as np

gain = [ np.ones(16) for i in range(3)]

name = ['test','add13','add15']
for i in range(3):
    ofile = './gain_' + name[i] + '.txt'
    np.savetxt(ofile,gain[i],delimiter=', ')


