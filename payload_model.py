from extra_functions.xor_encode import Encoder
from extra_functions.set_address_shellcodes import get_address
from struct import pack
from socket import inet_aton
import extra_functions.color as color
import extra_functions.custom_print as custom_print



class Payload():
    def __init__(self, shellcode, size, use_metaploit=False, info_metasploit="", arq="x64"):
        self.shellcode = shellcode
        self.size = size
        self.use_metaploit = use_metaploit
        self.info_metasploit = info_metasploit
        self.arq = str(arq)
        self.options = {
            "encode": ["Host to connect the shell", False, False],
            "lhost": ["Host to connect the shell", "", True],
            "lport": ["Port to connect the shell", "", True],
            "badchars": ["Port to connect the shell (example \\x00,\\xab)", "\\x00", True]
        }
    
    def get_info_metasploit(self):
        if not self.use_metaploit:
            return "This payload is not compatible with Metasploit"
        return "Compatible with Metasploit: " + self.info_metasploit
        
    def get_shellcode(self, port, host):
        if self.options["encode"][1]:
            sh_aux = self.shellcode % (pack(">h",int(port)), inet_aton(host))
            enc = Encoder(sh_aux,self.arq, self.options["badchars"][1])
            sh_aux = enc.execute()
        sh_aux = self.shellcode % (get_address(port, host))
        return sh_aux

    def put(self, key, value):
        try:
            self.options[key][1] = value
            custom_print.info(key + " => " + value)
        except:
            custom_print.error("Wrong option: " + key)
    
    def get_size(self):
        return self.sizeodule
    
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

