import subprocess
from subprocess import Popen

from module import Module


class BoomerModule(Module):

    def __init__(self):
        info = {
            "Name": "MacOS App Finder",
            "Author": "Antonio Marcos",
            "Description": "Find applications installed on MacOS"
        }
        options = {
            "file": ["File to dump results", "files/output/mac_app_finder.txt", False]
        }
        super(BoomerModule, self).__init__(options, info)

    def run(self):
        self.file_open = None
        if file := self.options.get("file")[1]:
            try:
                command = f"system_profiler SPApplicationsDataType > {file}"
                stdout, stderr = Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       shell=True).communicate()
                self.print_ok(f"File write in the path: {file}")
            except Exception as e:
                self.print_error(e)
                self.print_info("Only displayed by the console.")
