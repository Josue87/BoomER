#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mayhem/datatypes/windows.py
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the project nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  'AS IS' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import ctypes
import platform

from .structure import MayhemStructure

_IMAGE_NUMBEROF_DIRECTORY_ENTRIES = 16
is_64bit = platform.architecture()[0] == '64bit'

# http://msdn.microsoft.com/en-us/library/windows/desktop/aa383751(v=vs.85).aspx
BOOLEAN = ctypes.c_byte
BOOL = ctypes.c_int
BYTE = ctypes.c_uint8
PBYTE = ctypes.POINTER(BYTE)
LPBYTE = PBYTE

WORD = ctypes.c_uint16

DWORD = ctypes.c_uint32
DWORDLONG = ctypes.c_uint64
DWORD32 = ctypes.c_uint32
DWORD64 = ctypes.c_uint64
PDWORD = ctypes.POINTER(DWORD)
LPDWORD = PDWORD

QWORD = ctypes.c_uint64
PQWORD = ctypes.POINTER(QWORD)
LPQWORD = PQWORD

SHORT = ctypes.c_int16

LONG = ctypes.c_int32
LONGLONG = ctypes.c_int64
LONG32 = ctypes.c_int32
LONG64 = ctypes.c_int64
PLONG = ctypes.POINTER(LONG)
LPLONG = PLONG

UCHAR = ctypes.c_uint8
USHORT = ctypes.c_uint16
ULONG = ctypes.c_uint32
PULONG = ctypes.POINTER(ULONG)
ULONGLONG = ctypes.c_uint64
PULONGLONG = ctypes.POINTER(ULONGLONG)
ULONG_PTR = ctypes.c_uint64 if is_64bit else ctypes.c_ulong

PSTR = ctypes.c_char_p
LPSTR = PSTR
PWSTR = ctypes.c_wchar_p
LPWSTR = PWSTR

UCHAR = ctypes.c_ubyte
PUCHAR = ctypes.POINTER(ctypes.c_ubyte)

HANDLE = ctypes.c_void_p
HINSTANCE = HANDLE
HMODULE = HANDLE
PVOID = ctypes.c_void_p
LPVOID = PVOID
LPCVOID = PVOID
NTSTATUS = ctypes.c_uint32

# platform specific data primitives
SIZE_T = ctypes.c_uint64 if is_64bit else ctypes.c_uint32
class LARGE_INTEGER(MayhemStructure):
    _fields_ = [
        ('LowPart', DWORD),
        ('HighPart', LONG),
    ]


class LIST_ENTRY(MayhemStructure):
    _fields_ = [
        ('Flink', ctypes.c_void_p),
        ('Blink', ctypes.c_void_p),
    ]


class UNICODE_STRING(MayhemStructure):
    _fields_ = [
        ('Length', USHORT),
        ('MaximumLength', USHORT),
        ('Buffer', PWSTR),
    ]

    @classmethod
    def from_string(cls, string):
        inst = cls()
        inst.Length = len(string)
        inst.MaximumLength = len(string) + 1
        inst.Buffer = string
        return inst


class STARTUPINFO(MayhemStructure):
    """see:
    http://msdn.microsoft.com/en-us/library/windows/desktop/ms686331(v=vs.85).aspx
    """
    _fields_ = [
        ('cb', DWORD),
        ('lpReserved', LPSTR),
        ('lpDesktop', LPSTR),
        ('lpTitle', LPSTR),
        ('dwX', DWORD),
        ('dwY', DWORD),
        ('dwXSize', DWORD),
        ('dwYSize', DWORD),
        ('dwXCountChars', DWORD),
        ('dwYCountChars', DWORD),
        ('dwFillAttribute', DWORD),
        ('dwFlags', DWORD),
        ('wShowWindow', WORD),
        ('cbReserved2', WORD),
        ('lpReserved2', LPBYTE),
        ('hStdInput', HANDLE),
        ('hStdOutput', HANDLE),
        ('hStdError', HANDLE),
    ]


class LDR_MODULE(MayhemStructure):
    _fields_ = [
        ('InLoadOrderModuleList', LIST_ENTRY),
        ('InMemoryOrderModuleList', LIST_ENTRY),
        ('InInitializationOrderModuleList', LIST_ENTRY),
        ('BaseAddress', ctypes.c_void_p),
        ('EntryPoint', ctypes.c_void_p),
        ('SizeOfImage', ULONG),
        ('FullDllName', UNICODE_STRING),
        ('BaseDllName', UNICODE_STRING),
        ('Flags', ULONG),
        ('LoadCount', SHORT),
        ('TlsIndex', SHORT),
        ('HashTableEntry', LIST_ENTRY),
        ('TimeDateStamp', ULONG),
    ]


