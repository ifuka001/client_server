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

windowSize = 5
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
repack = []
while(1) :
    if nextseqnum > 9 :
        break
    msg = str(pktList[nextseqnum])
    try :

        s.settimeout(2)
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
            #base = base + 1
        
        try:
            data = s.recvfrom(1024)
            reply = data[0]
            addr = data[1]
            if int(reply) == 999:
                repack.append(nextseqnum)
        except :
            print 'time out!!!'
            for a in repack:
                msg = str(pktList[a-1])
                d = ip_checksum(msg)
                msg_d = d + msg
                msg_seq_d = str(a-1)+msg_d
                print 'resending... PKT' + msg_seq_d[3:]
                s.sendto(msg_seq_d, (host,port))
            del repack[:]
            base = nextseqnum
            continue


    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()