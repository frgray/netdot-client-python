#!/usr/bin/env python
# encoding: utf-8
"""
Util.py

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
import xml.etree.ElementTree as ET

class NetdotError(Exception):
    pass

def filter_dict(dict, kword):
    """
    This function descends into the Multi-level
    dictionary and returns a list of [filtered] key value pairs
    
    Usage:
      dot.filterDict(dict, ['list', 'of', '.*keywords'])
      
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

def validate_xml(content):
    if '<opt' not in content:
        raise NetdotError(content)
  
def parse_xml(xml):
    """
    This is a VERY simple parser specifically built to 
    parse the NetDot-XML Objects
        
    Returns: 
      Multi-level dictionary.
    """
    data = {}
    xml_root = ET.fromstring(xml)
    for child in xml_root:
      if child.tag in data:
        data[child.tag][child.attrib["id"]] = child.attrib
      else:
        data[child.tag] ={}
        data[child.tag][child.attrib["id"]] = child.attrib
    return data

def dump(object):
    for property, value in vars(object).iteritems():
      print property, ": ", value  
  
