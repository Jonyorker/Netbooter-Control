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
HOST = str(sys.argv[1])			            # The remote host IP address
COMMAND_USER = str(sys.argv[2])                     # The command we wish to send
PORT = int(23)       				    # The server port number - telnet better than http
USER = str('admin')
PASS = str('Rain4Est!')

### Establish if command if on or off

if COMMAND_USER == 'ON':
    COMMAND = 'A7 1'
elif COMMAND_USER == 'OFF':
    COMMAND = 'A7 0'

### Establish Connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

time.sleep(0.1) 		                    #use time.sleep to give delay and netBooter time to process
	
sock.send(b'\r')				    #send \r to start at beginning of line
time.sleep(0.5)

cmd = ('$a1 '+USER+' '+PASS+'\r').encode('utf-8')
sock.send(cmd)		                            #login command
time.sleep(0.5)					    #delay between commands to allow NP unit to process

### Receive connection Confirmation and run command
recv = sock.recv(2048)                              #Receive output

if recv.endswith(b'$A0'):
    cmd = ('$'+COMMAND+'\r').encode('utf-8')
    sock.send(cmd)                                  #report status command
    time.sleep(1)                                   #Wait for command to complete
    recv_status = sock.recv(2048)                   #Receive output
    if recv_status.endswith(b'$A0'):
        print ('Operation Successful')
    else:                                           #Try again in case delay wasn't enough
        time.sleep(5)                               #Wait for command to complete
        recv_status = sock.recv(2048)               #Receive output
        if recv_status.endswith(b'$A0'):
            print ('Operation Successful')
        else:
            print ('Operation Failed')
else:
    print ('Failed to Connect')
    
### Close connection
	
time.sleep(0.1)
	
sock.close()
	
