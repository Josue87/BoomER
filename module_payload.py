from extra_functions.autocomplete import MyCompleter
from extra_functions.load import loadModule
from module import Module


class PayloadModule(Module):
    def __init__(self, opt, info=None, compatible=None):
        if info is None:
            info = {}
        if compatible is None:
            compatible = []
        opt["payload"] = ["""If this option is empty open a local root shell\n
        Encode the shellcode and avoid bad characters""", "", False]
        super(PayloadModule, self).__init__(opt, info)
        self.payload = None
        self.compatible = compatible
        self.register_single_operation("list_payloads", "Shows supported payloads")
        self.complete = MyCompleter.getInstance()
        self.complete.set_all_payloads(self.compatible)

    def put(self, args):
        key = args[0]
        value = args[1]
        if key == "payload" and value:
            if value not in self.compatible:
                self.print_info("Payload not accepted by this module")
                return
            self.payload = loadModule(value, "support/payloads/")
            if self.payload:
                self.options["payload"][1] = value
                self.print_info(self.payload.get_info_metasploit())
            else:
                self.print_error("Wrong payload")
        elif key in self.options:
            super(PayloadModule, self).put(args)
        else:
            self.payload.put(key, value)

    def print_options(self):
        super(PayloadModule, self).print_options()
        if self.payload:
            self.payload.print_options()

    def get_options(self):
        aux = self.options
        if self.payload:
            aux.update(self.payload.get_options())
        return aux

    def list_payloads(self):
        print("-- Supported Payloads --")
        for payload in self.compatible:
            print(payload)
