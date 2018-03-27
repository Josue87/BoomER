import extra_functions.custom_print as custom_print

class ModelSession:
    def __init__(self, met, s_obj, current_session, system):
        self.current_session = current_session
        self.system = system
        self.obj_session = s_obj
        self.meterpreter_functions = met
        self.meterpreter_functions["help"] = {
                            "function":"help",
                            "help":"Show this help.",
                            "commmand": "help",
                            "exec": False,
                            "param": False}
        self.meterpreter_functions["exit"] = {
                            "function":"exit",
                            "help":"Close BoomERpreter",
                            "commmand": "exit",
                            "exec": False,
                            "param": False}
        self.meterpreter_functions["background"] =  {
                            "function":"background",
                            "help":"Send Session to background",
                            "commmand": "background",
                            "exec": False,
                            "param": False}
        
    def get_functions(self):
        return self.meterpreter_functions
    
    def help(self):
        for k,v in self.meterpreter_functions.items():
            print(k + ": " + v["help"])
            print("   |_ Execute: " + v["commmand"])
        
    def send_msg(self, data, need_args):
        if need_args and len(data) == 1:
            print("This function needs argument(s)")
            return "No"
        self.obj_session.send_msg(self.current_session, data) 

    def recv_msg(self):
        return self.obj_session.recv_msg(self.current_session)
    