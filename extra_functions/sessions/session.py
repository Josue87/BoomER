import extra_functions.color as color
import extra_functions.custom_print as custom_print
import os
import json
from extra_functions.autocomplete import MyCompleter
from extra_functions.sessions.linux.linux_session import Linux
from extra_functions.sessions.windows.windows_session import Windows


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
            self.completer = MyCompleter.getInstance()
            self.module_session = None
           
    def set_session(self,session, platform):
        self.sessions[self.current_id] = [session, platform]
        self.current_id += 1
        return self.current_id - 1
    
    def get_sessions(self):
        return self.sessions
    
    def interact(self, session_id):
        try:
            session_id = int(session_id)
            client = self.sessions[session_id][0]
            self.current_session = client
            pl = (self.sessions[session_id][1]).lower()
            if "linux" in pl:
                self.module_session = Linux(self, self.current_session)
                custom_print.info("Interacting with: " + pl)
            elif "windows" in pl:
                self.module_session = Windows(self, self.current_session)
                custom_print.info("Interacting with: " + pl)
            else:
                custom_print.info("Right now only Linux or Windows are accepted")
                return
        except Exception as e:
            print(e)
            print("Session no found")
            return
        self.completer.set_backup()
        self.completer.set_all_commands(list(self.module_session.get_functions().keys()),[])
        while True:
            try:
                data_input = input(color.YELLOW + "BoomERpreter >> " + color.RESET)
                data_input = data_input.strip()
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
                getattr(self.module_session, opt["function"])(split_data)
            except KeyboardInterrupt:
                self.completer.restore_backup()
                self._delete_session(session_id)
                return 0
            except Exception as e:
                custom_print.error(str(e))
                if "Broken pipe" in str(e):
                    custom_print.info("Meterpreter closed")
                    self._delete_session(session_id)
                    return 0
    
    def _delete_session(self, id):
        try:
            del self.sessions[id]
            self.current_session.close()
            custom_print.info("Session %s has been closed" % str(id))
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
        return True
    
    def recv_msg(self, client):
        data = client.recv(4096)
        if len(data) == 0:
            raise Exception("Broken pipe")
        return json.loads(data.decode())