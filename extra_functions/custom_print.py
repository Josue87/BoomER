import extra_functions.color as color

def error(msg):
    print(color.RED + "[-] " +  color.RESET + str(msg))

def ok(msg):
     print(color.GREEN + "[+] " +  color.RESET + str(msg))

def info(msg):
    print(color.BLUE + "[*] " + color.RESET + str(msg))