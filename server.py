'''
    Simple udp socket server
    Silver Moon (m00n.silv3r@gmail.com)
'''
 
import socket
import sys
import select
 
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
    timeout = 3
    readable,writable,exceptional = select.select(inputs,outputs,inputs,timeout)
    for tempSocket in readable:
        temp = tempSocket.recvfrom(1024)
        reply = temp[0]
        addr = temp[1]
        
        if not reply:
            break
        if reply[1:] == 'pkt2broken':
            print 'packet lost'
        else:
            data = 'Sending ACK' + reply[0:1]
            s.sendto(data,addr)
            
   


    #s.sendto(reply , addr)
     
s.close()