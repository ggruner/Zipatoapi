#!/usr/bin/env python3
# Author: Gregor Gruener
# 
# This script push the Hue Temperature data
# to your Zipato device as a virtual Endpoint

from ZipatoApi3 import ZipatoApi3
import requests
import json

# Zipato Login
user = ""
password = ""
# Hue_API Credential
hue_api = ""

# Do the Authenticatio
a = ZipatoApi3(user, password)
nonce, cookie = a.get_user_init()
hex_token = a.get_token(nonce)
a.get_user_login(hex_token, cookie)

# Save all virtual endpoints
endpoints = a.get_virtual_endpoints(cookie)

# Save hue data
r = requests.get(hue_api)
data = json.loads(r.text)

for k, v in data['sensors'].items():
    try:
        # Get the Hue Temperature Name and the value
        if "temperature" in v['productname']:
            temp = v['state']['temperature'] / 100
            uniq_id = v['uniqueid'].split("-").pop(0)
            for k,v in data['sensors'].items():
                try:
                    if uniq_id in v['uniqueid'] and "Hue motion sensor" in v['productname']:
                        name = v['name']
                        # Check if endpoint already exist
                        found = 0
                        for endpoint in endpoints:
                            if name in endpoint['name']:
                                found = 1
                                uuid = endpoint['uuid']
                                break
                            else:
                                found =0
                                continue

                        if found == 1:
                            config = a.get_virtual_endpoints_uuid(cookie, uuid)
                            for attr_url in config['attributeUrls']:
                                if "value1" == attr_url['attribute']:
                                    url = attr_url['url']
                                    set_url = url + str(temp)
                                    # Set the new Value for the endpoint
                                    requests.get(set_url, cookies=cookie)

                        else:
                            # Create virtual Endpoint
                            a.post_virtual_endpoints(cookie, "GAUGE", name)
                            a.get_save_and_synchronize(cookie)
                except:
                    pass
    except:
        pass

# Logout the user from Zipato
a.get_user_logout(cookie)
