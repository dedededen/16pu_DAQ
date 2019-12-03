
import sys
ver_python = sys.version_info[0]
if ver_python == 2:import Tkinter
else : import tkinter as Tkinter
import numpy as np
import os

size = [1200,700]
geometry_size = str(size[0]) +"x"+str(size[1])
data_path = '/jkdata/jkpublic/accbmon/mrbmon/16pu_data'

class Design(Tkinter.Frame,object):
    def __init__(self, master=Tkinter.Tk()):
        super(Design,self).__init__(master,width=size[0], height=size[1])
        self.master.title(u"Analysis of 16-electrodes monitor")
        self.master.geometry(geometry_size)
        self.data_path = data_path
        self.pack()
        self.create_frame()
        self.create_mode()
        self.create_widgets()
        self.create_quit()
        self.create_memobox()

    def create_frame(self):
        self.lFrame = Tkinter.Frame(self.master)
        self.lFrame.place(relx=0, rely=0,relwidth=0.5,relheight=1)
        
        self.modeFrame = Tkinter.Frame(self.master)
        self.modeFrame.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.6)

        self.mFrame = Tkinter.Frame(self.master)
        self.mFrame.place(relx=0.5, rely=0.6, relwidth=0.5, relheight=0.4)

    def create_mode(self):
        self.num_mode = Tkinter.IntVar()
        self.num_mode.set(0)
        Tkinter.Radiobutton(self.modeFrame, text="Beam", value=0,
                            variable=self.num_mode).place(relx=0.1, rely=0.1)
        Tkinter.Radiobutton(self.modeFrame, text="Adjust timing(Wave Only)", value=1,
                            variable=self.num_mode).place(relx=0.1, rely=0.2)
        Tkinter.Radiobutton(self.modeFrame, text="Noise", value=2,
                            variable=self.num_mode).place(relx=0.1, rely=0.3)
        Tkinter.Radiobutton(self.modeFrame, text="#13 and #15", value=3,
                            variable=self.num_mode).place(relx=0.1, rely=0.4)
        Tkinter.Radiobutton(self.modeFrame, text="Betatron Osc.(for inj. #13 & #15)", value=4,
                            variable=self.num_mode).place(relx=0.1, rely=0.5)
        Tkinter.Radiobutton(self.modeFrame, text="Extract vol. in .txt", value=5,
                            variable=self.num_mode).place(relx=0.1, rely=0.6)
        Tkinter.Radiobutton(self.modeFrame, text="Plot extract data", value=6,
                            variable=self.num_mode).place(relx=0.1, rely=0.7)
        Tkinter.Radiobutton(self.modeFrame, text="Adiabatic Dumping(extract data)", value=7,
                            variable=self.num_mode).place(relx=0.1, rely=0.8)
        Tkinter.Radiobutton(self.modeFrame, text="Home", value=16,
                            variable=self.num_mode).place(relx=0.1, rely=0.9)        

        Tkinter.Radiobutton(self.modeFrame, text="Reflectance", value=9,
                            variable=self.num_mode).place(relx=0.6, rely=0.1)
        Tkinter.Radiobutton(self.modeFrame, text="BBA", value=10,
                            variable=self.num_mode).place(relx=0.6, rely=0.2)
        Tkinter.Radiobutton(self.modeFrame, text="None8", value=11,
                            variable=self.num_mode).place(relx=0.6, rely=0.3)
        Tkinter.Radiobutton(self.modeFrame, text="None9", value=12,
                            variable=self.num_mode).place(relx=0.6, rely=0.4)
        Tkinter.Radiobutton(self.modeFrame, text="None10", value=13,
                            variable=self.num_mode).place(relx=0.6, rely=0.5)
        Tkinter.Radiobutton(self.modeFrame, text="None11", value=14,
                            variable=self.num_mode).place(relx=0.6, rely=0.6)
        Tkinter.Radiobutton(self.modeFrame, text="None12", value=15,
                            variable=self.num_mode).place(relx=0.6, rely=0.7)
        Tkinter.Radiobutton(self.modeFrame, text="None13", value=8,
                            variable=self.num_mode).place(relx=0.6, rely=0.8)
        Tkinter.Radiobutton(self.modeFrame, text="Help", value=17,
                            variable=self.num_mode).place(relx=0.6, rely=0.9)
        

        

    def create_widgets(self):
        self.select = Tkinter.Button(self.lFrame, text="select")#, command=self.select)
        self.select.place(relx=0.7, rely=0.925)
        
        self.file_list = Tkinter.Listbox(self.lFrame ,selectmode='browse')
        self.reflesh()
        self.file_list.place(relx=0.1, rely=0.1,relheight=0.8,relwidth=0.8)

    def create_memobox(self):
        self.textField = Tkinter.Text(self.mFrame, relief="groove")
        #self.textField.pack(side='bottom',anchor=Tkinter.S)
        self.textField.place(relx=0.1, rely=0.1,relheight=0.6,relwidth=0.8)
        self.textField.insert('insert','-----------Log------------\n')

    def create_quit(self):
        self.quit = Tkinter.Button(self.mFrame, text="EXIT", command=self.master.destroy)
        self.quit.place(relx=0.8, rely=0.8)
        
    def reflesh(self,path=data_path):
        self.data_path = path +'/'
        self.file_list.delete(0,'end')
        files = os.listdir(path)
        self.file_list.insert(1, './')
        self.file_list.insert(2, '../')
        for i in range(len(files)):
            self.file_list.insert(i+3, '  '+files[i])
        #self.file_list.pack()
        
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

if __name__=="__main__":
    app = Design()
    app.mainloop()
