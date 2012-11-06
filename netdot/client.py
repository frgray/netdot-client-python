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

import os, sys
import requests

#my_config = {'verbose':sys.stderr} # Request Debugging

__version__ = '0.01' ## Not always updated

class client(object):
	def __init__(self, username=None, password=None, server=None):
		"""Constructor
		"""
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
			self._login()											 # Call the _login() function 
		else:
			raise ParameterError('user, password and server are required')
		
	def _login(self):
		response = requests.post(self.login_url, data=self.params, headers=self.headers)
		if response.status_code == 200:
			self.auth_cookies = response.cookies
		else:
			raise LoginError('Invalid Credentials')

	def get(self, url):
		response = requests.get(self.base_url + url, cookies=self.auth_cookies, headers=self.headers)
		if response.status_code == 200:
			return response.content
			
	def post(self, url, data):
		response = requests.post(self.base_url + url, cookies=self.auth_cookies, data=data, headers=self.headers)
		if response.status_code == 200:
			return response.content

	def delete(self, url):
		response = requests.delete(self.base_url + url, cookies=self.auth_cookies, headers=self.headers)
		pp.pprint(response)
		if response.status_code == 200:
			return response.content
				
	def getHostByIPID(self, id):
		return self.get("/host?ipid=" + id)

	def getHostByRRID(self, id):
		return self.get("/host?rrid=" + id)

	def getHostByName(self, name):
		return self.get("/host?name=" + name)
		
	def getIPBlock(self, ipblock):
		return self.get("/host?subnet=" + ipblock)
	
	def createHost(self, data):
		return self.post("/host", data)
		
	def deleteHostByRRID(self, rrid):
		return self.delete("/host?rrid=" + rrid)
		
		
		