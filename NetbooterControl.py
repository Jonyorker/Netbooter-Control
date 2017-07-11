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
import smtplib

from email.message import EmailMessage

### Set Variables
HOST = str(sys.argv[1])			            # The remote host IP address
COMMAND_USER = str(sys.argv[2])                     # The command we wish to send
PORT = int(23)       				    # The server port number - telnet better than http
USER = str('admin')
PASS = str('Rain4Est!')

### Initialize email variables
global msg
msg = EmailMessage()
msg.set_content('No results yet')
msg['From'] = 'mdmail@ciena.com'
msg['To'] = 'alounsbu@ciena.com'


### Establish if command if on or off

if COMMAND_USER == 'ON':
    COMMAND = 'A7 1'
elif COMMAND_USER == 'OFF':
    COMMAND = 'A7 0'
else :
    sys.exit()

### Define Function

def Comm_Function(COMMAND):
    global msg
    cmd = ('$'+COMMAND+'\r').encode('utf-8')
    sock.send(cmd)                                  #report status command
    time.sleep(1)                                   #Wait for command to complete
    recv_status = sock.recv(2048)                   #Receive output
    if recv_status.endswith(b'$A0'):
        msg.set_content('Operation Successful.')     #Set message for email
        msg['Subject'] = 'Operation Successful'
    elif recv_status.endswith(b'$A0\x00'):
        msg.set_content('Operation Successful.')     #Set message for email
        msg['Subject'] = 'Operation Successful'                                
    else:                                           #Try again in case delay wasn't enough
        time.sleep(5)                               #Wait for command to complete
        recv_status = sock.recv(2048)               #Receive output
        if recv_status.endswith(b'$A0'):
            msg.set_content('Operation Successful.') #Set message for email
            msg['Subject'] = 'Operation Successful'
        elif recv_status.endswith(b'$A0\x00'):
            msg.set_content('Operation Successful.')     #Set message for email
            msg['Subject'] = 'Operation Successful'   
        else:
            msg.set_content('Operation Failed.')     #Set message for email
            msg['Subject'] = 'Operation Failed'

    return 

### Establish Connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

time.sleep(0.5) 		                    #use time.sleep to give delay and netBooter time to process
	
sock.send(b'\r')				    #send \r to start at beginning of line
time.sleep(1)

cmd = ('$a1 '+USER+' '+PASS+'\r').encode('utf-8')
sock.send(cmd)		                            #login command
time.sleep(1)					    #delay between commands to allow NP unit to process

### Receive connection Confirmation and run comm function
recv = sock.recv(2048)                              #Receive output

if recv.endswith(b'$A0'):
    m = Comm_Function(COMMAND)
elif recv.endswith(b'$A0\x00'):
    m = Comm_Function(COMMAND)
elif recv.endswith(b'$AF'):
    msg.set_content('Failed to Connect.')            #Set message for email
    msg['Subject'] = 'Failed to Connect'                                               
else:
    time.sleep(5)                                   #Sleep some more in case of slow communication
    m = Comm_Function(COMMAND)
    
### Close connection
	
time.sleep(0.5)
	
sock.close()

### Send Email
smtpObj = smtplib.SMTP('mdmail.ciena.com')
print (msg)

try:
    smtpObj.send_message(msg)
    print ("Successfully sent email")
except SMTPException as exception:
    print ("Error: unable to send email")
	
