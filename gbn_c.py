import socket   #for sockets
import sys  #for exit
from check import ip_checksum

# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

host = 'localhost';
port = 8888;

windowSize = 4
base = 1
nextseqnum = 1

pktList = []
n = 1
pktList.append(0)
while(n < 11) :
    pktList.append(n)
    n = n + 1


old_msg = ''
resend = 0
count =0 
while(1) :
    if base == 10 :
        break
    elif nextseqnum < base + windowSize :
        msg = str(pktList[nextseqnum])
    try :

        s.settimeout(3)
        if msg == '2' :
            if count == 0:
                d = ip_checksum(msg+'1')
                msg_d = d + msg
                msg_seq_d = str(nextseqnum) + msg_d
                count = count + 1
            else:
                d = ip_checksum(msg)
                msg_d = d + msg
                msg_seq_d = str(nextseqnum) + msg_d
        else :
            d = ip_checksum(msg)
            msg_d = d + msg
            msg_seq_d = str(nextseqnum) + msg_d
       
        if nextseqnum < base + windowSize :
            print 'sending... PKT' + msg_seq_d[3:]
            s.sendto(msg_seq_d, (host, port))
            nextseqnum = nextseqnum + 1
        
        ''' if nextseqnum < base + windowSize :
            s.sendto(msg_seq_d, (host, port))
            nextseqnum = nextseqnum + 1
        '''
        try:
            data = s.recvfrom(1024)
            reply = data[0]
            addr = data[1]
        except :
            print 'time out!!!'
            nextseqnum = base
            continue

        if reply == str(base) :
            base = base + 1

    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()