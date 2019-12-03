
from gui_design import gui
import sys
import os
import matplotlib.pyplot as plt
import numpy as np

from wave import plot_tmg
from wave import plot_wave
from wave import plot_bunch_moment
from wave import plot_fft
from wave import plot_all_mom
from process import plot_process
from process import plot_process_mom
from process import process_13_15
from process import betatron_13_15
from process import cal_process_mom
from noise import noise_analysis
from extract import extract_data
from extract import plot_pos
from extract import adiabatic_dump
from extract import betatron_ext
from reflectance import reflectance
from reflectance import process_ref
from BBA import BBA_cal

class Application(gui.Design,object):
    def __init__(self):
        super(Application,self).__init__()
        self.select.configure(command=self._select)

    def _select(self):
        self.mode_num = self.num_mode.get()
        ### Home
        if self.mode_num == 16:
            self.reflesh()
            return
        ### BBA
        elif self.mode_num == 10:
            BBA_cal.extract_cal_vol()
            return

        file_index = self.file_list.curselection()
        file_name = self.data_path+self.file_list.get(file_index[0]).replace('  ','')

        if not file_index: return
        ### extract
        elif self.mode_num == 5:
            extract_data.extract_vol(file_name)
        ### 
        elif os.path.isdir(file_name):
            self.reflesh(path=file_name)
        else : self.act_mode(file_name=file_name)
        
    def act_mode(self,file_name):
        self.mode_num = self.num_mode.get()
        ### beam data
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
        elif self.mode_num == 9:
            if 'wave_2' in file_name:
                self.memo(file_name)
                reflectance.plot_relation_reflectance(file_name)
            elif 'process_2' in file_name:
                self.memo(file_name)
                process_ref.plot_process_ref(file_name)
        ### #13 and #15
        elif self.mode_num == 3:
            if 'wave_2' in file_name:
                self.memo(file_name)
                #noise_analysis.wave_noise(file_name)
            elif 'process_2' in file_name:
                self.memo(file_name)
                process_13_15.plot_13_15(file_name)
        ### betatron osc. #13 and #15
        elif self.mode_num == 4:
            if 'wave_2' in file_name:
                self.memo(file_name)
                #noise_analysis.wave_noise(file_name)
            elif 'process_2' in file_name:
                self.memo(file_name)
                betatron_13_15.betatron(file_name)
            elif '.txt' in file_name:
                betatron_ext.plot_twiss(file_name)
        ### plot extract data
        elif self.mode_num == 6:
            if 'vol' in file_name:
                plot_pos.plot_row(file_name)

        ### plot extract data
        elif self.mode_num == 7:
            if 'vol' in file_name:
                adiabatic_dump.plot_dump(file_name)

                
                

if __name__=="__main__":
    app = Application()
    app.mainloop()
    
    
