import socket
from dotenv import dotenv_values
from _thread import *
from functions import *
import json
import sys

# Load .env
CONFIG = dotenv_values()

# Launch sockets
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    SOCKET.bind((CONFIG.get('SERVER_IP'), int(CONFIG.get('SERVER_PORT'))))
except socket.error as e:
    print(e)

SOCKET.listen(2)
print("Waiting for a connection, Server started")

# Default position
POS = [
    CONFIG.get('P1_DEFAULT_X') + ',' + CONFIG.get('P1_DEFAULT_Y'),
    CONFIG.get('P2_DEFAULT_X') + ',' + CONFIG.get('P2_DEFAULT_Y')
]

# Default side
SIDE = [
    'left',
    'right'
]

# Default LIFE
LIFE = [
    CONFIG.get('DEFAULT_HEALTH'),
    CONFIG.get('DEFAULT_HEALTH')
]

# Client listening
def threaded_client(conn, player):
    # Connection info
    conn.send(json.dumps({
        'position': POS[player],
        'side': SIDE[player],
        'life': LIFE[player]
    }).encode())

    reply = {}
    while True:
        try:
            # Get data send by network
            test = conn.recv(int(CONFIG.get('SERVER_BUFSIZE'))).decode()
            data = json.loads(test)
            POS[player] = data['position']
            LIFE[player] = data['health']

            if not data:
                print("Disconnected")
                break
            else:
                # Prepare response
                reply['side'] = SIDE[player]
                if player == 1:
                    reply['position'] = POS[0]
                    reply['health'] = LIFE[0]
                else:
                    reply['position'] = POS[1]
                    reply['health'] = LIFE[1]

                print("Received: ", data)
                print("Sending: ", reply)

            # Send to network
            conn.sendall(json.dumps(reply).encode())
        except socket.error as e:
            print(e)
            break

    print("Lost connection")
    conn.close()

# Launch client listening
CURRENT_PLAYER = 0
while True:
    conn, addr = SOCKET.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, CURRENT_PLAYER))
    CURRENT_PLAYER += 1