from module import Module
from extra_functions.load import loadModule


class PayloadModule(Module):
    def __init__(self, opt, info={}):
        opt["payload"] = ["""If this option is empty open a local root shell\n
        Use -e to encode the shellcode and avoid NULL characters""", "", False]
        super(PayloadModule, self).__init__(opt, info)
        self.payload = None
    
    def put(self, args):
        key = args[0]
        value = args[1]
        if key == "payload" and value:
            self.payload = loadModule(value, "support/payloads")
            if self.payload:
                self.options["payload"][1] = value
                if "-e" in args:
                    self.print_info("Encode enable")
                    self.options["encode"][1] = True
                self.print_info(self.payload.get_info_metasploit())
            else:
                self.print_error("Wrong payload")
        else:
            if key in self.options:
                super(PayloadModule, self).put(args)
            else:
                self.payload.put(key, value)

    def print_options(self):
        super(PayloadModule, self).print_options()
        if self.payload:
            self.payload.print_options()

    def get_options(self):
        aux = self.options
        aux.update(self.payload.get_options())
        return aux