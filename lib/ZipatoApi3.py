# Author: Gregor Gruener
# Version: 0.2
# Rewritten in Python3
# Tested against Python3.5.3, 3.7.3

import requests
import json
import hashlib

class ZipatoApi3:
    "Zipato Api library"

    url = "https://my.zipato.com:443/zipato-web/v2/"

    def __init__(self, user, password):
        self.user = user
        self.password = password

    def get_user_init(self):
        """
        Description:
        (re)initialize the nonce of current session and fetch the session ID
        Return:
        {
         "success": true,
         "jsessionid": "3185591CD191F18D1551440AE1BEF86A-n1.frontend3",
         "nonce": "GTPSLZUcDyjEBqeL"
        }
        """
        uri = "user/init"
        api_url = self.url + uri
        s = requests.session()
        s = requests.get(api_url)
        d = json.loads(s.text)
        c = s.cookies

        return d['nonce'], c

    def get_user_login(self, token, cookie):
        """
        Description:
         login
        """
        self.token = token
        self.cookie = cookie

        uri = "user/login?username="+self.user+"&token="+self.token

        api_url = self.url + uri
        r = requests.get(api_url, cookies=self.cookie)

    def get_token(self, n):
        """
         Description:
          https://my.zipato.com/zipato-web/api/#!/user/login
          The whole process to get a valid token and to authenticate on zipato
        """
        self.n = n
        hash_password = hashlib.sha1(self.password.encode('utf-8'))
        hex_password = hash_password.hexdigest()

        combined = self.n + hex_password

        hash_token = hashlib.sha1(combined.encode('utf-8'))

        return hash_token.hexdigest()

    def get_virtual_endpoints(self, cookie):
        """
        Description:
         Get all virtual endpoints
        """
        self.cookie = cookie

        uri = "virtualEndpoints"

        api_url = self.url + uri
        r = requests.get(api_url, cookies=self.cookie)
        d = json.loads(r.text)

        return d
