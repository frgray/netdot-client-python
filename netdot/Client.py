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

__version__ = "1.0"

class Connect(object):
  def __init__(self, username, password, server, debug = 0):
      """
      Class constructor, instantiates a number of
      variables for use in the class.  Mainly the required
      NetDot HTTP headers and login form parameters.

      Usage:
        import netdot
        dot = netdot.Client.connect(username,
                                    password,
                                    "https://netdot.localdomain/netdot",
                                    debug)

      Returns: NetDot.client object.
      """

      self.debug = bool(debug)
      if self.debug:
        print "DEBUG MODE: ON"
      self.http = requests.session()
      self.http.verify=False

      self.server = server
      self.base_url = server + '/rest'
      self.login_url = server + '/NetdotLogin'
      self.timeout = 10
      self.retries = 3
      self.version = __version__
      self.http.headers.update({ 'User_Agent':'Netdot::Client::REST/self.version',
                         'Accept':'text/xml; version=1.0'})
      # Call the _login() function
      self._login(username, password)

  def _login(self, username, password):
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
      params = {'destination':'index.html',
                  'credential_0':username,
                  'credential_1':password,
                  'permanent_session':1}
      response = self.http.post(self.login_url, data=params)
      if response.status_code != 200:
        raise AttributeError('Invalid Credentials')

  def logout(self):
      """
      Logout of the NetDot API
      """
      response = self.http.post(self.server + '/logout.html')

  def get_xml(self, url):
      """
      This function provides a simple interface
      into the "GET" function by handling the authentication
      cookies as well as the required headers and base_url for
      each request.

      Arguments:
        url -- Url to append to the base url

      Usage:
        response = netdot.Client.get_xml("/url")

      Returns:
        XML string output from Netdot
      """
      response = self.http.get(self.base_url + url)
      if self.debug:
        Util.dump(response)
      response.raise_for_status()
      return response.content

  def get(self, url):
      """
      This function delegates to get_xml() and parses the
      response xml to return a dict

      Arguments:
        url -- Url to append to the base url

      Usage:
        dict = netdot.Client.get("/url")

      Returns:
        Result as a multi-level dictionary on success.
      """
      return Util.parse_xml(self.get_xml(url))

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
        response = netdot.Client.post("/url", {form-data})

      Returns:
        Result as a multi-level dictionary on success
      """
      response = self.http.post(self.base_url + url, data=data)
      if self.debug:
        Util.dump(response)
      response.raise_for_status()

      Util.validate_xml(response.content)
      return response.content

  def delete(self, url):
      """
      This function provides a simple interface
      into the "HTTP/1.0 DELETE" function by handling the authentication
      cookies as well as the required headers and base_url for
      each request.

      Arguments:
        url -- Url to append to the base url

      Usage:
        response = netdot.Client.delete("/url")

      Returns:
        Result as an empty multi-level dictionary
      """
      response = self.http.delete(self.base_url + url)
      if self.debug:
        Util.dump(response)
      response.raise_for_status()
      return response.content

  def get_host_by_ipid(self, id):
      """
      Given an Ipblock ID, returns the Ipblock and associated
      resource records' data

      Arguments:
        id -- NetDot Ipblock ID

      Usage:
        response = netdot.Client.get_host_by_ipid("1111")

      Returns:
        Multi-level dictionary on success.
      """
      return self.get("/host?ipid=" + id)

  def get_host_by_rrid(self, id):
      """
      Given a resource record ID, returns the
      RR's data

      Arguments:
        id -- NetDot RR ID

      Usage:
        response = netdot.Client.get_host_by_rrid("1111")

      Returns:
        Multi-level dictionary on success.
      """
      return self.get("/host?rrid=" + id)

  def get_host_by_name(self, name):
      """
      Given a RR name, returns the RR's data

      Arguments:
        name -- RR label (DNS name)

      Usage:
        response = netdot.Client.get_host_by_name("foo")

      Returns:
        Multi-level dictionary on success.
      """
      return self.get("/host?name=" + name)

  def get_ipblock(self, ipblock):
      """
      This function returns all of the host
      records from the provided IP block

      Arguments:
        ipblock - Subnet address in CIDR notation

      Usage:
        response = netdot.Client.get_ipblock('192.168.1.0/24')

      Returns:
        Array of NetDot-XML objects on success
      """
      return self.get("/host?subnet=" + ipblock)

  def get_host_address(self, address):
      """
      Given an IP address, returns the associated
      records' data

      Arguments:
        address -- IP Address in "dotted-quad" syntax

      Usage:
        response = netdot.Client.get_host_address("192.168.0.1")

      Returns:
        Multi-level dictionary on success.
      """
      return self.get("/host?address=" + address)

  def get_person_by_username(self, user):
      """
      Returns a single-level dict of the requested Username

      Arguments:
        user -- Desired username

      Usage:
        response = netdot.Client.get_person_by_username("user")

      Returns:
        Multi-level dictionary on success.
      """
      return self.get("/person?username=" + user)

  def get_person_by_id(self, id):
      """
      Returns a single-level dict of the requested user id

      Arguments:
        id -- Desired User ID

      Usage:
        response = netdot.Client.get_person_by_id("id")

      Returns:
        Multi-level dictionary on success.
      """
      xml = self.get_xml("/person?id=" + id)
      xml_root = ET.fromstring(xml)
      person = dict()

      for child in xml_root:
        person[id] = child.attrib
      return person

  def create_object(self, object, data):
      """
      Create object record when it's parameters are known.
      Parameters are passed as key:value pairs in a dictionary

      Arguments:
        data -- key:value pairs applicable for an object:
                (e.g. a device below)
              name:                 'devicename'
              snmp_managed:         '0 or 1'
              snmp_version:         '1 or 2 or 3'
              community:            'SNMP community'
              snmp_polling:         '0 or 1'
              canautoupdate:        '0 or 1'
              collect_arp:          '0 or 1'
              collect_fwt:          '0 or 1'
              collect_stp:          '0 or 1'
              info:                 'Description string'

      Usage:
        response = netdot.Client.create_device("device",
                                               {'name':'my-device',
                                                'snmp_managed':'1',
                                                'snmp_version':'2',
                                                'community':'public',
                                                'snmp_polling':'1',
                                                'canautoupdate':'1',
                                                'collect_arp':'1',
                                                'collect_fwt':'1',
                                                'collect_stp':'1',
                                                'info':'My Server'}

      Returns:
        Created record as a multi-level dictionary.
      """
      return self.post("/" + object, data)

  def get_object_by_id(self, object, id):
      """
      Returns a single-level dict of the requested object and id

      Arguments:
        object -- 'device', 'person',  etc...
        id  --  Object ID

      Usage:
        response = netdot.Client.get_object_by_id("object", "id")

      Returns:
        Multi-level dictionary on success
      """
      return self.get("/" + object + "?id=" + id)

  def get_object_by_name(self, object, name):
      """
      Returns a multi-level dict of the requested object by name

      Arguments:
        object -- 'device', 'person',  etc...
        name  --  name

      Usage:
        response = netdot.Client.get_object_by_id("object", "name")

      Returns:
        Multi-level dictionary on success
      """
      return self.get("/" + object + "?name=" + name)

  def get_object_by_desc(self, object, desc):
      """
      Returns a multi-level dict of the requested object by
      description

      Arguments:
        object -- 'device', 'person',  etc...
        desc  --  Object description

      Usage:
        response = netdot.Client.get_object_by_desc("object", "desc")

      Returns:
        Multi-level dictionary on success
      """
      return self.get("/" + object + "?description=" + desc)

  def get_object_by_info(self, object, info):
      """
      Returns a multi-level dict of the requested object by
      description

      Arguments:
        object -- 'device', 'person',  etc...
        info  -- Comment Field 

      Usage:
        response = netdot.Client.get_object_by_info("object", "info")

      Returns:
        Multi-level dictionary on success
      """
      return self.get("/" + object + "?info=" + info)

  def delete_object_by_id(self, object, id):
      """
      This function deletes an object record by it's id

      Arguments:
        object -- 'device', 'vlan', etc...
        id  -- Object ID

      Usage:
        response = netdot.Client.delete_object_by_id("device", "id")

      Returns:
      """
      return self.delete("/" + object + "/" + id)

  def get_contact_by_person_id(self, id):
      """
      Returns contact information for given person ID

      Arguments:
        id  --  person id

      Usage:
        response = netdot.Client.get_contact_by_person_id('id')

      Returns:
        Single-level dictionary on success
      """
      xml = self.get_xml("/contact?person=" + id)
      xml_root = ET.fromstring(xml)
      person = dict()

      for child in xml_root:
        person[id] = child.attrib
      return person

  def get_contact_by_username(self, user):
      """
      Returns contact information for given person username

      Arguments:
        user  --  NetDot Username

      Usage:
        response = netdot.Client.get_contact_by_username("mary")

      Returns:
        Multi-level dictionary on success
      """
      person = self.get_person_by_username(user)
      return self.get_contact_by_person_id(person['id'])

  def get_grouprights_by_conlist_id(self, id):
      """
      Returns a single-level dict of the requested group's
      access rights

      Arguments:
        id  --  NetDot Contact List ID

      Usage:
        response = netdot.Client.get_grouprights_by_conlist_id("id")

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
        response = dot.add_cname_to_record('foo.example.com', 'bar.example.com')
      """
      data = { 'cname': cname }
      host = self.get_host_by_name(name)
      for key in host[name]['RR'].iterkeys():
        for attr, attr_val in host[name]['RR'][key].iteritems():
          if attr == 'name' and attr_val == name:
            return self.post("/host?rrid=" + host['RR'][key]['id'], data)

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
        netdot.Client.rename_host('old-name','new-name')
      """
      host = self.get_host_by_name(old)
      rrid = host['RR']['id']
      data = {}
      data['name'] = new
      return self.post("/host?rrid=" + rrid, data)

  def create_host(self, data):
      """
      Create DNS records (and optionally) DHCP entries
      for a given IP address, using the given
      name and description.
      Passing a subnet address instead of an IP address,
      the function will create records for the next
      available IP address in the subnet.

      Arguments:
        data -- dict with the following key:value pairs:
              name:     'servername'
              address:  'IP'
              subnet:   'CIDR'
              ethernet: 'MAC'
              info:     'Description string'

      Usage:
        response = netdot.Client.create_host({'name':'my-server',
                                              'subnet':'192.168.1.0/24',
                                              'ethernet':'XX:XX:XX:XX:XX:XX',
                                              'info':'My Server'})

      Returns:
        Created record as a multi-level dictionary.
      """
      return self.post("/host", data)

  def delete_host_by_rrid(self, id):
      """
      This function deletes a hostname record
      for the requested RR ID. This also frees the IP.

      Arguments:
        rrid -- NetDot Resource Record ID

      Usage:
        response = netdot.Client.delete_host_by_rrid("1111")

      Returns:
      """
      return self.delete("/host?rrid=" + id)

  def delete_host_by_ipid(self, id):
      """
      This function deletes all hostname records
      for the requested Ipblock ID.

      Arguments:
        ipid -- NetDot Ipblock ID

      Usage:
        response = netdot.Client.delete_host_by_ipid("1111")

      Returns:
      """
      return self.delete("/host?ipid=" + id)

  def get_vlans_by_groupid(self, id):
      """
      Returns a multi-level dict of vlans in a vlan group

      Arguments:
        id  --  vlan group id

      Usage:
        response = netdot.Client.get_object_by_id("id")

      Returns:
        Multi-level dictionary on success
      """
      return self.get("/vlan?VlanGroup=" + id)

  def get_object_by_filter(self, object, field, value):
      """
      Returns a multi-level dict of an objects (device, interface, rr, person)
      filtered by an object field/attribute
      Arguments:
        object -- NetDot object ID
        field -- NetDot field/attribute of object
        value -- The value to select from the field.

      Usage:
        response = netdot.Client.get_object_by_filter("device", "name", "some-switch")

      Returns:
        Multi-level dictionary on success
      """
      url = "/{}?{}={}".format(object, field, value)
      return self.get(url)
