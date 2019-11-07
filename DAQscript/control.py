import sys
ver_python = sys.version_info[0]
    
import socket
import select
import time

import datetime
import os
from struct import unpack
################################################################
#### RBCP Command                                           ####
####  sndHeader :                                           ####
####     type(RBCP_VER) + command(RBCP_CMD_) +              ####
####            id () +length() +address (int)              ####
################################################################
RBCP_VER = 255 #b'\xFF'
RBCP_CMD_WR = 128 #b'\x80'
RBCP_CMD_RD = 192#b'\xC0'
rbcpPort = 4660

def check(sock,id_num):
    sndHeader = [ RBCP_VER , RBCP_CMD_RD,id_num[0],38+2,
                 0,0,0,0]
    while True:
        sock.send(bytearray(sndHeader))
        a = select.select([sock],[],[],1)
        #print(a)
        if not a[0]:
            print( "*** Timeout! ***")
            sndHeader[2] += 1
            if (sndHeader[2] - id_num[0]) < 3:
                id_num[0] = sndHeader[2]        
                return
        else:
            break
    print("Succeess to conect!")
    id_num[0] = sndHeader[2] + 1
    recvData,ip_data = sock.recvfrom(2048)#'a'
    recvBytes = len(recvData) ## recv
    if ver_python == 2: recvData = [unpack('B',recvData[i])[0] for i in range(recvBytes)]
    #print(recvData)
    #print(recvBytes)
    if recvBytes < 30:
        print("ERROR: ACK packet is too short")
        return 
    if (0x0f & recvData[1]) != 0x8:
        print("ERROR: Detected bus error" )
        return
    #recvData[recvBytes] = 0
    offset = 8
    if int(recvData[offset+0]) == 0: print("MODE : process")
    elif int(recvData[offset+0]) == 2: print("MODE : wave")
    elif int(recvData[offset+0]) == 3: print("MODE : ready")
    # print(" GAIN")
    # for ch in range(16):
    #     print("\tpick up "+str(ch) +" : " +str(int(recvData[offset+2*ch+1])/128.+ int(recvData[offset+2*ch+2])/32768.) ) 
    print(" DATA # : " + str( int(recvData[offset+33])*65536 +
                             int(recvData[offset+34])*256 +
                             int(recvData[offset+35]) ))
    #print(" Delay_Clock : " + str(recvData[offset+39]))

    
    if(recvData[offset+0] == 2 or recvData[offset+0] == 1):
        if(recvData[offset+37] ==0): print(" sample memory is neither full nor empty.")
        elif(recvData[offset+37] == 1): print(" sample memory is full.")
        elif(recvData[offset+37] == 2): print(" sample memory is empty.")
    #print(" Tset Memory Status: " + str(recvData[offset+37]))
    return

def set_gain(sock,id_num,gain_value = [1.0 for i in range(16)]):
    for ch in range(16):
        sndHeader = [ RBCP_VER , RBCP_CMD_WR, id_num[0] + ch, 2,
                     0,0,0,ch*2+1,
                     (int(32768 * gain_value[ch])&0xFF00)>>8, int(32768 * gain_value[ch])&0xFF]
        sock.send(bytearray(sndHeader))
        sock.recvfrom(2048)#'a'
    id_num[0] += 16
    return 
def set_mode(sock,id_num,mode=3): ### mode={0:"process",2:"wave",3:"ready"]
    sndHeader = [ RBCP_VER , RBCP_CMD_WR, id_num[0], 1,
                 0,0,0,0,
                 0xFF & mode]
    sock.send(bytearray(sndHeader))
    sock.recvfrom(2048)#'a'
    id_num[0] += 1
    return

def set_data_number(sock,id_num,data_namber=0):
    sndHeader = [ RBCP_VER , RBCP_CMD_WR, id_num[0],3,
                 0,0,0,33,
                 (0x00FF0000 & data_namber)>>16, (0x0000FF00 & data_namber)>>8, 0x000000FF & data_namber]
    sock.send(bytearray(sndHeader))
    sock.recvfrom(2048)#'a'
    id_num[0] += 1
    return

def set_delay_clock(sock,id_num,delay_clock=0):
    sndHeader = [ RBCP_VER , RBCP_CMD_WR, id_num[0],1,
                 0,0,0,38,
                 0x3F & delay_clock]
    sock.send(bytearray(sndHeader))
    sock.recvfrom(2048)#'a'
    id_num[0] += 1
    return

