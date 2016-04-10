#!/usr/bin/env python

# Autor: Gregor Gruener
# Project URL: https://github.com/ggruner/Zipatoapi
# Version: 0.1
# Changelog:
# 0.1
# - initial version
#
# Dependency: python-yaml, python-pycurl, python-requests, python-nmap

'''
Desciption:
 This script checks which connection should be tracked,
 receive all mac addresses from the network, create the sensors on zipato
 and update the Status of the sensor if a device is offline / online
'''

from Zipatoapi import Zipatoapi
import yaml
import pycurl
import json
import nmap

### my.zipato.com Login Credentials
login = ""
password = ""
###

### Set your IP Range here
cidr2 = '192.168.178.1/24'
###

### Do the authentification on my.zipato.com
a = Zipatoapi(login, password)
init = a.get_user_init()
hex_token = a.get_token(init['nonce'])
zipato_login = a.get_user_login(hex_token)

### Create the nmap instance and do the network scan
nm = nmap.PortScanner()
result = nm.scan(hosts=cidr2, arguments='-F --host-timeout 5s')

### Read the connection_tracking File
with open("connection_tracking.yaml", 'r') as ct_output:
    try:
        ct_data = yaml.safe_load(ct_output)
    except yaml.YAMLError as exc:
        print exc


### Check if all tracked User has a virtual Endpoint
created_virtual_endpoint = 0
virtual_endpoints = a.get_all_virtual_endpoints()

for line in ct_data:
    account_exist = 0
    for virtual_endpoint in virtual_endpoints:
        if line['name'] == virtual_endpoint['name']:
            account_exist += 1 
        
    if account_exist == 0:
        data = {}
        data['name'] = line['name']
        data['category'] = 'SENSOR'
        json_data = json.dumps(data)
        a.create_virtual_endpoints(json_data, "SENSOR")
        created_virtual_endpoint = 1

### Receive the new virtual Endpoints list
if created_virtual_endpoint == 1:
    a.synchronize()
    virtual_endpoints = a.get_all_virtual_endpoints()

### Get all relevant informations to set the value
for lines in ct_data:
    online = 0
    for ipv4, info in result['scan'].items():
        if info['status']['state'] != 'up':
                continue

        mac = info['addresses'].get('mac')
        if mac is None:
                continue

        # This is the check, if we like to track the mac
        if mac == lines['mac']:
            online = 1
                
    for virtual_endpoint in virtual_endpoints:
        ### Get the Sensor URL
        if lines['name'] == virtual_endpoint['name']:
            config_data = a.get_virtual_endpoint(virtual_endpoint['uuid'])
            url = config_data['attributeUrls'][0]['url']
            # virtual Endpoint Sensor just understand true or false
            if online == 1:
                status = 'true'

            else:
                status = 'false'

            # Send the new value to my.zipato.com
            http = url + status
            a.set_value_virtual_endpoint(http)
