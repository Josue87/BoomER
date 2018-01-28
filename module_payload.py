from module import Module
from extra_functions.load import loadModule

class PayloadModule(Module):
    def __init__(self, opt, info = {}):
        super(PayloadModule, self).__init__(opt,info)
        self.payload = None
    
    def put(self, args):
        if args[0] == "payload":
            self.options["payload"][1] = args[1]
            self.payload = loadModule(args[1], "support/payloads")
            if self.payload:
                self.print_info("Execute in Metasploit: use exploit/multi/handler")
                self.print_info("set payload " + self.payload.get_metasploit())
                self.options["lhost"] = ["Host to connect the shell", "", True]
                self.options["lport"] = ["Port to connect the shell", "", True]
            else:
                self.print_error("Wrong payload")
        else:
            super(PayloadModule, self).put(args)