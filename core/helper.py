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
import socket
import url_normalize

from core.storage import storage

class helper:
    def __init__(self):
        self.storage = storage()

    def getip(self):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server.connect(("192.168.1.1", 80))
            local_host = server.getsockname()[0]
            server.close()
            local_host = local_host
        except Exception:
            local_host = "127.0.0.1"
        return local_host

    def strip_scheme(self, url):
        url = url.replace('http://', '', 1)
        url = url.replace('https://', '', 1)
        return url.replace('/', '')
    
    def normalize_url(self, url):
        return url_normalize.url_normalize(url)
    
    def len_file(self, path):
        return str(os.path.getsize(path)) + " bytes"

    def len_line(self, line):
        return str(len(line.encode())) + " bytes"
