#!/usr/bin/env python
# encoding: utf-8
"""
example.py

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

import sys
import os
import netdot

uname = 'my_user'
pword = 'my_pass'
server = "https://netdot.localdomain/netdot"
debug = 1

#for verify you can pass the valid ca location to verify or use True to use the default ssl cert verification chain in requests
# if verify not passed, verify is False by default

dot = netdot.Client.Connect(uname, pword, server, [verify], [debug])


# Direct GET/POST/DELETE calls
r = dot.get('/host?name=my-server-name')
r = dot.post('/host', host)

name = dot.get_host_by_name('foo')
cname = dot.add_cname_to_record('foo','bar.foo.example.com')
ipid = dot.get_host_by_ipid('11111')
rrid = dot.get_host_by_rrid('11111')

ipblock =  dot.get_ipblock("184.171.96.0/24")
user = dot.get_person_by_username('mary')
user_id = dot.get_person_by_id('111')

host = {
	'name':'my-server', 
	'subnet':'192.168.1.0/24', 
	'ethernet':'XX:XX:XX:XX:XX:XX',
	'info':'My Server'
}
r = dot.create_host(host)

print r
