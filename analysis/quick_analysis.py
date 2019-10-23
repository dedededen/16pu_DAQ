
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
import goertzel

size = [800,700]
geometry_size = str(size[0]) +"x"+str(size[1])
data_path = './data'

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
        
        self.file_list = Tkinter.Listbox(self.lFrame ,selectmode='browse')
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
        file_name = self.data_path+self.file_list.get(file_index[0]).replace('  ','')
        if not file_index: return
        elif os.path.isdir(file_name):
            self.reflesh(path=file_name)
        elif 'wave_2' in file_name:
            self.memo(file_name)
            vol = self.plot_wave(file_name)
            self.plot_fft(file_name,vol)
        elif 'process_2' in file_name:
            self.memo(file_name)
            self.plot_process(file_name)
            
            
    def plot_wave(self,file_name):
        vol = decode_wave.read_wave_file(file_name)
        num = len(vol[0])
        num_range = 64*9
        #x = range(num)
        x = range(num_range)
        
        # ## test for delay clock
        # for i in range(30):
        #     test = goertzel.goertzel(vol[8][i:64+i],2)/64*2
        #     print('delay: '+str(i))
        #     print(test)
        # ### test
        plt.figure(figsize=(15,9))
        for ch in range(16):
            vol_max = np.max(vol[ch])
            vol_min = np.min(vol[ch])
            plt.text(num_range*1.,2**13+2**14*ch,'ch '+str(ch))
            plt.text(num_range*1.05,2**13+2**14*ch,'Max '+str(vol_max))
            plt.text(num_range*1.05,2**12+2**14*ch,'Min '+str(vol_min))
            plt.text(num_range*1.05,2**10+2**14*ch,'p-p '+str(vol_max-vol_min))

            #plt.plot(x,vol[ch]+2**14*ch,c='blue',linewidth=0.5)
            [ plt.plot(x,vol[ch][i*num_range:(i+1)*num_range]+2**14*ch,c='blue',linewidth=0.5)
             for i in range(int(num/num_range))]
        plt.ylim(0,16*2**14)
        plt.xlim(0,num_range)
        plt.title(os.path.split(file_name)[1])
        #plt.tight_layout()
        plt.ylabel('ADC count + 2^{14}*ch')
        plt.xlabel('sampling number % 1 turn')
        plt.grid()
        #plt.show()
        return vol
    
    def plot_fft(self,file_name,vol):
        num = len(vol[0])
        plt.figure(figsize=(15,9))
        x = np.linspace(0, 1.7*64, num)
        for ch in range(16):
            vol_ft = np.abs(np.fft.fft(vol[ch]))/num*2
            plt.plot(x,vol_ft,linewidth=0.5,label=str(ch))
        plt.legend()
        plt.yscale('log')
        plt.ylim(1e-4,2**14)
        plt.xlim(0,x[-1]/2)
        plt.title(os.path.split(file_name)[1])
        #plt.tight_layout()
        plt.ylabel('ADC count')
        plt.xlabel('Frequecy[MHz]')
        plt.grid()
        plt.show()
        
    def plot_process(self,file_name):
        mom = decode_process.read_process_file(file_name)
        num = len(mom[:,0])
        x = range(num)
        for j in range(16):
            #plt.text(num_range*1.1,2**13+2**14*ch,'ch '+str(ch))
            plt.plot(x,mom[:,j]/64e6,linewidth=0.5,marker='v',markersize=1,label=str(j))
        #plt.ylim(0,16*2**14)
        plt.yscale('log')
        plt.legend()
        plt.ylabel('ADC count')
        plt.xlabel('bunch number')
        plt.title(os.path.split(file_name)[1])
        plt.legend(loc="upper center", ncol=4)
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