class LOADED_IMAGE(MayhemStructure):
    """see:
    http://msdn.microsoft.com/en-us/library/windows/desktop/ms680349%28v=vs.85%29.aspx
    """
    _fields_ = [
        ('ModuleName', PSTR),
        ('hFile', HANDLE),
        ('MappedAddress', PUCHAR),
        ('FileHeader', ctypes.c_void_p),
        ('LastRvaSection', ctypes.c_void_p),
        ('NumberOfSections', ULONG),
        ('Sections', ctypes.c_void_p),
        ('Characteristics', ULONG),
        ('fSystemImage', BOOLEAN),
        ('fDOSImage', BOOLEAN),
        ('fReadOnly', BOOLEAN),
        ('Version', UCHAR),
        ('Links', ctypes.c_void_p),
        ('SizeOfImage', ULONG),
    ]


class LUID(MayhemStructure):
    """see:
    https://msdn.microsoft.com/en-us/library/windows/desktop/aa379261(v=vs.85).aspx
    """
    _fields_ = [
        ('LowPart', DWORD),
        ('HighPart', LONG),
    ]


class IMAGE_DATA_DIRECTORY(MayhemStructure):
    """see:
    http://msdn.microsoft.com/en-us/library/windows/desktop/ms680305%28v=vs.85%29.aspx
    """
    _fields_ = [
        ('VirtualAddress', DWORD),
        ('Size', DWORD),
    ]


class IMAGE_DOS_HEADER(MayhemStructure):
    _fields_ = [
        ('e_magic', WORD),
        ('e_cblp', WORD),
        ('e_cp', WORD),
        ('e_crlc', WORD),
        ('e_cparhdr', WORD),
        ('e_minalloc', WORD),
        ('e_maxalloc', WORD),
        ('e_ss', WORD),
        ('e_sp', WORD),
        ('e_csum', WORD),
        ('e_ip', WORD),
        ('e_cs', WORD),
        ('e_lfarlc', WORD),
        ('e_ovno', WORD),
        ('e_res', WORD * 4),
        ('e_oemid', WORD),
        ('e_oeminfo', WORD),
        ('e_res2', WORD * 10),
        ('e_lfanew', LONG),
    ]


class IMAGE_EXPORT_DIRECTORY(MayhemStructure):
    _fields_ = [
        ('Characteristics', DWORD),
        ('TimeDateStamp', DWORD),
        ('MajorVersion', WORD),
        ('MinorVersion', WORD),
        ('Name', DWORD),
        ('Base', DWORD),
        ('NumberOfFunctions', DWORD),
        ('NumberOfNames', DWORD),
        ('AddressOfFunctions', DWORD),
        ('AddressOfNames', DWORD),
        ('AddressOfNameOrdinals', DWORD),
    ]


class IMAGE_FILE_HEADER(MayhemStructure):
    _fields_ = [
        ('Machine', WORD),
        ('NumberOfSections', WORD),
        ('TimeDateStamp', DWORD),
        ('PointerToSymbolTable', DWORD),
        ('NumberOfSymbols', DWORD),
        ('SizeOfOptionalHeader', WORD),
        ('Characteristics', WORD),
    ]


class IMAGE_OPTIONAL_HEADER(MayhemStructure):
    _fields_ = [
        ('Magic', WORD),
        ('MajorLinkerVersion', BYTE),
        ('MinorLinkerVersion', BYTE),
        ('SizeOfCode', DWORD),
        ('SizeOfInitializedData', DWORD),
        ('SizeOfUninitializedData', DWORD),
        ('AddressOfEntryPoint', DWORD),
        ('BaseOfCode', DWORD),
        ('BaseOfData', DWORD),
        ('ImageBase', DWORD),
        ('SectionAlignment', DWORD),
        ('FileAlignment', DWORD),
        ('MajorOperatingSystemVersion', WORD),
        ('MinorOperatingSystemVersion', WORD),
        ('MajorImageVersion', WORD),
        ('MinorImageVersion', WORD),
        ('MajorSubsystemVersion', WORD),
        ('MinorSubsystemVersion', WORD),
        ('Win32VersionValue', DWORD),
        ('SizeOfImage', DWORD),
        ('SizeOfHeaders', DWORD),
        ('CheckSum', DWORD),
        ('Subsystem', WORD),
        ('DllCharacteristics', WORD),
        ('SizeOfStackReserve', DWORD),
        ('SizeOfStackCommit', DWORD),
        ('SizeOfHeapReserve', DWORD),
        ('SizeOfHeapCommit', DWORD),
        ('LoaderFlags', DWORD),
        ('NumberOfRvaAndSizes', DWORD),
        ('DataDirectory', IMAGE_DATA_DIRECTORY * _IMAGE_NUMBEROF_DIRECTORY_ENTRIES),
    ]


class IMAGE_IMPORT_BY_NAME(MayhemStructure):
    _fields_ = [
        ('Hint', WORD),
        ('Name', BYTE),
    ]


