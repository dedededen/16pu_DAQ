
#import Tkinter
import tkinter as Tkinter
import sys
import numpy as np
import subprocess
import datetime
import os

import matplotlib.pyplot as plt
from analysis import decode_wave
from analysis import decode_process

size = [800,600]
geometry_size = str(size[0]) +"x"+str(size[1])
data_path = './data'

class Application(Tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master,width=size[0], height=size[1])
        self.master.title(u"Analysis of 16-electrodes monitor")
        self.master.geometry(geometry_size)
        self.data_path = './data'        
        self.pack()
        self.create_frame()
        self.create_widgets()
        self.create_quit()
        self.create_checkbox()
        self.create_memobox()

    def create_frame(self):
        self.lFrame = Tkinter.Frame(self.master)
        self.lFrame.place(relx=0, rely=0,relwidth=0.5,relheight=0.7)

        self.bFrame = Tkinter.Frame(self.master)
        self.bFrame.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.7)

        self.mFrame = Tkinter.Frame(self.master)
        self.mFrame.place(relx=0, rely=0.7, relwidth=1, relheight=0.3)
        
    def create_widgets(self):
        self.select = Tkinter.Button(self.bFrame, text="select/plot", command=self.select)
        self.select.place(relx=0.5, rely=0.75)
        
        self.file_list = Tkinter.Listbox(self.lFrame ,selectmode='browse')
        self.reflesh()
        self.file_list.place(relx=0.05, rely=0.1,relheight=0.8,relwidth=0.8)

    def create_checkbox(self):
        self.iv1 = Tkinter.IntVar()
        self.iv1.set(0)
        Tkinter.Radiobutton(self.bFrame, text="waveform", value=0, variable=self.iv1).place(relx=0., rely=0.15)
        Tkinter.Radiobutton(self.bFrame, text="FFT", value=1, variable=self.iv1).place(relx=0., rely=0.25)
        Tkinter.Radiobutton(self.bFrame, text="delay_clock", value=2, variable=self.iv1).place(relx=0., rely=0.35)
        Tkinter.Radiobutton(self.bFrame, text="process", value=3, variable=self.iv1).place(relx=0., rely=0.45)

    def create_memobox(self):
        self.textField = Tkinter.Text(self.mFrame, relief="groove")
        #self.textField.pack(side='bottom',anchor=Tkinter.S)
        self.textField.place(relx=0.1, rely=0.,relheight=0.6,relwidth=0.8)
        self.textField.insert('insert','-----------Log------------\n')

    def create_quit(self):
        self.quit = Tkinter.Button(self.mFrame, text="EXIT", command=self.master.destroy)
        self.quit.place(relx=0.8, rely=0.7)
        
    def reflesh(self,path=data_path):
        self.data_path = path +'/'
        self.file_list.delete(0,'end')
        files = os.listdir(path)
        self.file_list.insert(1, './')
        self.file_list.insert(2, '../')
        for i in range(len(files)):
            self.file_list.insert(i+3, '  '+files[i])
        #self.file_list.pack()
        
    def select(self):
        file_index = self.file_list.curselection()
        file_name = self.data_path+self.file_list.get(file_index[0]).replace('  ','')
        if not file_index: return
        elif os.path.isdir(file_name):
            self.reflesh(path=file_name)
        elif 'wave' in file_name:
            self.memo(file_name)
            self.plot(file_name)
        elif 'process' in file_name:
            self.memo(file_name)
            decode_process.read_process_file(file_name)
            
    def plot(self,file_name):
        vol = decode_wave.read_wave_file(file_name)
        num = len(vol[0])
        num_range = 64*9
        x = range(num_range)
        for ch in range(16):
            plt.text(num_range*1.1,2**13+2**14*ch,'ch '+str(ch))
            [ plt.plot(x,vol[ch][i*num_range:(i+1)*num_range]+2**14*ch,c='black',linewidth=0.5) for i in range(int(num/num_range))]
        plt.ylim(0,16*2**14)
        plt.title(file_name)
        plt.show()
            

    def memo(self,file_name):
        file_name = file_name.replace('.dat','.txt')
        file_name = file_name.replace('wave_data','log')
        file_name = file_name.replace('process_data','log')
        file_name = file_name.replace('wave','log')
        file_name = file_name.replace('process','log')
        self.textField.delete('1.0','end')
        if os.path.exists(file_name):
            fd = open(file_name,'r')
            out = fd.read()
            self.textField.insert('insert',out)
        else:
            self.textField.insert('insert','Log is not exist\n')

root = Tkinter.Tk()
app = Application(master=root)
app.mainloop()
