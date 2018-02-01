import struct
import sys


class Encoder():

    def __init__(self, sh, arq, bc):
        self.decoder64 = b"\x48\x31\xC9\x48\x81\xE9%s\x48\x8D\x05\xEF\xFF\xFF\xFF"
        self.decoder64 += b"\x48\xBBXXXXXXXX\x48\x31\x58\x27\x48\x2D\xF8\xFF\xFF\xFF\xE2\xF4"
        # key in position [16]
        #self.decoder32 = b"\xd9\xe1\xd9\x74\x24\xf4\x5a\x80\xc2\x17\x31\xc9\xb1\x18\x80\x32\x00\x42\xe2\xfa"
        self.shellcode = sh
        block = -(((len(self.shellcode) - 1) / 8) + 1)
        aux = struct.pack('<l', int(block))
        self.decoder64 = self.decoder64 % aux
        self.key = 0
        self.badchars = bc.split(",")
        self.arq = arq

    def _convert(self):
        exit = False
        shellcode2 = []
        while not exit:
            exit = True
            self.key += 1
            for s in self.shellcode:
                value = str(hex(s ^ self.key))
                if len(value) == 3:
                    value = value[0:2] + "0" + value[2:]
                if "\\" + value[1:] in self.badchars:
                    shellcode2 = []
                    exit = False
                    break
                shellcode2.append(value)
        return shellcode2

    def execute(self):
        if "64" in self.arq:
            return self.execute64()
        else:
            pass

    def execute64(self):
        aux_dec = self.decoder64
        exit = False
        shellcode2 = self._convert()

        aux = b""
        for k in range(8):
            aux += struct.pack('B', self.key)

        aux_dec = aux_dec.replace(b'XXXXXXXX', aux)
        return_decoder = b""
        for d in aux_dec:
            aux = hex(d)
            if len(aux) == 3:
                aux = aux[0:2] + "0" + aux[2:]
            aux = "\\" + aux[1:]
            return_decoder += aux.encode()

        return_shell = b""
        for s in shellcode2:
            aux = s
            if len(aux) == 3:
                aux = aux[0:2] + "0" + aux[2:]
            aux = "\\" + aux[1:]
            return_shell += aux.encode()
        return (return_decoder.decode() + return_shell.decode()).encode()