
### UDP receive test ###

from socket import socket, AF_INET, SOCK_DGRAM
HOST = '127.0.0.1'
PORT = 4660

s = socket(AF_INET, SOCK_DGRAM)
s.bind((HOST, PORT))

while True:
    msg, address = s.recvfrom(8192)
    print(msg)
    print(address)

s.close()
    
