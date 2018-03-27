import extra_functions.custom_print as custom_print
from extra_functions.sessions.model import ModelSession


class Windows(ModelSession):
    def __init__(self, s_obj, current_session):     
        self.meterpreter_functions = {
                        "unquoted": {
                            "function": "unquoted_services",
                            "help": "Find unquoted services path",
                            "commmand":"unquoted_services", 
                            "exec": False,
                            "param": False}
                    }
        super(Windows,self).__init__(self.meterpreter_functions, s_obj, current_session, "windows")

    
    def unquoted_services(self):
        self.send_msg(["unquoted_services"], False)
        result = self.recv_msg()
        print(result)