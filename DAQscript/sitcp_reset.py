
import socket
import sys
import sys
ver_python = sys.version_info[0]
if ver_python == 2:import Tkinter
else : import tkinter as Tkinter

import time

ipAddr ="10.72.108.43"
RBCP_VER = 255 #b'\xFF'
RBCP_CMD_WR = 128 #b'\x80'
RBCP_CMD_RD = 192#b'\xC0'
rbcpPort = 4660

def set_test_triger0(sock,id_num,offset=0):
    sndHeader = [ RBCP_VER , RBCP_CMD_WR, id_num[0],1,
                 0,0,0,37+offset,
                 1]
    sock.send(bytearray(sndHeader))    
    sock.recvfrom(2048)#'a'
    sndHeader[2] += 1
    sndHeader[8] = 0
    #time.sleep(1)
    sock.send(bytearray(sndHeader))
    sock.recvfrom(2048)#'a'
    id_num[0] = sndHeader[2] +1
    return

def set_test_triger(sock,id_num,offset=0):
    sndHeader = [ RBCP_VER , RBCP_CMD_WR, id_num[0],1,
                 0,0,0,37+offset,
                 1]
    sock.send(bytearray(sndHeader))    
    sock.recvfrom(2048)#'a'
    id_num[0] = sndHeader[2] +1
    return

def reset_sitcp(sock,id_num,offset=0):
    sndHeader = [ RBCP_VER , RBCP_CMD_WR, id_num[0],1,
                 0xFF,0xFF,0xFF,0x10,
                 0x80]
    sock.send(bytearray(sndHeader))    
    sock.recvfrom(2048)#'a'
    id_num[0] = sndHeader[2] +1
    return

def trigger():
    rbcpPort = 4660
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)
    sock.connect((ipAddr,rbcpPort))
    sock.settimeout(1)
    RBCP_ID = [1]
    set_test_triger(sock,RBCP_ID)
    print('trigger')
    sock.close()
    
def reset():
    rbcpPort = 4660
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)
    sock.connect((ipAddr,rbcpPort))
    sock.settimeout(1)
    RBCP_ID = [1]
    reset_sitcp(sock,RBCP_ID,1)
    print('reset')
    sock.close()


if __name__=="__main__": ### test
    root = Tkinter.Tk()
    root.title('test trigger')
  
    root.geometry('200x200')
    btn = Tkinter.Button(root, text='Trigger', command=trigger)
    btn.pack()
    btn = Tkinter.Button(root, text='Reset',command=reset)
    btn.pack()

    btn = Tkinter.Button(root, text='Exit',command=root.quit)
    btn.pack()
    root.mainloop()
