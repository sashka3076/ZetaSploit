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
import subprocess

from core.badges import badges
from core.storage import storage
from core.formatter import formatter
from core.modules import modules

class execute:
    def __init__(self):
        self.badges = badges()
        self.storage = storage()
        self.formatter = formatter()
        self.modules = modules()

    def execute_command(self, commands, arguments):
        if commands:
            if not self.execute_core_command(commands, arguments):
                if not self.execute_module_command(commands, arguments):
                    if not self.execute_plugin_command(commands, arguments):
                        self.badges.output_error("Unrecognized command: " + commands[0] + "!")
        
    def execute_system(self, commands):
        subprocess.call(self.formatter.format_arguments(commands))
        
    def execute_core_command(self, commands, arguments):
        if commands[0] in self.storage.get("commands").keys():
            command = self.storage.get("commands")[commands[0]]
            if command.details['NeedsArgs']:
                if (len(commands) - 1) < command.details['ArgsCount']:
                    self.badges.output_usage(command.details['Usage'])
                else:
                    command.details['Args'] = self.formatter.format_arguments(arguments)
                    try:
                        command.run()
                    except (KeyboardInterrupt, EOFError):
                        self.badges.output_empty("")
            else:
                try:
                    command.run()
                except (KeyboardInterrupt, EOFError):
                    self.badges.output_empty("")
            return True
        return False
        
    def execute_module_command(self, commands, arguments):
        if self.modules.check_current_module():
            if hasattr(self.modules.get_current_module_object(), "commands"):
                if commands[0] in self.modules.get_current_module_object().commands.keys():
                    command = self.modules.get_current_module_object().commands[commands[0]]
                    self.parse_and_execute_command(commands, command, arguments)
                    return True
        return False
        
    def execute_plugin_command(self, commands, arguments):
        if self.storage.get("loaded_plugins"):
            for plugin in self.storage.get("loaded_plugins").keys():
                if hasattr(self.storage.get("loaded_plugins")[plugin], "commands"):
                    for label in self.storage.get("loaded_plugins")[plugin].commands.keys():
                        if commands[0] in self.storage.get("loaded_plugins")[plugin].commands[label].keys():
                            command = self.storage.get("loaded_plugins")[plugin].commands[label][commands[0]]
                            self.parse_and_execute_command(commands, command, arguments)
                            return True
        return False
        
    def parse_and_execute_command(self, commands, command, arguments):
        if command['NeedsArgs']:
            if (len(commands) - 1) < command['ArgsCount']:
                self.badges.output_usage(command['Usage'])
            else:
                command['Args'] = self.formatter.format_arguments(arguments)
                try:
                    command['Run']()
                except (KeyboardInterrupt, EOFError):
                    self.badges.output_empty("")
        else:
            try:
                command['Run']()
            except (KeyboardInterrupt, EOFError):
                self.badges.output_empty("")
