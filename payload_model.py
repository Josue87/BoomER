class Payload():
    def __init__(self, shellcode, size, use_metaploit=False, info_metasploit=""):
        self.shellcode = shellcode
        self.size = size
        self.use_metaploit = use_metaploit
        self. info_metasploit = info_metasploit        
    
    def get_info_metasploit(self):
        if not self.use_metaploit:
            return "This payload is not compatible with Metasploit"
        return "Compatible with Metasploit: " + self.info_metasploit
        
    def get_shellcode(self):
        return self.shellcode
    
    def get_size(self):
        return self.size
    
    def metasploit_compatible(self):
        return self.use_metaploit
