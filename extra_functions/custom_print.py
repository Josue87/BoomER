import extra_functions.color as color

def error(msg):
    print(color.RED + "[KO] " +  color.RESET + str(msg))

def ok(msg):
     print(color.GREEN + "[OK] " +  color.RESET + str(msg))

def info(msg):
    print(color.BLUE + "[I] " + color.RESET + str(msg))