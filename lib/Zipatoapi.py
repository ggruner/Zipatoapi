# Author: Gregor Gruener
# Version: 0.7.1

# Changelog:
# 0.7.1
# Fixed an issue in "put_attributes" method - Changed from POST to PUT
# 0.7
# - Added "put_attributes" method
# 0.6
# - Adjusted the get_virtual_endpoint method
# - Added "put_attributes_config" method
# 0.5
# - Added "synchronize" method
# 0.4
# - Added "set_value_virtual_endpoint" method
# - Added "save_and_synchronize" method
# 0.3
# - Added "get_virtual_endpoint" method
# 0.2
# - Added "get_virtual_endpoints_config" method
# 0.1
# - initial version

import pycurl
from io import BytesIO
import json
import hashlib

class Zipatoapi:
	"""zipato api library"""

	url = "https://my.zipato.com:443/zipato-web/v2/"

	def __init__(self, login, password):
		self.login = login
		self.password = password

	def get_user_init(self):
		'''
		Description:
		 (re)initialize the nonce of current session and fetch the session ID
		Return:
		 {
  			"success": true,
  			"jsessionid": "3185591CD191F18D1551440AE1BEF86A-n1.frontend3",
  			"nonce": "GTPSLZUcDyjEBqeL"
		 }
		'''
		uri = "user/init"
		api_url = self.url + uri
		c = pycurl.Curl()
		output_init = BytesIO()

		c.setopt(c.URL, api_url)
		### Create the cookie File
		c.setopt(pycurl.COOKIEJAR, 'cookie.txt')
		c.setopt(c.WRITEFUNCTION, output_init.write)
		c.perform()

		return json.loads(output_init.getvalue())

	def get_user_login(self, token):
		'''
		Description:
		 login
		'''
		self.token = token

		uri = "user/login?username="+self.login+"&token="+self.token

		api_url = self.url + uri
		c = pycurl.Curl()
		output = BytesIO()

		c.setopt(c.URL, api_url)
		### Read the cookie File
		c.setopt(pycurl.COOKIEFILE, 'cookie.txt')
		c.setopt(c.WRITEFUNCTION, output.write)
		c.perform()

		return json.loads(output.getvalue())

	def hash_string(self, string):
		'''
		Description:
		 https://my.zipato.com/zipato-web/api/#!/user/login
		 Create a sha1 hash string and return the sha1 string in hex
		'''
		self.hash_string = hashlib.sha1(string)

		return self.hash_string.hexdigest()

	def get_token(self, nonce):
		'''
		Description:
		 https://my.zipato.com/zipato-web/api/#!/user/login
		 The whole process to get a valid token and to authenticate on zipato
		'''
		self.nonce = nonce

		hash_password = hashlib.sha1(self.password)
		hex_password = hash_password.hexdigest()

		combined = self.nonce + hex_password

		hash_token = hashlib.sha1(combined)

		return hash_token.hexdigest()

	def get_all_virtual_endpoints(self):
		'''
		Description:
		 get all virtual endpoints
		'''
		uri = "virtualEndpoints"
		api_url = self.url + uri
		c = pycurl.Curl()
		output_init = BytesIO()

		c.setopt(c.URL, api_url)
		### Create the cookie File
		c.setopt(pycurl.COOKIEFILE, 'cookie.txt')
		c.setopt(c.WRITEFUNCTION, output_init.write)
		c.perform()

		return json.loads(output_init.getvalue())

	def create_virtual_endpoints(self, data, category):
		'''
		Description:
		 create a virtual endpoints
		 category:
		  SENSOR
		  METER
		  GAUGE
		  ONOFF
		  LEVEL_CONTROL
		'''
		self.data = data
		self.category = category

		uri = "virtualEndpoints/?category=" + self.category
		api_url = self.url + uri

		c = pycurl.Curl()
		c.setopt(pycurl.URL, api_url)
		c.setopt(pycurl.HTTPHEADER, ['Accept: application/json','Content-Type: application/json','charset=UTF-8'])
		c.setopt(pycurl.COOKIEFILE, 'cookie.txt')
		c.setopt(pycurl.POST, 1)
		c.setopt(pycurl.POSTFIELDS, self.data)
		c.setopt(pycurl.VERBOSE, 1)
		c.perform()

	def get_virtual_endpoints_config(self, uuid):
		'''
		Description:
		 get virtual endpoints config
		'''
		self.uuid = uuid

		uri = "virtualEndpoints/"+self.uuid+"/config"
		api_url = self.url + uri
		
		c = pycurl.Curl()
		output_init = BytesIO()

		c.setopt(c.URL, api_url)
		### Create the cookie File
		c.setopt(pycurl.COOKIEFILE, 'cookie.txt')
		c.setopt(c.WRITEFUNCTION, output_init.write)
		c.perform()

		return json.loads(output_init.getvalue())

	def get_virtual_endpoint(self, uuid, network="false", device="false", clusterEndpoints="false", config="false", icons="true",
		                     bindings="false", descriptor="false", room="false", info="false", full="false", attributes="false"):
		'''
		Description:
		 get virtual endpoint
		'''
		self.uuid = uuid

		uri = ("virtualEndpoints/"+self.uuid+"?network="+ network +"&device=" + device + "&clusterEndpoints=" + clusterEndpoints + "&config=" + config + "&icons=" + icons + 
		      "&type=false&bindings=" + bindings + "&descriptor=" + descriptor + "&room=" + room + "&info=" + info + "&full=" + full + "&attributes=" + attributes)
		api_url = self.url + uri
		c = pycurl.Curl()
		output_init = BytesIO()

		c.setopt(c.URL, api_url)
		### Create the cookie File
		c.setopt(pycurl.COOKIEFILE, 'cookie.txt')
		c.setopt(c.WRITEFUNCTION, output_init.write)
		c.perform()

		return json.loads(output_init.getvalue())

	def set_value_virtual_endpoint(self, http):
		'''
		Description:
		 This is just a simple Method to set a value on a virtual Endpoint URL
		'''
		self.http = http
		
		c = pycurl.Curl()
		c.setopt(pycurl.URL, self.http)
		c.perform()
		c.close()

	def create_rooms(self, data):
		'''
		Description:
		 create a room
		'''
		self.data = data
		
		uri = "rooms/"
		api_url = self.url + uri

		c = pycurl.Curl()
		c.setopt(pycurl.URL, api_url)
		c.setopt(pycurl.HTTPHEADER, ['Accept: application/json','Content-Type: application/json','charset=UTF-8'])
		c.setopt(pycurl.COOKIEFILE, 'cookie.txt')
		c.setopt(pycurl.POST, 1)
		c.setopt(pycurl.POSTFIELDS, self.data)
		c.setopt(pycurl.VERBOSE, 1)
		c.perform()

	def put_attributes_config(self, data, uuid):
		'''
		Description:
		 modify an attribute
		'''
		self.data = data
		self.uuid = uuid

		uri = "attributes/" + self.uuid + "/config"
		api_url = self.url + uri

		c = pycurl.Curl()
		c.setopt(pycurl.URL, api_url)
		c.setopt(pycurl.HTTPHEADER, ['Accept: application/json','Content-Type: application/json','charset=UTF-8'])
		c.setopt(pycurl.COOKIEFILE, 'cookie.txt')
		c.setopt(pycurl.POST, 1)
		c.setopt(pycurl.POSTFIELDS, self.data)
		c.setopt(pycurl.VERBOSE, 1)
		c.perform()

	def save_and_synchronize(self, wait="false", timeout=30):
		'''
		Description:
		 synchronize Zipato with the Server
		'''
		self.wait = wait
		self.timeout = timeout

		uri = "box/saveAndSynchronize?wait=" + self.wait + "&timeout=" + str(self.timeout)

		api_url = self.url + uri
		
		c = pycurl.Curl()
		output_init = BytesIO()

		c.setopt(c.URL, api_url)
		### Create the cookie File
		c.setopt(pycurl.COOKIEFILE, 'cookie.txt')
		c.setopt(c.WRITEFUNCTION, output_init.write)
		c.perform()
		c.close()

		return json.loads(output_init.getvalue())

	def synchronize(self, ifneeded="false", wait="false", timeout=30):
		'''
		Description:
		 synchronize Zipato with the Server
		'''
		self.ifneeded = ifneeded
		self.wait = wait
		self.timeout = timeout

		uri = "box/synchronize?ifNeeded=" + self.ifneeded + "wait=" + self.wait + "&timeout=" + str(self.timeout)

		api_url = self.url + uri
		
		c = pycurl.Curl()
		output_init = BytesIO()

		c.setopt(c.URL, api_url)
		### Create the cookie File
		c.setopt(pycurl.COOKIEFILE, 'cookie.txt')
		c.setopt(c.WRITEFUNCTION, output_init.write)
		c.perform()
		c.close()

		return json.loads(output_init.getvalue())
	
	def put_attributes(self, data, uuid):
		'''
		Description:
		 set attribute value with application/json content
		'''
		self.data = data
		self.uuid = uuid

		uri = "attributes/" + self.uuid + "/value"
		api_url = self.url + uri

		c = pycurl.Curl()
		c.setopt(pycurl.URL, api_url)
		c.setopt(pycurl.HTTPHEADER, ['Accept: application/json','Content-Type: application/json','charset=UTF-8'])
		c.setopt(pycurl.COOKIEFILE, 'cookie.txt')
		c.setopt(pycurl.CUSTOMREQUEST, "PUT")
		c.setopt(pycurl.POSTFIELDS, self.data)
		c.setopt(pycurl.VERBOSE, 1)
		c.perform()
