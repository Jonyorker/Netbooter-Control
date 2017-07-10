import requests
from requests.auth import HTTPBasicAuth

HOST = str("10.177.96.26") 
USER = str("admin")
PASSWORD = str("Rain4Est!")

r = requests.get('http://'+HOST+'/cmd.cgi?$A1', auth=('USER', 'PASSWORD'))

print(r.url)
print(r.content)
print(r.text)
print(r.json)
print(r.status_code)
print(r.raw)

r2 = requests.get('http://'+HOST+'/cmd.cgi?$A5', auth=('USER', 'PASSWORD'))

print(r2.url)
print(r2.content)
print(r2.text)
print(r2.json)
print(r2.status_code)
print(r2.raw)