def set_test_triger(sock,id_num):
    sndHeader = [ RBCP_VER , RBCP_CMD_WR, id_num[0],1,
                 0,0,0,37,
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

def reset_sitcp(sock,id_num):
    sndHeader = [ RBCP_VER , RBCP_CMD_WR, id_num[0],1,
                 0xFF,0xFF,0xFF,0x10,
                 0x80]
    sock.send(bytearray(sndHeader))    
    sock.recvfrom(2048)#'a'
    sndHeader[2] += 1
    sndHeader[8] = 0
    #time.sleep(1)
    sock.send(bytearray(sndHeader))
    sock.recvfrom(2048)#'a'
    id_num[0] = sndHeader[2] +1
    return

################################################################
#### TCP                                                    ####
####  Readout data                                          ####
################################################################
READING_BUF_SIZE = 2048
BUF_SIZE = 40
header_ex = [ b"TRANSVERSE MOMENTs measured with sixteen-pu-monitor at address 15",b'wave']
footer_ex = [ b"DATA processed with the 16-pu-monitor circuit",b'data']
if ver_python == 2:
   header_ex = [ "TRANSVERSE MOMENTs measured with sixteen-pu-monitor at address 15",'wave']
   footer_ex = [ "DATA processed with the 16-pu-monitor circuit",'data']
 
def receive_data(sock, header=header_ex[0], footer=footer_ex[0],datapath='./data/',
                 filename=None,flag=0):
    recvData = sock.recv(READING_BUF_SIZE)
    while True:
        if len(recvData) > BUF_SIZE:
            if header in recvData:
                dt_time = '{0:%Y_%m_%d_%H_%M_%S}'.format(datetime.datetime.now())
                #print("data start: "+ dt_time)
                if filename == None:
                    filename = datapath +'process_data/process_'+ dt_time + '.dat'
                    print(filename)
                fd = open(filename,'ab')
                if flag ==0 : fd.write(dt_time.encode())
                if footer in recvData:
                    index = recvData.find(footer)
                    fd.write(recvData[recvData.find(header):index+len(footer)])
                    fd.close()
                    return filename
                fd.write( recvData
                         [recvData.find(header):])
                recvData = recvData[len(recvData) - BUF_SIZE:]
                break
            recvData = recvData[len(recvData) - BUF_SIZE:]
        recvData += sock.recv(READING_BUF_SIZE)
    while True:
        recvData += sock.recv(READING_BUF_SIZE)
        if footer in recvData:
            index = recvData.find(footer)                    
            fd.write(recvData[BUF_SIZE:index+len(footer)])
            #print(recvData[index+len(footer):])
            break
        else: fd.write(recvData[BUF_SIZE:])
        recvData = recvData[len(recvData) - BUF_SIZE:]
    fd.close()
    #print('data stop')
    os.chmod(filename,0o777)
    return filename

def get_wave(sock,sockTCP,id_num,process_fname):
    sndHeader = [ RBCP_VER , RBCP_CMD_WR, id_num[0],1,
                 0,0,0,36,
                 0]
    fname = process_fname.replace('process','wave')
    print('Begining : get_wave')
    for ch in range(15):
        sndHeader[8] = ch
        sock.send(bytearray(sndHeader))
        #sock.send(bytearray(sndHeader))
        #sock.recvfrom(2048)#'a'
        if ch ==0:set_mode(sock,id_num,3)
        receive_data(sockTCP,header=header_ex[1], footer=footer_ex[1],flag=ch,filename=fname)
        #time.sleep(0.1)
        #time.sleep(0.08)
        sndHeader[3] += 1
    sndHeader[8] = 15
    sock.send(bytearray(sndHeader))
    receive_data(sockTCP,header=header_ex[1], footer=footer_ex[1],flag=ch,filename=fname)
    #sock.send(bytearray(sndHeader))
    sock.recvfrom(4096)#'a'
    #sock.recvfrom(2048)#'a'
    id_num[0] = sndHeader[3] +1
    print('END: get_wave')
    return

if __name__=="__main__": ### test
    ### UDP
    ipAddr ="10.72.108.43"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)
    sock.connect((ipAddr,rbcpPort))
    sock.settimeout(1)

    RBCP_ID = [1]

    #print("Command: Check, RBCP_ID : "+str(RBCP_ID[0]))
    #check(sock,RBCP_ID)

    #print("Command: Set_gain, RBCP_ID : "+str(RBCP_ID[0]))
    #gain = [0.1*ch for ch in range(16)]
    #set_gain(sock,RBCP_ID,gain)
    
    #print("Command: set_mode, RBCP_ID : "+str(RBCP_ID[0]))
    #set_mode(sock,RBCP_ID,0)

    #print("Command: Set_data_number, RBCP_ID : "+str(RBCP_ID[0]))
    #set_data_number(sock,RBCP_ID,0)

    #print("Command: Get_wave, RBCP_ID : "+str(RBCP_ID[0]))
    #get_wave(sock,RBCP_ID)
    #print("Command: Check, RBCP_ID : "+str(RBCP_ID[0]))
    #check(sock,RBCP_ID)
    #set_test_triger(sock,RBCP_ID)
    #set_delay_clock(sock,RBCP_ID,10)
    #check(sock,RBCP_ID)
    #sock.close()

    ### read out
    sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)
    ret_temp = sockTCP.getsockopt( socket.SOL_SOCKET, socket.SO_RCVBUF)
    print(ret_temp)
    option_value = 174760;
    sockTCP.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF,option_value)
    sockTCP.connect(("10.72.108.43",24))
    ret_temp = sockTCP.getsockopt( socket.SOL_SOCKET, socket.SO_RCVBUF)
    print(ret_temp)
    receive_data(sockTCP)
    get_wave2(sock,sockTCP,RBCP_ID)
    sock.close()
    sockTCP.close()
