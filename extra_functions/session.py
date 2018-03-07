import extra_functions.color as color
import extra_functions.custom_print as custom_print
import os


class Session:
    __instance = None

    @staticmethod
    def getInstance():
        if Session.__instance == None:
            Session()
        return Session.__instance 

    def __init__(self):
        if Session.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Session.__instance = self
            self.sessions = {}
            self.current_id = 1
            self.current_session = None
            self.completer = None
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
    
    def set_session(self,session):
        self.sessions[self.current_id] = session
        self.current_id += 1
        return self.current_id - 1
    
    def get_sessions(self):
        return self.sessions
    
    def set_autocomplete(self, completer):
        self.completer = completer

    def interact(self, session_id):
        try:
            session_id = int(session_id)
            client = self.sessions[session_id]
            self.current_session = client
        except:
            print("Session no found")
            return
        self.completer.set_backup()
        self.completer.set_all_commands(list(self.meterpreter_functions.keys()),[])
        while True:
            try:
                data_input = input(color.YELLOW + "BoomERpreter >> " + color.RESET)
                if data_input == "":
                    continue
                if "exit" in data_input:
                    self.completer.restore_backup()
                    self._delete_session(session_id)
                    return
                if "background" in data_input:
                    custom_print.info("Session %s to background"%str(session_id))
                    self.completer.restore_backup()
                    return 1
                split_data = data_input.split()
                opt = self.meterpreter_functions[split_data[0]]
                if not opt:
                    continue
                if not opt["exec"]:
                    getattr(self, opt["function"])()
                    continue
                client.send(data_input.encode())
                data = client.recv(4096)
                if data:
                    if "Error" in data.decode():
                        custom_print.error("Wrong input: " + data_input)
                    else:
                        getattr(self, opt["function"])(data.decode())
            except Exception as e:
                print(str(e))
                if "Broken pipe" in str(e):
                    custom_print.info("Meterpreter closed")
                    self._delete_session(session_id)
                    return 0

    def check_result(self, result):
        print(result)
    
    def help(self):
        for k,v in self.meterpreter_functions.items():
            self.print_info(k + ": " + v["help"])
            print("   |_ Execute: " + v["execute"])
    
    def shell(self, result):
        if "No" == result:
            custom_print.info("No shell obtained")
            return
        print(result.strip(), end=" ")
        while True:
            data_input = input()
            self.current_session.send((data_input+"\n").encode())
            if "exit" in data_input:
                return
            recv = self.current_session.recv(1024)
            print(recv.decode().strip(), end=" ")
    
    def _delete_session(self, id):
        try:
            del self.sessions[id]
        except:
            custom_print.error("Error deleting session " + str(id))