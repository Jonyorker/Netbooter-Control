import json
import telnetlib

with open('config.json') as config:
    data = json.load(config)

HOST = data['PS1']['ip']
USER = data['PS1']['username']
PASSWORD = data['PS1']['password']

tn = telnetlib.Telnet(HOST)

tn.read_until("login: ")
tn.write(USER + "\n")
if PASSWORD:
    tn.read_until("Password: ")
    tn.write(PASSWORD + "\n")

tn.write("pshow")
tn.write("exit\n")

print (tn.read_all())
