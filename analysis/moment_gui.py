
import sys
ver_python = sys.version_info[0]
if ver_python == 2:import Tkinter
else : import tkinter as Tkinter
import numpy as np
import subprocess
import datetime
import os

import matplotlib.pyplot as plt
import decode_wave
import decode_process
import waveform_analysis
import process_analysis

size = [800,700]
geometry_size = str(size[0]) +"x"+str(size[1])
data_path = '/jkdata/jkpublic/accbmon/mrbmon/16pu_data'

class Application(Tkinter.Frame,object):
    def __init__(self, master=None):
        super(Application,self).__init__(master,width=size[0], height=size[1])
        self.master.title(u"Analysis of 16-electrodes monitor")
        self.master.geometry(geometry_size)
        self.data_path = data_path
        self.pack()
        self.create_frame()
        self.create_widgets()
        self.create_quit()
        self.create_memobox()

    def create_frame(self):
        self.lFrame = Tkinter.Frame(self.master)
        self.lFrame.place(relx=0, rely=0,relwidth=0.5,relheight=1)

        self.mFrame = Tkinter.Frame(self.master)
        self.mFrame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)
        
    def create_widgets(self):
        self.select = Tkinter.Button(self.lFrame, text="select", command=self.select)
        self.select.place(relx=0.7, rely=0.925)
        
        self.file_list = Tkinter.Listbox(self.lFrame,selectmode=Tkinter.EXTENDED)
        self.reflesh()
        self.file_list.place(relx=0.1, rely=0.1,relheight=0.8,relwidth=0.8)

    def create_memobox(self):
        self.textField = Tkinter.Text(self.mFrame, relief="groove")
        #self.textField.pack(side='bottom',anchor=Tkinter.S)
        self.textField.place(relx=0.1, rely=0.1,relheight=0.8,relwidth=0.8)
        self.textField.insert('insert','-----------Log------------\n')

    def create_quit(self):
        self.quit = Tkinter.Button(self.mFrame, text="EXIT", command=self.master.destroy)
        self.quit.place(relx=0.7, rely=0.925)
        
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
        file_name = [ self.data_path+self.file_list.get(index).replace('  ','') for index in file_index ]
        if not file_index: return
        elif os.path.isdir(file_name[0]):
            self.reflesh(path=file_name[0])
        elif 'wave_2' in file_name[0]:
            self.memo(file_name[0])
            waveform_analysis.plot_mom(file_name)
        elif 'process_2' in file_name[0]:
            self.memo(file_name[0])
            process_analysis.plot_process_mom(file_name[0])
            ifile = file_name[0].replace('process','wave')
            waveform_analysis.plot_bunch_moment(ifile)

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
