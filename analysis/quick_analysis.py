
from gui_design import gui
import sys
import os
import matplotlib.pyplot as plt
import numpy as np

from wave import plot_tmg
from wave import plot_wave
from wave import plot_bunch_moment
from wave import plot_fft
from wave import reflectance
from wave import plot_all_mom
from process import plot_process
from process import plot_process_mom
from process import process_ref
from noise import noise_analysis

mode = {0:'Beam data',1:'Adjustment of timing',2:'Noise',3:'Reflectance',4:'all'}

class Application(gui.Design,object):
    def __init__(self,mode=0):
        super(Application,self).__init__()
        self.mode_num = mode
        self.select.configure(command=self._select)

    def _select(self):
        file_index = self.file_list.curselection()
        file_name = self.data_path+self.file_list.get(file_index[0]).replace('  ','')
        if not file_index: return
        elif os.path.isdir(file_name):
            self.reflesh(path=file_name)
        else : self.act_mode(file_name=file_name)

    def act_mode(self,file_name):
        print(self.mode_num)
        ### beam time
        if self.mode_num == 0:
            if 'wave_2' in file_name:
                self.memo(file_name)
                vol,mon = plot_wave.plot_wave(file_name)
                plot_bunch_moment.plot_bunch_moment(file_name,vol,mon)
                plot_fft.plot_fft(file_name,vol)
            elif 'process_2' in file_name:
                self.memo(file_name)
                vol = plot_process.plot_process(file_name)
                plot_process_mom.plot_process_mom(file_name,vol)
        ### adjust timing
        elif self.mode_num == 1:
            print(file_name)
            if 'wave_2' in file_name:
                self.memo(file_name)
                plot_tmg.plot_timing(file_name)
        ### noise
        elif self.mode_num == 2:
            if 'wave_2' in file_name:
                self.memo(file_name)
                noise_analysis.wave_noise(file_name)
            elif 'process_2' in file_name:
                self.memo(file_name)
                noise_analysis.process_noise(file_name)
        ### reflectance
        elif self.mode_num == 3:
            if 'wave_2' in file_name:
                self.memo(file_name)
                reflectance.plot_relation_reflectance(file_name)
            elif 'process_2' in file_name:
                self.memo(file_name)
                process_ref.plot_process_ref(file_name)
        ### all
        elif self.mode_num == 4:
            if 'wave_2' in file_name[0]:
                self.memo(file_name[0])
                plot_all_mom.plot_mom(file_name)
            elif 'process_2' in file_name[0]:
                self.memo(file_name[0])
                
                

if __name__=="__main__":
    args = sys.argv
    if len(sys.argv) == 1:
        print('argv is None.')
        print('[USAGE]: python quick_analysis.py #mode number')
        for i in range(len(mode)):
            print('\t mode ' +str(i) +' : ' +mode[i])
    else:
        print('Begin in mode ' + str(args[1]) +'\t'+ mode[int(args[1])])
        app = Application(mode=int(args[1]))
        app.mainloop()
    
    
