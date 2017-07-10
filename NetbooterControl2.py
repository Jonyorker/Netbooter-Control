###############################################################
#
#   Synaccess Networks, Inc.  (www.synaccess-net.com)
#   Jan. 6th, 2013
#   Python Script Example 1  
#   for NP series. 
#   
################################################################

import socket 
import time 									
import sys 

### Set Variables
HOST = str(sys.argv[1])			        # The remote host IP address
COMMAND = str(sys.argv[2])                      # The command we wish to send
PORT = int(23)       				# The server port number - telnet better than http
USER = str('admin')
PASS = str('Rain4Est!')

### Establish Connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

time.sleep(0.1) 		                #use time.sleep to give delay and netBooter time to process
	
sock.send(b'\r')				#send \r to start at beginning of line
time.sleep(0.5)

cmd = ('$a1 '+USER+' '+PASS+'\r').encode('utf-8')
sock.send(cmd)		                        #login command
time.sleep(0.5)					#delay between commands to allow NP unit to process

### Receive connection Confirmation
recv = sock.recv(2048)                          #Receive output

if recv.endswith(b'$A0'):
    cmd = ('$'+COMMAND+'\r').encode('utf-8')
    sock.send(cmd)                             #report status command
    recv_status = sock.recv(2048)                          #Receive output
    if recv_status.endswith(b'11111'):
        print ('All 5 outlets are on')
    else:
        print ('Some outlets are off')
else:
    print ('failed to connect')
    
##sock.send(b'$A5\r')                             #report status command
##time.sleep(0.5)
##
##recv = sock.recv(2048)                         #See what we retrieve here
##print(recv1)                                    #print data received
##
##sock.send(b'A2\r')				#send logout command to unit to gracefully close socket connection
##	
##recv2 = sock.recv(2048)				#receive data from session
##print(recv2)					#print data received
	
time.sleep(0.1)
	
sock.close()
	
