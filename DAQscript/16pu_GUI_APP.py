
import sys
import datetime
import socket
#import numpy as np
import time
import gui_design
import control

import os

class Application(gui_design.Design,object):
    def __init__(self, ipAddr="10.72.108.43",#"127.0.0.1",
                 address_num=13,
                 rbcpPort=4660,
                 tcpPort=24,
                 gain_file='./DAQscript/gain/gain_test.txt',
                 ofile ='/jkdata/jkpublic/accbmon/mrbmon/16pu_data/16pu_address'):

        self.ofile = ofile + str(address_num) + '/' + '{0:%Y%m%d/}'.format(datetime.datetime.now())
        
        if not os.path.exists(self.ofile):
            os.mkdir(self.ofile)
            os.mkdir(self.ofile+'wave_data')
            os.mkdir(self.ofile+'process_data')
            os.mkdir(self.ofile+'log')
        self.RBCP_ID = [1]
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)
        self.sock.connect((ipAddr,rbcpPort))
        
        control.reset_sitcp(self.sock,self.RBCP_ID) 

        super(Application,self).__init__()
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

        control.set_gain(self.sock,self.RBCP_ID)# ,np.loadtxt(gain_file,delimiter=', ')) not import numpy as np ### default all 1
        
        self._setting()
        control.check(self.sock,self.RBCP_ID)

    def _print_time(self):
        print("\nRBCP_ID : "+str(self.RBCP_ID))
        dt_now =  '{0:%Y_%m_%d_%H_%M_%S}'.format(datetime.datetime.now()) 
        print('Now time:  '+dt_now )
        
    def _setting(self):
        control.set_mode(self.sock,self.RBCP_ID,self.num_mode.get())        
        # control.set_delay_clock(self.sock,self.RBCP_ID,
        #                         int(self.bunch_num_Box.get()))
        control.set_data_number(self.sock,self.RBCP_ID,
                                int(self.bunch_num_Box.get())) ## for processing
        self._print_time()

    def _get_data(self):
        shot_num = int(self.shot_number_Box.get())
        num_mode = int(self.num_mode.get())
        control.set_data_number(self.sock,self.RBCP_ID,
                                int(self.bunch_num_Box.get())) ## for processing
        flist = []
        for i in range(shot_num):
            print("Beginning : Get_Data")
            if num_mode == 0:
                control.set_mode(self.sock,self.RBCP_ID,0)        
                fname = control.receive_data(self.sockTCP,datapath=self.ofile)
                flist.append(fname)
            elif num_mode == 2:
                control.set_mode(self.sock,self.RBCP_ID,2)        
                fname = control.receive_data(self.sockTCP,datapath=self.ofile)
                control.get_wave(self.sock,self.sockTCP,self.RBCP_ID,process_fname=fname)
                flist.append(fname)
                time.sleep(1.5)
            print("Save: "+str(i+1)+'/'+str(shot_num)+'data')
        self._write_log(flist)
        control.set_mode(self.sock,self.RBCP_ID,3)        
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
    hostname = '%s' % socket.gethostname()
    print("HOST NAME: " + hostname)
    if hostname == 'sioc-mon-d1hexadeca01.mr.jkcont':
        print("Begin DAQ script for # 13")
        app = Application(address_num=13)
        app.mainloop()
        app.sock.close()

    elif hostname == 'sioc-mon-d1hexadeca02.mr.jkcont':
        print("Begin DAQ script for # 15")
        app = Application(address_num=15)
        app.mainloop()
        app.sock.close()

    else:
        print("Begin DAQ script for test-bench")
        app = Application(address_num=0)
        app.mainloop()
        app.sock.close()
        

