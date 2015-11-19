import socket   #for sockets
import sys  #for exit
import select
from check import ip_checksum
# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
 
host = 'localhost';
port = 8888;

w_size = 4
nextseqnum = 0
base = 0
myPkt = []
n=1

while(n<7):
    myPkt.append(n)
    n = n+1



while(1) :
    msg = raw_input('Enter message to send : ')
    try :
        
        
        
        
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()