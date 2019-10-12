
#import Tkinter
import tkinter as Tkinter
import sys
import numpy as np
import subprocess
import datetime
import os

import matplotlib.pyplot as plt
from analysis import decode_wave

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
        self.mFrame.place(relx=0, rely=0.7, relwidth=1, relheight=0.3)#, bg="red")
        
    def create_widgets(self):
        
        self.hi_there = Tkinter.Button(self.bFrame,text='Reload',command=self.reflesh)
        self.hi_there.pack(anchor=Tkinter.NW)
        self.hi_there.place(relx=0, rely=0.75)
        
        self.select = Tkinter.Button(self.bFrame, text="select/plot", command=self.select)
        #self.select.pack(anchor=Tkinter.NW)
        self.select.place(relx=0.5, rely=0.75)
        
        self.file_list = Tkinter.Listbox(self.lFrame ,selectmode='browse')
        self.reflesh()
        #self.file_list.pack(anchor=Tkinter.NW)
        #self.scroll_bar =Tkinter.Scrollbar(self.lFrame, command=self.file_list.yview)
        #self.scroll_bar.pack(side=Tkinter.RIGHT, fill="y")
        self.file_list.place(relx=0.05, rely=0.1,relheight=0.8,relwidth=0.8)
        #self.file_list.config(yscrollcommand=self.scroll_bar.set)

    def create_checkbox(self):
        self.iv1 = Tkinter.IntVar()
        self.iv1.set(0)
        Tkinter.Radiobutton(self.bFrame, text="memo", value=0, variable=self.iv1).place(relx=0., rely=0.15)
        Tkinter.Radiobutton(self.bFrame, text="time_domain", value=1, variable=self.iv1).place(relx=0., rely=0.25)
        Tkinter.Radiobutton(self.bFrame, text="frequency_domain", value=2, variable=self.iv1).place(relx=0., rely=0.35)
        Tkinter.Radiobutton(self.bFrame, text="delay_clock", value=3, variable=self.iv1).place(relx=0., rely=0.45)
        Tkinter.Radiobutton(self.bFrame, text="process", value=4, variable=self.iv1).place(relx=0., rely=0.55)
        Tkinter.Radiobutton(self.bFrame, text="turn-by-turn", value=4, variable=self.iv1).place(relx=0., rely=0.65)

    def create_memobox(self):
        self.textField = Tkinter.Text(self.mFrame, relief="groove")
        #self.textField.pack(side='bottom',anchor=Tkinter.S)
        self.textField.place(relx=0.1, rely=0.,relheight=0.8,relwidth=0.8)
        self.textField.insert('insert','-----------Memo------------\n')

    def create_quit(self):
        self.quit = Tkinter.Button(self.mFrame, text="EXIT", command=self.master.destroy)
        self.quit.place(relx=0.9, rely=0.8)
        
    def reflesh(self,path=data_path):
        self.data_path = path +'/'
        self.file_list.delete(0,'end')
        files = os.listdir(path)
        self.file_list.insert(0, 'file_list: '+path)
        for i in range(len(files)):
            self.file_list.insert(i+1, '  '+files[i])
        #self.file_list.pack()
        
    def select(self):
        file_index = self.file_list.curselection()
        file_name = self.data_path+self.file_list.get(file_index[0]).replace('  ','')
        if not file_index: return
        elif file_index[0] == 0 : self.reflesh()
        elif os.path.isdir(file_name):
            self.reflesh(path=file_name)
        elif '.dat' in file_name:
            num = self.iv1.get()
            if num != 0:
                self.plot(file_name,num)
            elif num == 0:
                self.memo(file_name)

    def plot(self,file_name,num):
        vol = decode_wave.read_wave_file(file_name)
        x = range(len(vol[0]))
        fig,axes = plt.subplots(nrows=4,ncols=4)
        for ch in range(16):
            axes[ch//4,ch%4].plot(x,vol[0],label=str(ch))
        plt.show()

    def memo(self,file_name):
        file_name = file_name.replace('/data', '/memo')
        file_name = file_name.replace('.dat','.txt')
        if os.path.exists(file_name):
            command = ['cat',file_name]
            p = subprocess.Popen(command, stdout=subprocess.PIPE)
            out = p.stdout.read()
            self.textField.insert('insert',file_name)
            self.textField.insert('insert',out)
        else:
            self.textField.insert('insert','memo is not exist\n')

root = Tkinter.Tk()
app = Application(master=root)
app.mainloop()