class IMAGE_IMPORT_DESCRIPTOR(MayhemStructure):
    _fields_ = [
        ('OriginalFirstThunk', DWORD),
        ('TimeDateStamp', DWORD),
        ('ForwarderChain', DWORD),
        ('Name', DWORD),
        ('FirstThunk', DWORD),
    ]


class IMAGE_THUNK_DATA32(MayhemStructure):
    _fields_ = [
        ('ForwarderString', DWORD),
        ('Function', DWORD),
        ('Ordinal', DWORD),
        ('AddressOfData', DWORD),
    ]


class IMAGE_NT_HEADERS32(MayhemStructure):
    _fields_ = [
        ('Signature', DWORD),
        ('FileHeader', IMAGE_FILE_HEADER),
        ('OptionalHeader', IMAGE_OPTIONAL_HEADER),
    ]


class _IO_STATUS_BLOCK_U0(ctypes.Union):
    _fields_ = [
        ('Status', NTSTATUS),
        ('Pointer', PVOID),
    ]


class IO_STATUS_BLOCK(MayhemStructure):
    _anonymous_ = ('u0',)
    _fields_ = [
        ('u0', _IO_STATUS_BLOCK_U0),
        ('Information', ULONG_PTR),
    ]


class PEB(MayhemStructure):
    """see:
    http://msdn.microsoft.com/en-us/library/windows/desktop/aa813706%28v=vs.85%29.aspx
    """
    _fields_ = [
        ('Reserved1', BYTE * 2),
        ('BeingDebugged', BYTE),
        ('SpareBool', BYTE),
        ('Mutant', ctypes.c_void_p),
        ('ImageBaseAddress', ctypes.c_void_p),
        ('Ldr', ctypes.c_void_p),
        ('ProcessParameters', ctypes.c_void_p),
        ('SubSystemData', ctypes.c_void_p),
        ('ProcessHeap', ctypes.c_void_p),
        ('Reserved4', BYTE * 96),
        ('Reserved5', ctypes.c_void_p * 52),
        ('PostProcessInitRoutine', ctypes.c_void_p),
        ('Reserved6', BYTE * 128),
        ('Reserved7', ctypes.c_void_p),
        ('SessionId', ULONG),
    ]


class PEB_LDR_DATA(MayhemStructure):
    _fields_ = [
        ('Length', ULONG),
        ('Reserved', UCHAR * 4),
        ('SsHandle', HANDLE),
        ('InLoadOrderModuleList', LIST_ENTRY),
        ('InMemoryOrderModuleList', LIST_ENTRY),
        ('InInitializationOrderModuleList', LIST_ENTRY),
    ]


class PROCESS_BASIC_INFORMATION(MayhemStructure):
    """see:
    http://msdn.microsoft.com/en-us/library/windows/desktop/ms684280%28v=vs.85%29.aspx
    """
    _fields_ = [
        ('Reserved1', ctypes.c_void_p),
        ('PebBaseAddress', ctypes.c_void_p),
        ('Reserved2', ctypes.c_void_p * 2),
        ('UniqueProcessId', PULONG),
        ('Reserved3', ctypes.c_void_p),
    ]


class SECURITY_ATTRIBUTES(MayhemStructure):
    """see:
    http://msdn.microsoft.com/en-us/library/windows/desktop/aa379560(v=vs.85).aspx
    """
    _fields_ = [
        ('nLength', DWORD),
        ('lpSecurityDescriptor', LPVOID),
        ('bInheritHandle', BOOL),
    ]


class HANDLE_ENTRY(MayhemStructure):
    _fields_ = [
        ('phead', ctypes.c_void_p),
        ('pOwner', ctypes.c_void_p),
        ('bType', ctypes.c_uint8),
        ('bFlags', ctypes.c_uint8),
        ('wUniq', ctypes.c_uint16),
    ]

    @classmethod
    def from_handle(cls, handle):
        shared_info = SHARED_INFO.from_user32()
        addr = shared_info.aheList + (ctypes.sizeof(cls) * (handle & 0xffff))
        return cls.from_address(addr)


class WND_MSG(MayhemStructure):
    _fields_ = [
        ('maxMsgs', ctypes.c_uint32),
        ('abMsgs', ctypes.c_void_p),
    ]


class SHARED_INFO(MayhemStructure):
    _fields_ = [
        ('psi', ctypes.c_void_p),
        ('aheList', ctypes.c_void_p),
        ('HeEntrySize', ctypes.c_uint32),
        ('pDispInfo', ctypes.c_void_p),
        ('ulSharedDelta', ctypes.c_uint64 if is_64bit else ctypes.c_uint32),
        ('awmControl', WND_MSG * 31),
        ('DefWindowMsgs', WND_MSG),
        ('DefWindowSpecMsgs', WND_MSG),
    ]

    @classmethod
    def from_user32(cls):
        kernel32 = ctypes.windll.kernel32
        addr = kernel32.GetProcAddress(kernel32.GetModuleHandleA('user32.dll'), 'gSharedInfo')
        return cls.from_address(addr)


