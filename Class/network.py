import socket
import sys
from dotenv import dotenv_values

# Load .env
CONFIG = dotenv_values()

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = CONFIG.get('SERVER_IP')
        self.port = int(CONFIG.get('SERVER_PORT'))
        self.addr = (self.server, self.port)
        self.pos = self.connect()
    
    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(int(CONFIG.get('SERVER_BUFSIZE'))).decode()
        except socket.error as e:
            sys.exit("Server not found")

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(int(CONFIG.get('SERVER_BUFSIZE'))).decode()
        except socket.error as e:
            print(e)