
### process only

import sys
import datetime
import socket
#import numpy as np
import time
import control

import os

class Application(object):
    def __init__(self, ipAddr="10.72.108.43",#"127.0.0.1",
                 address_num=13,
                 rbcpPort=4660,
                 tcpPort=24,
                 gain_file='./DAQscript/gain/gain_test.txt', ## all 1.0
                 ofile ='/jkdata/jkpublic/accbmon/mrbmon/16pu_data/',
                 shot_num = 2,
                 bunch_num=100):
    
        #self.ofile = ofile + str(address_num) + '/' + '{0:%Y%m%d/}'.format(datetime.datetime.now())
        self.ofile = ofile  + '{0:%Y%m%d/}'.format(datetime.datetime.now())
        self.address = address_num
        if not os.path.exists(self.ofile):
            os.mkdir(self.ofile)
            os.mkdir(self.ofile+'wave_data')
            os.mkdir(self.ofile+'process_data')
            os.mkdir(self.ofile+'log')
        self.RBCP_ID = [1]
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)
        self.sock.connect((ipAddr,rbcpPort))
        
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

        control.set_mode(self.sock,self.RBCP_ID,3)
        control.check(self.sock,self.RBCP_ID)
        self._get_data(shot_num=shot_num,bunch_num=bunch_num)

    def _print_time(self):
        print("\nRBCP_ID : "+str(self.RBCP_ID))
        dt_now =  '{0:%Y_%m_%d_%H_%M_%S}'.format(datetime.datetime.now()) 
        print('Now time:  '+dt_now )
        

    def _get_data(self,shot_num,bunch_num):
        num_mode = 0
        control.set_data_number(self.sock,self.RBCP_ID,bunch_num)
        flist = []
        for i in range(shot_num):
            print("Beginning : Get_Data")
            control.set_mode(self.sock,self.RBCP_ID,0)        
            fname = control.receive_data(self.sockTCP,datapath=self.ofile,address=self.address)
            flist.append(fname)
            print("Save: "+str(i+1)+'/'+str(shot_num)+'data')
        control.set_mode(self.sock,self.RBCP_ID,3)        
        control.check(self.sock,self.RBCP_ID)

        
if __name__=="__main__":
    hostname = '%s' % socket.gethostname()
    print("HOST NAME: " + hostname)
    if hostname == 'sioc-mon-d1hexadeca01.mr.jkcont':
        print("Begin DAQ script for # 13")
        app = Application(ipAddr="10.72.108.43",address_num=13)
        app.sock.close()

    elif hostname == 'sioc-mon-d1hexadeca02.mr.jkcont':
        print("Begin DAQ script for # 15")
        app = Application(ipAddr="10.72.108.43",address_num=15)
        app.sock.close()

    else:
        print("Begin DAQ script for test-bench")
        app = Application(address_num=0)
        app.sock.close()
        

