import json
import telnetlib

with open('config.json') as config:
    data = json.load(config)

print (data['PS1']['ip'])
