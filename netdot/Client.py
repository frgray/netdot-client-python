#!/usr/bin/env python
# encoding: utf-8
"""
Client.py

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

import os
import sys
import re
import requests
import Util

__version__ = "0.03"

class Connect(object):
  def __init__(self, username, password, server, debug = 0):
      """
      Class constructor, instantiates a number of 
      variables for use in the class.  Mainly the required
      NetDot HTTP headers and login form parameters.
    
      Usage:
        import netdot
        dot = netdot.client(username,
                            password,
                            "https://netdot.localdomain/netdot",
                            [debug])
            
      Returns: NetDot.client object.
      """
      if debug == 1:
        self.debug = True
        print "DEBUG MODE: ON"
      if username and password and server:
        self.base_url = server + '/rest'
        self.login_url = server + '/NetdotLogin'
        self.timeout = 10
        self.retries = 3
        self.version = __version__
        self.headers = { 'User_Agent':'Netdot::Client::REST/self.version',
                         'Accept':'text/xml; version=1.0'}
        params = {'destination':'index.html',
                  'credential_0':username, 
                  'credential_1':password, 
                  'permanent_session':1}
      # Call the _login() function    
        self._login(params)
      else:
        raise AttributeError('Username, Password and Server are REQUIRED')
  
  def _login(self,params):
      """
      Internal Function. Logs into the NetDot API with provided credentials, 
      stores the Apache generated cookies into the self object to be 
      reused.  
    
      Arguments:
        dict -- 'destination':'index.html', 
                'credential_0':username, 
                'credential_1':password, 
                'permanent_session':1
      """
      response = requests.post(self.login_url, data=params, 
                              headers=self.headers)
      if response.status_code == 200:
        self.auth_cookies = response.request.cookies
      else:
        raise AttributeError('Invalid Credentials')
  
  def get(self, url):
      """
      This function provides a simple interface
      into the "GET" function by handling the authentication
      cookies as well as the required headers and base_url for 
      each request. 
    
      Arguments:
        url -- Url to append to the base url
      
      Usage: 
        response = netdot.client.get("/url")
      
      Returns: 
        Result as a multi-level dictionary on sucsess. 
      """
      response = requests.get(self.base_url + url, 
                              cookies=self.auth_cookies, 
                              headers=self.headers)
      if hasattr(self, 'debug'):
        Util.dump(response)
      if response.error:
        raise HTTPError
      if response.status_code == 200:
        xmlmatch = re.search(r'\<opt.*', response.content)    
        if xmlmatch:
          return response.content
        else:
          print response.content
      if response.status_code == 403:
        print 'HTTP/1.1 - GET %s - ACCESS DENIED' % url
      else: 
        raise Exception('Non-200 Return Code: %s, Content: %s' % 
                        (response.status_code, response.content))
  
  def post(self, url, data):
      """
      This function provides a simple interface
      into the "POST" function by handling the authentication
      cookies as well as the required headers and base_url for 
      each request.     
    
      Arguments:
        url -- Url to append to the base url
        data -- dict of key/value pairs that the form requires
    
      Usage:
        response = netdot.client.post("/url", {form-data})
    
      Returns: 
        Result as a multi-level dictionary on success
      """
      response = requests.post(self.base_url + url, 
                              cookies=self.auth_cookies, 
                              data=data, headers=self.headers)
      if hasattr(client, 'debug'):
        self._dump(response)
      if response.error:
        raise HTTPError
      if response.status_code == 200:
        xmlmatch = re.search(r'\<opt.*', response.content)    
        if xmlmatch:
          return response.content
        else:
          print response.content
      if response.status_code == 403:
        print 'HTTP/1.1 - POST %s - ACCESS DENIED' % url
      else: 
        raise Exception('Non-200 Return Code: %s, Content: %s' % 
                        (response.status_code, response.content))
  
  def delete(self, url):
      """
      This function provides a simple interface
      into the "HTTP/1.0 DELETE" function by handling the authentication
      cookies as well as the required headers and base_url for 
      each request.     

      Arguements:
        url -- Url to append to the base url
    
      Usage: 
        response = netdot.client.delete("/url")

      Returns: 
        Result as an empty multi-level dictionary
      """
      response = requests.delete(self.base_url + url, 
                                cookies=self.auth_cookies, 
                                headers=self.headers)
      if hasattr(client, 'debug'):
        self._dump(response)
      if response.error:
        raise HTTPError
      if response.status_code == 200:
        xmlmatch = re.search(r'\<opt.*', response.content)    
        if xmlmatch:
          return response.content
        else:
          print response.content
      if response.status_code == 403:
        print 'HTTP/1.1 - DELETE %s - ACCESS DENIED' % url
      else: 
        raise Exception('Non-200 Return Code: %s, Content: %s' % 
                      (response.status_code, response.content))
  
  def get_host_by_ipid(self, id):
      """
      This function returns a NetDot-XML object 
      for the requested IP ID.
    
      Arguments: 
        id -- NetDot IP ID
    
      Usage:
        response = netdot.client.getHostByIPID("1111")
    
      Returns:
        Multi-level dictionary on success.
      """
      return Util.parse_xml(self.get("/host?ipid=" + id))
  
  def get_host_by_rrid(self, id):
      """
      This function returns a NetDot-XML object 
      for the requested RR ID.
    
      Arguments: 
        id -- NetDot RR ID
    
      Usage:
        response = netdot.client.getHostByRRID("1111")
    
      Returns:
        Multi-level dictionary on success.
      """
      return Util.parse_xml(self.get("/host?rrid=" + id))
  
  def get_host_by_name(self, name):
      """
      This function returns a NetDot-XML object 
      for the requested shortname
    
      Arguments: 
        name -- DNS shortname
    
      Usage:
        response = netdot.client.getHostByName("foo")
    
      Returns:
        Multi-level dictionary on success.
      """
      return Util.parse_xml(self.get("/host?name=" + name))
  
  def get_ipblock(self, ipblock):
      """
      This function returns all of the host 
      records from the provided ip block.
    
      Arguments: 
        ipblock - IpBlock in CIDR notation 
    
      Usage: 
        response = netdot.client.getIPBlock('192.168.1.0/24')
      
      Returns:
        Array of NetDot-XML objects on success
      """   
      return self.get("/host?subnet=" + ipblock)
  
  def get_host_address(self, address):
      """
      This function returns a NetDot-XML object 
      for the requested IP Address.   
    
      Arguments:
        address -- IP Address in "dotted-quad" syntax

      Usage:
        response = netdot.client.getHostByIPID("192.168.0.1")

      Returns:
        Multi-level dictionary on success.
      """
      return Util.parse_xml(self.get("/host?address=" + address))
  
  def get_person_by_username(self, user):
      """
      Returns a single-level dict of the requested Username

      Arguments:
        user -- Desired username

      Usage:
        response = netdot.client.getPersonByUsername("user")
      
      Returns:
        Multi-level dictionary on success.
      """
      return Util.parse_xml(self.get("/person?username=" + user))
  
  def get_person_by_id(self, id):
      """
      Returns a single-level dict of the requested user id

      Arguments:
        id -- Desired User ID

      Usage:
        response = netdot.client.getPersonById("id")
      
      Returns:
        Multi-level dictionary on success.
      """
      xml = self.get("/person?id=" + id)
      xml_root = ET.fromstring(xml)
      person = dict()
    
      for child in xml_root:
        person[id] = child.attrib
      return person
  
  def get_object_by_id(self, object, id):
      """
      Returns a single-level dict of the requested object and id
    
      Arguments:
        object -- 'device' or 'host' etc...
        id  --  Object ID
    
      Usage:
        response = netdot.client.getObjectByID("object", "id")
    
      Returns:
        Multi-level dictionary on success
      """
      return self.get("/" + object + "?id=" + id)
  
  def get_contact_by_person_id(self, id):
      """
      Returns a single-level dict of the requested Person
    
      Arguments:
        id  --  person id
    
      Usage:
        response = netdot.client.getContactByPersonID('id')
    
      Returns:
        Single-level dictionary on success
      """
      xml = self.get("/contact?person=" + id)
      xml_root = ET.fromstring(xml)
      person = dict()
    
      for child in xml_root:
        person[id] = child.attrib
      return person
  
  def get_contact_by_username(self, user):
      """
      Returns a single-level dict of the requested Username
    
      Arguments:
        user  --  NetDot Username
    
      Usage:
        response = netdot.client.getContactByUsername("mary")
    
      Returns:
        Multi-level dictionary on success
      """
      person = self.getPersonByUsername(user)
      return self.getContactByPersonID(person['id'])    
  
  def get_grouprights_by_conlist_id(self, id):
      """
      Returns a single-level dict of the requested group's 
      access rights
    
      Arguments:
        id  --  NetDot Contact List ID
    
      Usage:
        response = netdot.client.getGrouprightsByConlistID("id")
    
      Returns:
        Multi-level dictionary on success
      """
      return self.get("/groupright?contactlist=" + id)
  
  def add_cname_to_record(self, name, cname):
      """
      This fucntion will add a CNAME to an 
      existing resource record or "A" record
    
      Arguments:
        name -- A record
        cname -- Desired CNAME
      
      Usage: 
        response = dot.addCnameToARecord('foo.example.com', 'bar.example.com')
      """
      data = { 'cname': cname }
      host = self.getHostByName(name)
      for key in host[name]['RR'].iterkeys():
        for attr, attr_val in host[name]['RR'][key].iteritems():
          if attr == 'name' and attr_val == name:
            return self.post("/host?rrid=" + host[name]['RR'][key]['id'], data)
  
  def rename_host(self, old, new):
      """
      This function will rename a host record.  Previously, 
      the user had to query know the RRID of the record, then 
      post the updated name to the RRID record.  This function
      automates the RRID search and constructs the post request 
      for you.

      Arguments:
        old -- Old DNS shortname
        new -- New DNS shortname

      Usage: 
        netdot.client.renameHost('old-name','new-name')
      """
      host = self.getHostByName(old)
      rrid = host['RR']['id']
      data = {}
      data['name'] = new
      return self.post("/host?rrid=" + rrid, data)
  
  def create_host(self, data):
      """
      This function takes a dict and creates a new 
      record in the subnet '192.168.1.0/24' with an ethernet 
      address of 'XX:XX:XX:XX:XX:XX' and a comment of 'My Server'. 
    
      Arguments:
        data -- dict with at least the following key:value pairs:
              name:'servername'
              subnet: 'CIDR notation'

      Usage: 
        response = netdot.client.createHost({'name':'my-server',
                                            'subnet':'192.168.1.0/24',
                                            'ethernet':'XX:XX:XX:XX:XX:XX',
                                            'info':'My Server'})

      Returns: 
        Created record as a multi-level dictionary.
      """
      return self.post("/host", data) 
  
  def delete_host_by_rrid(self, rrid):
      """
      This function deletes a hostname record
      for the requested RR ID. This also frees the IP.
    
      Arguments:
        rrid -- NetDot Resource Record ID
    
      Usage:
        response = netdot.client.deleteHostByRRD("1111")
    
      Returns: 
      """
      return self.delete("/host?rrid=" + rrid)
  
    

    
    