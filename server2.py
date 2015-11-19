 
import socket
import sys
import select
from check import ip_checksum
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
 
 
# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#now keep talking with the client
while 1:
    inputs = [s]
    outputs = []
    timeout = 5
    readable,writable,exceptional = select.select(inputs,outputs,inputs,timeout)
    for tempSocket in readable:
        temp = tempSocket.recvfrom(1024)
        reply = temp[0]
        addr = temp[1]
        
        ack = reply[0:1]
        msg_sum = reply[1:2]
        msg = reply[3:len(reply)]
        msg_chksum = ip_checksum(msg)
        
        if msg_sum == msg_chksum:
            message = 'received ack ' + reply[0:1]
            s.sendto(message, (HOST, PORT))
        else :
            print 'packet corrupted'
        

            
   


    #s.sendto(reply , addr)
     
s.close()