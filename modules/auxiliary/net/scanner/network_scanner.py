#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os
import sys

import scapy.all

from core.badges import badges
from core.parser import parser
from core.formatter import formatter

class ZetaSploitModule:
    def __init__(self):
        self.badges = badges()
        self.parser = parser()
        self.formatter = formatter()
        
        self.details = {
            'Name': "auxiliary/net/scanner/network_scanner",
            'Authors': [
                'enty8080'
            ],
            'Description': "Scan local network.",
            'Comments': [
                'Uses Python scapy module to scan local network.'
            ]
        }

        self.options = {
            'RANGE': {
                'Description': "IP range.",
                'Value': "192.168.1.1/24",
                'Required': True
            }
        }

    def run(self):
        self.badges.output_process("Scanning network...")
        
        ip_range = self.parser.parse_options(self.options)
        arp = scapy.all.ARP(pdst=ip_range)
        ether = scapy.all.Ether(dst="ff:ff:ff:ff:ff:ff")
        result = scapy.all.srp(ether/arp, timeout=10, verbose=False)[0]
        
        net_data = list()
        headers = ("Host", "MAC")
        for _, received in result:
            net_data.append((received.psrc, received.hwsrc))
        self.badges.output_empty("")
        self.formatter.format_table("Network Devices", headers, *net_data)
        self.badges.output_empty("")
