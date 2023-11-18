class Encoder86():

    def __init__(self, sh, bc):
        # key in position [16]
        self.decoder32 = b"\xd9\xe1\xd9\x74\x24\xf4\x5a\x80\xc2\x17\x31\xc9\xb1\x18\x80\x32\x00\x42\xe2\xfa"
        self.shellcode = sh
        self.badchars = bc.split(",")

    def get_shellcode(self, sc):
        exit = False
        key = 0
        shellcode2 = []
        while not exit:
            exit = True
            key += 1
            for s in sc:
                value = hex(s ^ key)
                if value == 0:
                    shellcode2 = []
                    exit = False
                    break
                if len(value) == 3:
                    value = f"{value[:2]}0{value[2:]}"
                value = "\\" + value[1:]
                shellcode2.append(value)
        return key, shellcode2

    def execute(self):
        key, sh = self.get_shellcode(self.shellcode)
        shell_c = "".join(sh)
        print(shell_c)
        decoder2 = []
        for i, d in enumerate(self.decoder32):
            aux = hex(key) if i == 16 else hex(d)
            if len(aux) == 3:
                aux = f"{aux[:2]}0{aux[2:]}"
            aux = "\\" + aux[1:]
            decoder2.append(aux)
        return ("".join(decoder2) + shell_c).encode()
