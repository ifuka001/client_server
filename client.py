'''
    udp socket client
    Silver Moon
'''
 
import socket   #for sockets
import sys  #for exit
import select
# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
 
host = 'localhost';
port = 8888;
 
while(1) :
    msg = raw_input('Enter message to send : ')
     
    try :
        #Set the whole string
        if msg[1:] != 'pkt2':
            s.sendto(msg, (host, port))
        else:
            msg_broken = msg + 'broken'
            s.sendto(msg_broken, (host,port))
        
        
        # receive data from client (data, addr)
        #d = s.recvfrom(1024)
        #reply = d[0]
        #addr = d[1]
        while(1):
            inputs = [s]
            outputs = []
            timeout = 3
            cond = False
            
            readable,writable,exceptional = select.select(inputs,outputs,inputs,timeout)
            for tempSocket in readable:
                temp = tempSocket.recvfrom(1024)
                reply = temp[0]
                addr = temp[1]
                print 'Server reply : ' + reply
                cond = True
            
            if cond != True :
                print 'Did not receive ack so resending packet'
                s.sendto(msg, (host, port))
            else:
                break
            
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()