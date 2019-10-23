
import datetime
import socket
import numpy as np
import time
import DAQscript.control as control
import DAQscript.gui_design as gui_design
import os
import sys

class Application(gui_design.Design,object):
    def __init__(self, ipAddr="10.72.108.43",#"127.0.0.1",
                 address_num=13,
                 rbcpPort=4660,
                 tcpPort=24,
                 gain_file='./DAQscript/gain/gain_test.txt',
                 ofile ='./data/'):
        self.ofile = ofile + '{0:%Y%m%d/}'.format(datetime.datetime.now())
        if not os.path.exists(self.ofile):
            os.mkdir(self.ofile)
            os.mkdir(self.ofile+'wave_data')
            os.mkdir(self.ofile+'process_data')
            os.mkdir(self.ofile+'log')
        self.RBCP_ID = [1]
        self.turn_number = 20
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)
        self.sock.connect((ipAddr,rbcpPort))
        ### test
        control.reset_sitcp(self.sock,self.RBCP_ID) 
        super().__init__()
        self.B_get_data.configure(command = self._get_data)
        self._print_time()
        
        ### comment out when offline
        self.sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)
        ret_temp = self.sockTCP.getsockopt( socket.SOL_SOCKET, socket.SO_RCVBUF)
        print(ret_temp)
        self.sockTCP.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF,174760)
        self.sockTCP.connect((ipAddr,tcpPort))
        ret_temp = self.sockTCP.getsockopt( socket.SOL_SOCKET, socket.SO_RCVBUF)
        print(ret_temp)

        control.set_gain(self.sock,self.RBCP_ID,np.loadtxt(gain_file,delimiter=', '))
        control.set_data_number(self.sock,self.RBCP_ID,self.turn_number) ## for processing
        self._setting()
        control.check(self.sock,self.RBCP_ID)

    def _print_time(self):
        print("\nRBCP_ID : "+str(self.RBCP_ID))
        dt_now =  '{0:%Y_%m_%d_%H_%M_%S}'.format(datetime.datetime.now()) 
        print('Now time:  '+dt_now )
        
    def _setting(self):
        control.set_mode(self.sock,self.RBCP_ID,self.num_mode.get())        
        control.set_delay_clock(self.sock,self.RBCP_ID,
                                int(self.timing_Box.get()))
        self._print_time()
    def _get_data(self):
        shot_num = int(self.shot_number_Box.get())
        num_mode = int(self.num_mode.get())
        flist = []
        self._setting()
        for i in range(shot_num):
            print("Beginning : Get_Data")
            if num_mode == 0:
                fname = control.receive_data(self.sockTCP,datapath=self.ofile)
                self._print_time()
                print("Save: "+str(i)+'/'+str(shot_num+1)+'data')
                flist.append(fname)
            elif num_mode == 2:
                fname = control.receive_data(self.sockTCP,datapath=self.ofile)
                control.get_wave(self.sock,self.sockTCP,self.RBCP_ID,process_fname=fname)
                self._print_time()                
                print("Save: "+str(i)+'/'+str(shot_num+1)+'data')
                flist.append(fname)
        self._write_log(flist)
        control.check(self.sock,self.RBCP_ID)

    def _write_log(self,flist):
        log = self.mtextField.get('1.0','end')
        for i in range(len(flist)):
            fname = flist[i].replace('process_data/','log/')
            fname = fname.replace('process_','log_')
            fname = fname.replace('.dat','.txt')
            fout = open(fname,'w')
            fout.write(log)
            fout.close()
        self.insert_log_format()
        
if __name__=="__main__":
    args = sys.argv
    if len(args) < 2:
        print("ERROR : use \"python 16pu_GUI_APP.py 13or15\"")
        sys.exit()
    address_num = int(args[1])
    if address_num == 13:
        print("Begin DAQ script for # 13")    
    elif address_num == 15:
        print("Begin DAQ script for # 13")
    else:
        print("ERROR : use \"python 16pu_GUI_APP.py 13or15\"")
        sys.exit()

    app = Application(address_num)
    app.mainloop()
    app.sock.close()
