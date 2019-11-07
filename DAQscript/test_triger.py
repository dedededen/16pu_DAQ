
import socket
import sys
import sys
ver_python = sys.version_info[0]
if ver_python == 2:import Tkinter
else : import tkinter as Tkinter

import control
import time

def trigger():
    ipAddr ="10.72.108.43"
    rbcpPort = 4660
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)
    sock.connect((ipAddr,rbcpPort))
    sock.settimeout(1)
    RBCP_ID = [1]
    control.set_test_triger(sock,RBCP_ID)
    print('trigger')
    sock.close()

if __name__=="__main__": ### test
    root = Tkinter.Tk()
    root.title('test trigger')
  
    root.geometry('200x60')
    btn = Tkinter.Button(root, text='Trigger', command=trigger)
    btn.pack()
    btn = Tkinter.Button(root, text='Exit',command=root.quit)
    btn.pack()
    root.mainloop()
