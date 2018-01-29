from extra_functions.xor_encode import Encoder
from extra_functions.set_address_shellcodes import get_address


class Payload():
    def __init__(self, shellcode, size, use_metaploit=False, info_metasploit="", encode=False, arq="x64"):
        self.shellcode = shellcode
        self.size = size
        self.use_metaploit = use_metaploit
        self. info_metasploit = info_metasploit
        self.encode = encode
        self.arq = str(arq)        
    
    def get_info_metasploit(self):
        if not self.use_metaploit:
            return "This payload is not compatible with Metasploit"
        return "Compatible with Metasploit: " + self.info_metasploit
        
    def get_shellcode(self, host, port):
        self.shellcode = self.shellcode %(get_address(host,port))
        if self.encode:
            enc = Encoder(self.shellcode,self.arq, self.size)
            self.shellcode = enc.execute()
        return self.shellcode
    
    def get_size(self):
        return self.size
    
    def metasploit_compatible(self):
        return self.use_metaploit
