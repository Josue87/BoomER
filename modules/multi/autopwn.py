import os
import sys

from os.path import isfile, join, isdir

from extra_functions.load import loadModule
from module import Module


class BoomerModule(Module):
    def __init__(self):
        info = {
            "Name": "Autopwn",
            "Author": "Antonio Marcos",
            "Description": "Run all OS exploits"
        }
        options = {

        }
        super(BoomerModule, self).__init__(options, info)

    def run(self):
        current_os = None

        if sys.platform.startswith('win'):
            current_os = 'windows'
        elif sys.platform.startswith('linux'):
            current_os = 'linux'
        elif sys.platform.startswith('mac'):
            current_os = 'mac'

        if current_os == None:
            self.print_error('The OS is not supported, try to run this module in a Windows, Linux or MacOS.')
            return

        try:
            modules = self.load_all_os_modules(current_os)
            for module in modules:
                try:
                    module_load = loadModule(module)
                    self.print_info('Checking module: ' + module)
                    module_load.check()
                except Exception as e:
                    self.print_error(e)
        except Exception as e:
            self.print_error(e)

    def load_all_os_modules(self, current_os):
        os_modules_path = 'modules' + os.sep + current_os
        modules = self.load_modules_from_path(os_modules_path)

        return modules

    def load_modules_from_path(self, path):
        modules = []
        for dir in os.listdir(path):
            child = join(path, dir)
            if isfile(child) and child.endswith('.py') and not child.__contains__('__init__.py'):
                child = child.split(os.sep)
                child.pop(0)
                child = "/".join(child)

                modules.append(child[:-3])
            elif isdir(child):
                modules = modules + self.load_modules_from_path(child)

        return modules