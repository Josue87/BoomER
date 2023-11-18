def get_address(p, ip):
    host = _treat_host(str(ip))
    port = _treat_port(str(p))
    return port.encode(), host.encode()


def _treat_host(ip):
    host = ip.split(".")
    if len(host) != 4:
        print("Bad IP")
    host_tr = ""
    for h in host:
        hex_h = _configure(hex(int(h)))
        host_tr += hex_h
    return host_tr


# We can use struct.pack
def _treat_port(p):
    p1 = "\\x00"
    p2 = ""
    port = hex(int(p))
    p2 = port
    if len(port) > 4:
        p1 = port[:4]
        p2 = f"0x{port[4:]}"
        p1 = _configure(p1)
    p2 = _configure(p2)
    return p1 + p2


def _configure(p):
    aux = p
    if len(aux) == 3:
        aux = f"{aux[:2]}0{aux[2:]}"
    aux = "\\" + aux[1:]
    return aux