class SYSTEM_INFO(MayhemStructure):
    """see:
    http://msdn.microsoft.com/en-us/library/windows/desktop/ms724958(v=vs.85).aspx
    """
    _fields_ = [
        ('wProcessorArchitecture', WORD),
        ('wReserved', WORD),
        ('dwPageSize', DWORD),
        ('lpMinimumApplicationAddress', ctypes.c_void_p),
        ('lpMaximumApplicationAddress', ctypes.c_void_p),
        ('dwActiveProcessorMask', DWORD),
        ('dwNumberOfProcessors', DWORD),
        ('dwProcessorType', DWORD),
        ('dwAllocationGranularity', DWORD),
        ('wProcessorLevel', WORD),
        ('wProcessorRevision', WORD),
    ]

    @classmethod
    def from_kernel32(cls):
        kernel32 = ctypes.windll.kernel32
        system_info = cls()
        kernel32.GetSystemInfo(ctypes.byref(system_info))
        return system_info


class SYSTEM_PROCESS_INFORMATION(MayhemStructure):
    """see:
    https://msdn.microsoft.com/en-us/library/windows/desktop/ms725506(v=vs.85).aspx
    http://undocumented.ntinternals.net/index.html?page=UserMode%2FUndocumented%20Functions%2FSystem%20Information%2FStructures%2FSYSTEM_PROCESS_INFORMATION.html
    """
    _fields_ = [
        ('NextEntryOffset', ULONG),
        ('NumberOfThreads', ULONG),
        ('Reserved1', BYTE * 48),
        ('Reserved2', PVOID * 3),
        ('UniqueProcessId', HANDLE),
        ('Reserved3', PVOID),
        ('HandleCount', ULONG),
        ('Reserved4', BYTE * 4),
        ('Reserved5', PVOID * 11),
        ('PeakPagefileUsage', SIZE_T),
        ('PrivatePageCount', SIZE_T),
        ('Reserved6', LARGE_INTEGER * 6),
    ]


class PROCESS_INFORMATION(MayhemStructure):
    """see:
    http://msdn.microsoft.com/en-us/library/windows/desktop/ms684873(v=vs.85).aspx
    """
    _fields_ = [
        ('hProcess', HANDLE),
        ('hThread', HANDLE),
        ('dwProcessId', DWORD),
        ('dwThreadId', DWORD),
    ]


class MEMORY_BASIC_INFORMATION32(MayhemStructure):
    """see:
    http://msdn.microsoft.com/en-us/library/windows/desktop/aa366775(v=vs.85).aspx
    """
    _fields_ = [
        ('BaseAddress', ULONG),
        ('AllocationBase', PVOID),
        ('AllocationProtect', DWORD),
        ('RegionSize', ULONG),
        ('State', DWORD),
        ('Protect', DWORD),
        ('Type', DWORD),
    ]


class MEMORY_BASIC_INFORMATION64(MayhemStructure):
    """see:
    http://msdn.microsoft.com/en-us/library/windows/desktop/aa366775(v=vs.85).aspx
    """
    _fields_ = [
        ('BaseAddress', ULONGLONG),
        ('AllocationBase', PVOID),
        ('AllocationProtect', DWORD),
        ('__alignment1', DWORD),
        ('RegionSize', ULONGLONG),
        ('State', DWORD),
        ('Protect', DWORD),
        ('Type', DWORD),
        ('__alignment2', DWORD),
    ]


# platform specific structures
if is_64bit:
    MEMORY_BASIC_INFORMATION = MEMORY_BASIC_INFORMATION64
else:
    MEMORY_BASIC_INFORMATION = MEMORY_BASIC_INFORMATION32
PMEMORY_BASIC_INFORMATION = ctypes.POINTER(MEMORY_BASIC_INFORMATION)


class MENUITEMINFOW(MayhemStructure):
    """see:
    https://msdn.microsoft.com/en-us/library/windows/desktop/ms647578(v=vs.85).aspx
    """
    _fields_ = [
        ('cbSize', ctypes.c_uint),
        ('fMask', ctypes.c_uint),
        ('fType', ctypes.c_uint),
        ('fState', ctypes.c_uint),
        ('wID', ctypes.c_uint),
        ('hSubMenu', HANDLE),
        ('hbmpChecked', HANDLE),
        ('hbmpUnchecked', HANDLE),
        ('dwItemData', ctypes.POINTER(ctypes.c_ulong)),
        ('dwTypeData', ctypes.c_wchar_p),
        ('cch', ctypes.c_uint),
        ('hbmpItem', HANDLE),
    ]
