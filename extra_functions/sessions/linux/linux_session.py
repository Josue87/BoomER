import extra_functions.custom_print as custom_print

class Linux:
    def __init__(self, current_session):
        self.current_session = current_session
        self.meterpreter_functions = {
                        "help": {
                            "function":"help",
                            "help":"Show this help.",
                            "execute": "help",
                            "exec": False},
                        "background": {
                            "function":"background",
                            "help":"Send Session to background",
                            "execute": "background",
                            "exec": False},
                        "exit": {
                            "function":"exit",
                            "help":"Close BoomERpreter",
                            "execute": "exit",
                            "exec": True},
                        "suid_sgid": {
                            "function": "check_result",
                            "help": "Find root SUID_SGID files",
                            "execute":"suid_sgid <path>", 
                            "exec": True},
                        "shell": {
                            "function": "shell",
                            "help": "Spawn a Shell",
                            "execute":"shell", 
                            "exec": True}
                    }

    def get_functions(self):
        return self.meterpreter_functions
    
    def check_result(self, result):
        print(result)
    
    def help(self):
        for k,v in self.meterpreter_functions.items():
            print(k + ": " + v["help"])
            print("   |_ Execute: " + v["execute"])
    
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