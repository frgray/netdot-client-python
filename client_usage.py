#!/usr/bin/env python
# encoding: utf-8
"""
client_usage.py

Created by Francisco Gray <frgray@uoregon.edu> on 2012-11-01.
Copyright (c) 2012 University of Oregon. All rights reserved.
"""

import sys
import os
import netdot
# OR
#from netdot import client

uname = 'my_user'
pword = 'my_pass'
server = "https://netdot.localdomain/netdot"

dot = netdot.client(uname,pword,server)

r = dot.get('/host?name=my-server-name')
r = dot.post('/host', host)

r = dot.getHostByName('my-server-name')
r = dot.getHostByIPID("111111")
r = dot.getHostByRRID("111111")

host = {
	'name':'my-server', 
	'subnet':'192.168.1.0/24', 
	'ethernet':'XX:XX:XX:XX:XX:XX',
	'info':'My Server'
}
r = dot.createHost(host)
r = dot.getHostByName('my-server')
r = dot.getHostByRRID('1111')
r = dot.deleteHostByRRID('11111')

print r