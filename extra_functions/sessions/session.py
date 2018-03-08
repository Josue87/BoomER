import extra_functions.color as color
import extra_functions.custom_print as custom_print
import os
import json
from extra_functions.sessions.linux.linux_session import Linux


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
            self.module_session = None
           
    def set_session(self,session, platform):
        self.sessions[self.current_id] = [session, platform]
        self.current_id += 1
        return self.current_id - 1
    
    def get_sessions(self):
        return self.sessions
    
    def set_autocomplete(self, completer):
        self.completer = completer

    def interact(self, session_id):
        try:
            session_id = int(session_id)
            client = self.sessions[session_id][0]
            self.current_session = client
            pl = (self.sessions[session_id][1]).lower()
            if "linux" in pl:
                self.module_session = Linux(self.current_session)
                custom_print.info("Interacting with: " + pl)
            else:
                custom_print.info("Right now only Linux is accepted")
                return
        except:
            print("Session no found")
            return
        self.completer.set_backup()
        self.completer.set_all_commands(list(self.module_session.get_functions().keys()),[])
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
                opt = self.module_session.get_functions()[split_data[0]]
                if not opt:
                    continue
                if not opt["exec"]:
                    getattr(self.module_session, opt["function"])()
                    continue
                self.send_msg(client, split_data)
                if "shell" == data_input.strip():
                    data = client.recv(4096)
                    data = data.decode()
                else:
                    data = self.recv_msg(client)
                if data:

                    data
                    if "Error" in data:
                        custom_print.error(data)
                    else:
                        getattr(self.module_session, opt["function"])(data)
            except Exception as e:
                print(str(e))
                if "Broken pipe" in str(e):
                    custom_print.info("Meterpreter closed")
                    self._delete_session(session_id)
                    return 0

    
    def _delete_session(self, id):
        try:
            del self.sessions[id]
        except:
            custom_print.error("Error deleting session " + str(id))
    
    def send_msg(self, client, msg):
        data = {
            "function": msg[0],
            "args": []
        }
        if len(msg) > 1:
            data["args"] = msg[1:]
        client.send((json.dumps(data)).encode())
    
    def recv_msg(self, client):
        data = client.recv(4096)
        return json.loads(data.decode())