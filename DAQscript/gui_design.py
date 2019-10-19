
import sys
ver_python = sys.version_info[0]
if ver_python == 2:import Tkinter
else : import tkinter as Tkinter

class Design(Tkinter.Frame,object):
    def __init__(self, master=Tkinter.Tk()):
        super(Design,self).__init__(master,width=600, height=450)
        self.master.title(u"DAQ of 16-electrodes monitor")
        self.pack()
        self.create_frame()
        self.create_widgets_sFrame()
        self.create_widgets_mFrame()
        
    def create_frame(self):
        self.sFrame = Tkinter.Frame(self.master)
        self.sFrame.place(relx=0, rely=0,relwidth=1,relheight=0.5)
        self.mFrame = Tkinter.Frame(self.master)
        self.mFrame.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

    def create_widgets_sFrame(self):        
        y = 0.1
        self.num_mode = Tkinter.IntVar()
        self.num_mode.set(3)
        Tkinter.Label(self.sFrame, text="Mode:").place(relx=0.1, rely=y)

        y += 0.2
        Tkinter.Radiobutton(self.sFrame, text="process", value=0,
                            variable=self.num_mode).place(relx=0.1, rely=y)
        Tkinter.Radiobutton(self.sFrame, text="wave", value=2,
                            variable=self.num_mode).place(relx=0.25, rely=y)
        Tkinter.Radiobutton(self.sFrame, text="ready", value=3,
                            variable=self.num_mode).place(relx=0.4, rely=y)

        y += 0.2
        Tkinter.Label(self.sFrame,text=u'Delay Clock').place(relx=0.1, rely=y)
        self.timing_Box = Tkinter.Entry(self.sFrame,width=8)
        self.timing_Box.insert(Tkinter.END,0)
        self.timing_Box.place(relx=0.3, rely=y)

        y += 0.2
        Tkinter.Label(self.sFrame,text=u'Shot Number').place(relx=0.1, rely=y)
        self.shot_number_Box = Tkinter.Entry(self.sFrame,width=8)
        self.shot_number_Box.insert(Tkinter.END,0)
        self.shot_number_Box.place(relx=0.3, rely=y)

        y = 0.7
        self.B_get_data = Tkinter.Button(self.sFrame,text='Get Data')
        self.B_get_data.place(relx=0.7, rely=y)

    def create_widgets_mFrame(self):
        self.mtextField = Tkinter.Text(self.mFrame, relief="groove")
        self.mtextField.place(relx=0.1, rely=0.1,relheight=0.6,relwidth=0.8)
        self.insert_log_format()
        Tkinter.Button(self.mFrame, text="EXIT", command=self.master.destroy).place(relx=0.8, rely=0.8)
    def insert_log_format(self):
        self.mtextField.delete('1.0','end')
        self.mtextField.insert('insert','Shot Number :\t\n')
        self.mtextField.insert('insert','Purpose     :\t\n')
        self.mtextField.insert('insert','Bunch       :\t\n')
        self.mtextField.insert('insert','p.p.b       :\t\n')
        self.mtextField.insert('insert','Atenuation  :\t\n')
        self.mtextField.insert('insert','Trigger time:\t\n')
        self.mtextField.insert('insert','Else        :\t\n')
if __name__=="__main__":
    app = Design()
    app.mainloop()
