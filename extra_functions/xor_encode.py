#TODO
class Encoder():
    
    def __init__(self, sh, arq, size):
        # key in position [11] and shellcode size in [7]
        self.decoder64 = b"\xeb\x0e\x5b\x31\xc9\x80\xc1\xFF\xc0\x0c\x0b\xFF\xe2\xfa\xff\xe3\xe8\xed\xff\xff\xff"
        # key in position [16]
        self.decoder32 = b"\xd9\xe1\xd9\x74\x24\xf4\x5a\x80\xc2\x17\x31\xc9\xb1\x18\x80\x32\x00\x42\xe2\xfa"
        self.shellcode = sh
        self.key = 0
        self.size = int(size)
        self.arq = arq
    
    def _convert(self, shellcode):
        exit = False
        shellcode2 = []
        while not exit:
            exit = True
            self.key += 1
            for s in self.shellcode:
                value =  str(hex(s ^ self.key))
                if value == "0x0":
                    shellcode2 = []
                    exit = False
                    break
                if len(value) == 3:
                    value = value[0:2] + "0" + value[2:]
                shellcode2.append(value)
        return shellcode2

    def _get_shellcode(self, sc):
        shellcode_conv = self._convert(sc)
        shellcode2 = []
        for s in shellcode_conv:
            aux = "\\" + s[1:]
            shellcode2.append(aux)
        
        return shellcode2
    
    def _treat_int(self, num):
        hkey = hex(num)
        if len(hkey) == 3:
            hkey = hkey[0:2] + "0" + hkey[2:]
        hkey = "\\" + hkey[1:]
        return hkey
   
    def _get_decoder(self, decoder, opt=64):
        i = 0
        decoder2 = []
        for d in decoder:
            if i == 11 and opt ==64:
                decoder2.append(self._treat_int(self.key))
            elif i == 7 and opt ==64:
                decoder2.append(self._treat_int(self.size))
            elif i == 16 and opt == 32:
                decoder2.append(self._treat_int(self.key))
            else:
                aux = hex(d)
                if len(aux) == 3:
                    aux = aux[0:2] + "0" + aux[2:]
                aux = "\\" + aux[1:]
                decoder2.append(aux)
            i += 1
        return decoder2
    
    def execute(self):
        if "64" in self.arq:
            return self.execute64()
        else:
            return self.execute32()

    def execute64(self):
        sh = self._get_shellcode(self.shellcode)
        decoder2 = self._get_decoder(self.decoder64)
        return_shell = b""
        for d in decoder2:
            return_shell += d.encode()
        for s in sh:
            return_shell += s.encode()
        return return_shell
    
    def execute32(self):
        sh = self._get_shellcode(self.shellcode)
        decoder2 = self._get_decoder(self.decoder32, opt=32)
        return_shell = b""
        for d in decoder2:
            return_shell += d.encode()
        for s in sh:
            return_shell += s.encode()
        return return_shell