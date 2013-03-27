#!/usr/bin/env python
# encoding: utf-8
"""
client.py

Created by Francisco Gray <frgray@uoregon.edu> on 2012-11-01.
Copyright (c) 2012 University of Oregon. All rights reserved.
DISCLAIMER OF WARRANTY

BECAUSE THIS SOFTWARE IS LICENSED FREE OF CHARGE, THERE IS NO WARRANTY
FOR THE SOFTWARE, TO THE EXTENT PERMITTED BY APPLICABLE LAW. EXCEPT WHEN
OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES
PROVIDE THE SOFTWARE "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER
EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE
ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE SOFTWARE IS WITH
YOU. SHOULD THE SOFTWARE PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL
NECESSARY SERVICING, REPAIR, OR CORRECTION.

IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR
REDISTRIBUTE THE SOFTWARE AS PERMITTED BY THE ABOVE LICENCE, BE
LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL,
OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE
THE SOFTWARE (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING
RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A
FAILURE OF THE SOFTWARE TO OPERATE WITH ANY OTHER SOFTWARE), EVEN IF
SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES.
"""

import os, sys, re
import requests

#my_config = {'verbose':sys.stderr} # Request Debugging

__version__ = '0.01' ## Not always updated

class client(object):
	def __init__(self, username, password, server, debug):
		"""__init__():
				Usage:
					uname = 'my_user'
					pword = 'my_pass'
					server = "https://netdot.localdomain/netdot"
					import netdot
					dot = netdot.client(uname,pword,server)
			
				Description: 
					Class constructor, instantiates a number of 
				variables for use in the class.  Mainly the required
				NetDot HTTP headers and login form parameters.
			
				Returns: 
					NetDot.client object.
		"""
		if debug == 1:
			self.debug = True
		if username and password and server:
			self.user = username
			self.pw = password
			self.base_url = server + '/rest'
			self.login_url = server + '/NetdotLogin'
			self.timeout = 10
			self.retries = 3
			self.version = __version__
			self.headers = {
					'User_Agent':'Netdot::Client::REST/self.version',
					'Accept':'text/xml; version=1.0'
					}
			self.params = {
					'destination':'index.html', 
					'credential_0':self.user, 
					'credential_1':self.pw, 
					'permanent_session':1
					}
			# Call the _login() function 		
			self._login()
		else:
			raise AttributeError('Username, Password and Server are REQUIRED')
		
	def _login(self):
		"""_login():
				Description: 
					Internal Function. Logs into the NetDot API with provided credentials, 
				stores the Apache generated cookies into the self object to be 
				reused.  
		"""
		response = requests.post(self.login_url, data=self.params, headers=self.headers)
		if response.status_code == 200:
			self.auth_cookies = response.cookies
		else:
			raise AttributeError('Invalid Credentials')

	def get(self, url):
		"""get():
				Usage:
					response = netdot.client.get("/url")
			
				Description: 
					This function provides a simple interface
				into the "GET" function by handling the authentication
				cookies as well as the required headers and base_url for 
				each request.  
			
				Returns: 
					Result as a multi-level dictionary on sucess. 
		"""
		response = requests.get(self.base_url + url, cookies=self.auth_cookies, headers=self.headers)
		if self.debug:
			return response.content
		if response.error:
			raise HTTPError
 		if response.status_code == 200:
			xmlmatch = re.search(r'\<opt.*', response.content)		
			if xmlmatch:
				return self._parseXML(response.content)
			else:
				print response.content
		if response.status_code == 403:
			print 'HTTP/1.1 - GET %s - ACCESS DENIED' % url
		else: 
			raise Exception('Non-200 Return Code: %s, Content: %s' % (response.status_code, response.content))

			
	def post(self, url, data):
		"""post():
				Usage:
					response = netdot.client.post("/url", {form-data})
			
				Description: 
					This function provides a simple interface
				into the "POST" function by handling the authentication
				cookies as well as the required headers and base_url for 
				each request.  
			
				Returns: 
					Result as a multi-level dictionary on success
		"""
		response = requests.post(self.base_url + url, cookies=self.auth_cookies, data=data, headers=self.headers)
		if self.debug:
			return response.content
		if response.error:
			raise HTTPError
 		if response.status_code == 200:
			xmlmatch = re.search(r'\<opt.*', response.content)		
			if xmlmatch:
				return self._parseXML(response.content)
			else:
				print response.content
		if response.status_code == 403:
			print 'HTTP/1.1 - POST %s - ACCESS DENIED' % url
		else: 
			raise Exception('Non-200 Return Code: %s, Content: %s' % (response.status_code, response.content))

	def delete(self, url):
		"""delete():
				Usage: 
					response = netdot.client.delete("/url")

				Description: 
					This function provides a simple interface
				into the "DELETE" function by handling the authentication
				cookies as well as the required headers and base_url for 
				each request.  

				Returns: 
					Result as a multi-level dictionary
		"""
		response = requests.delete(self.base_url + url, cookies=self.auth_cookies, headers=self.headers)
		if self.debug:
			return response.content
		if response.error:
			raise HTTPError
 		if response.status_code == 200:
			xmlmatch = re.search(r'\<opt.*', response.content)		
			if xmlmatch:
				return self._parseXML(response.content)
			else:
				print response.content
		if response.status_code == 403:
			print 'HTTP/1.1 - DELETE %s - ACCESS DENIED' % url
		else: 
			raise Exception('Non-200 Return Code: %s, Content: %s' % (response.status_code, response.content))

				
	def getHostByIPID(self, id):
		"""getHostByIPID():
				Usage:
					response = netdot.client.getHostByIPID("1111")
					
				Description: 
					This function returns a NetDot-XML object 
				for the requested IP ID.
				
				Returns:
					Multi-level dictionary on success.
		"""
		return self.get("/host?ipid=" + id)

	def getHostByRRID(self, id):
		"""getHostByRRID():
				Description: 
					This function returns a multi-level dictionary object 
				for the requested RR ID.
				
				Returns:
					Multi-level dictionary on success.
		"""
		return self.get("/host?rrid=" + id)

	def getHostByName(self, name):
		"""getHostByName():
				Usage: 
					response = netdot.client.getHostByName("host")
					
				Description: 
					This function returns a NetDot-XML object 
				for the requested shortname.
				
				Returns:
					Multi-level dictionary on success.
		"""
		return self.get("/host?name=" + name)
		
	def getIPBlock(self, ipblock):
		"""getIPBlock():
				Usage: 
					response = netdot.client.getIPBlock('192.168.1.0/24')
				
				Description: 
					This function returns all of the host 
				records from the provided ip block.
				
				Returns:
					Array of NetDot-XML objects on success
		"""		
		return self.get("/host?subnet=" + ipblock)
	
	def renameHost(self, old, new):
		"""renameHost():
				Usage: 
					netdot.client.renameHost('old-name','new-name')
				
				Description: 
						This function will rename a host record.  Previously, 
					the user had to query know the RRID of the record, then 
					post the updated name to the RRID record.  This function
					automates the RRID search and constructs the post request 
					for you.
		"""
		host = self.getHostByName(old)
		rrid = host['RR']['id']
		data = {}
		data['name'] = new
		return self.post("/host?rrid=" + rrid, data)

	def createHost(self, data):
		"""createHost():
				Usage: 
					response = netdot.client.createHost({'name':'my-server',
					'subnet':'192.168.1.0/24',
					'ethernet':'XX:XX:XX:XX:XX:XX',
					'info':'My Server'})
				Description: 
					This function takes a dict and creates a new 
				record in the subnet '192.168.1.0/24' with an ethernet 
				address of 'XX:XX:XX:XX:XX:XX' and a comment of 'My Server'.  

				Returns: 
					Created record as a multi-level dictionary.
		"""		
		return self.post("/host", data)
		
	def deleteHostByRRID(self, rrid):
		"""deleteHostByRRID():
				Usage:
					response = netdot.client.deleteHostByRRD("1111")
					 
				Description: 
					This function deletes a hostname record
				for the requested RR ID. This also frees the IP.
		"""	
		return self.delete("/host?rrid=" + rrid)
		
		def getHostByAddress(self, address):
			"""getHostByAddress():
					Usage:
						response = netdot.client.getHostByIPID("192.168.0.1")

					Description: 
						This function returns a NetDot-XML object 
					for the requested IP Address.
	
					Returns:
						Multi-level dictionary on success.
			"""
			return self.get("/host?address=" + address)

		def getPersonByUsername(self, user):
			"""getPersonByUsername():
					Usage:
						response = netdot.client.getPersonByUsername("user")

					Description:
						This function returns a NetDot-XML object
					for the requested Username
		
					Returns:
						Multi-level dictionary on success.
			"""
			return self.get("/person?username=" + user)

		def getObjectByID(self, object, id):
			"""getObjectByID():
				Usage:
					response = netdot.client.getObjectByID("object", "id")

				Description:
					This function returns a NetDot-XML object 
				for the request object and id

				Return:
					Multi-level dictionary on success
			"""
			return self.get("/" + object + "?id=" + id)

		def getContactByPersonID(self, id):
			"""getContactByPersonID():
					Usage:
						response = netdot.client.getContactByPersonID("id")

					Description:
						This function returns a NetDot-XML object
					for the requested Contact

					Returns:
						Multi-level dictionary on success.
			"""
			return self.get("/contact?person=" + id)

		def getGrouprightByConlistID(self, id):
			"""getGrouprightByConlistID():
					Usage:
						response = netdot.client.getGrouprightByConlistID("id")

					Description:
							This function returns a NetDot-XML object
						for the requested Contact

					Returns:
						Multi-level dictionary on success.
			"""
			return self.get("/groupright?contactlist=" + id)

			
		def filterDict(self, dict, kword):
			"""filterDict()
				Usage:
					dot.filterDict(dict, ['list', 'of', '.*keywords'])

				Description:
					This function discends into the Multi-level
				dictionary and returns a list of [filtered] key value pairs

				Returns:
					Multi-level dictionary on success
			"""
			data = {}
			for top_k, top_v in dict.items():
				data[top_k] = {}
				for mid_k, mid_v in top_v.items():
					data[top_k][mid_k] = {}
					for bot_k, bot_v in mid_v.items():
						if kword:
							re_comb = "(" + ")|(".join(kword) + ")"
							if re.match(re_comb, bot_k):
								data[top_k][mid_k][bot_k] = bot_v
						else:
							data[top_k][mid_k][bot_k] = bot_v
			return data
			
	def _parseXML(self, xml):
		"""_parseXML():
			Description: 
					This is a VERY simple parser specifically built to 
				parse the NetDot-XML Objects
				
			Returns: 
				Multi-level dictionary.
		"""
		import xml.etree.ElementTree as ET
		data = {}
		xml_root = ET.fromstring(xml)
		for child in xml_root:
			data[child.tag] = {}
			for attribute in child.attrib:
				data[child.tag][attribute] = child.attrib[attribute]
		return data
	