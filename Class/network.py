import socket
import sys
from dotenv import dotenv_values
import json

# Load .env
CONFIG = dotenv_values()

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = CONFIG.get('SERVER_IP')
        self.port = int(CONFIG.get('SERVER_PORT'))
        self.addr = (self.server, self.port)
        self.pos = self.connect()['position']
    
    # Get player positoin
    def getPos(self):
        return self.pos

    # Connect to server and return current player position (one time)
    def connect(self):
        try:
            self.client.connect(self.addr)
            return json.loads(self.client.recv(int(CONFIG.get('SERVER_BUFSIZE'))).decode())
        except socket.error as e:
            sys.exit("Server not found")

    # Send current player position to server and get opponent one
    def send(self, data):
        try:
            # TODO - Test here
            print('network', data)
            self.client.send(json.dumps(data).encode())
            return json.loads(self.client.recv(int(CONFIG.get('SERVER_BUFSIZE'))).decode())
        except socket.error as e:
            print(e)