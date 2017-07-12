###############################################################
#
#   Synaccess Networks, Inc.  (www.synaccess-net.com)
#   July 11, 2017
#   By Al Lounsbury & SharkBytes Asscociates (Jon York)
#   for NP05 series. 
#   
################################################################

import socket
import time
import datetime
import sys
import smtplib

from email.message import EmailMessage

### Set Variables
global HOST, msg
HOST = str(sys.argv[1])			            # The remote host IP address
COMMAND_USER = str(sys.argv[2])                     # The command we wish to send
PORT = int(23)       				    # The server port number - telnet better than http
USER = str('admin')
PASS = str('Rain4Est!')
#   debugfile = 'E:\\PythonScripts\\pythonlog.txt'
debugfile = 'C:\\Users\\alounsbu\\My WebSites\\pythondev\\pythonlog.txt'

### Initialize email variables
msg = EmailMessage()
msg.set_content('No results yet')
msg['From'] = 'EBC Power Control <mdmail@ciena.com>'
msg['To'] = 'Al Lounsbury <alounsbu@ciena.com>'

### Open debug file
db = open( debugfile, "a")

### Define Functions

def Log_Write( message):
    global HOST
    db.write ( str(datetime.datetime.now()) )    # start log entry with date
    db.write (' ' + str(HOST) + ' ')            # log the host device IP address
    db.write ( ' ' + str(message) )
    db.write ( '\n\r')
    return

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
            Log_Write ("Command Failure.  Buffer = " + str(recv_status))
    return 

### Establish if command is on or off

if COMMAND_USER == 'ON':
    COMMAND = 'A7 1'
elif COMMAND_USER == 'OFF':
    COMMAND = 'A7 0'
else :
    Log_Write ("Invalid Operation defined, not ON or OFF")
    sys.exit()

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
    msg['Subject'] = 'Login Failure'
    Log_Write("Login Failure")
elif recv.endswith(b'$AF\x00'):
    msg.set_content('Failed to Connect.')            #Set message for email
    msg['Subject'] = 'Login Failure'
    Log_Write("Login Failure")
else:
    time.sleep(5)                                   #Sleep some more in case of slow communication
    m = Comm_Function(COMMAND)                      # need to fix - we cannot assume we can continue if here
    
### Close connection
	
time.sleep(0.5)
sock.close()

### Send Email
smtpObj = smtplib.SMTP('mdmail.ciena.com')
Log_Write (msg)

try:
    smtpObj.send_message(msg)
    smtpObj.quit()
    Log_Write ("Successfully sent email")
except SMTPException as exception:
    Log_Write ("Error: unable to send email")
	
db.close()      # close debug file
