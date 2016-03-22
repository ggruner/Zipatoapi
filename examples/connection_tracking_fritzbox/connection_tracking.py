#!/usr/bin/env python

# Autor: Gregor Gruener
# Project URL: https://github.com/ggruner/Zipatoapi
# Version: 0.3
# Changelog:
# 0.3
# - Bugfixes
# 0.2
# - Create automatically a virtual Endpoint
# 0.1
# - initial version
#
# Dependency: python-yaml, python-pycurl, python-requests, python-pycurl

'''
Desciption:
 This script checks which connection should be tracked,
 if the virtual Endpoint Sensor exists and update the state
 of the Sensor.
'''

from Zipatoapi import Zipatoapi
import yaml
import pycurl
import json

### my.zipato.com Login Credentials
login = ""
password = ""
###

### Do the authentification on my.zipato.com
a = Zipatoapi(login, password)
init = a.get_user_init()
hex_token = a.get_token(init['nonce'])
zipato_login = a.get_user_login(hex_token)


### Read the known_hosts File
with open("known_hosts.yaml", 'r') as kh_output:
    try:
        kh_data = yaml.safe_load(kh_output)
    except yaml.YAMLError as exc:
        print(exc)

### Read the connection_tracking File
with open("connection_tracking.yaml", 'r') as ct_output:
    try:
        ct_data = yaml.safe_load(ct_output)
    except yaml.YAMLError as exc:
        print(exc)


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
for section in kh_data:
    for lines in ct_data:
        # This is the check, if we like to track the mac
        if section['mac'] == lines['mac']:
            for virtual_endpoint in virtual_endpoints:
                ### Get the Sensor URL
                if lines['name'] == virtual_endpoint['name']:
                    config_data = a.get_virtual_endpoint(virtual_endpoint['uuid'])
                    url = config_data['attributeUrls'][0]['url']
                    # virtual Endpoint Sensor just understand true or false
                    if section['status'] == '1':
                        status = 'true'
                    else:
                        status = 'false'

                    # Send the new value to my.zipato.com
                    http = url + status
                    a.set_value_virtual_endpoint(http)
