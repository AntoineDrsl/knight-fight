import socket
from dotenv import dotenv_values
from _thread import *
from functions import *
import json

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

# Default DIRECTION
DIRECTION = [
    'right',
    'left'
]

# Default LIFE
LIFE = [
    CONFIG.get('DEFAULT_HEALTH'),
    CONFIG.get('DEFAULT_HEALTH')
]

ATTACKING = [
    False,
    False
]

# Client listening
def threaded_client(conn, player):
    global CURRENT_PLAYER

    # Connection info
    conn.send(json.dumps({
        'position': POS[player],
        'side': SIDE[player],
        'life': LIFE[player],
        'direction': DIRECTION[player],
        'attacking': ATTACKING[player]
    }).encode())

    reply = {}
    while True:
        try:
            # Get data send by network
            test = conn.recv(int(CONFIG.get('SERVER_BUFSIZE'))).decode()
            if test:
                data = json.loads(test)
                POS[player] = data['position']
                LIFE[player] = data['health']
                DIRECTION[player] = data['direction']
                ATTACKING[player]= data['attacking']
            
            # Prepare response
            reply['side'] = SIDE[player]
            if player == 1:
                reply['position'] = POS[0]
                reply['health'] = LIFE[0]
                reply['direction'] = DIRECTION[0]
                reply['attacking'] = ATTACKING[0]
            else:
                reply['position'] = POS[1]
                reply['health'] = LIFE[1]
                reply['direction'] = DIRECTION[1]
                reply['attacking'] = ATTACKING[1]

            # print("Received: ", data)
            # print("Sending: ", reply)

            # Send to network
            conn.sendall(json.dumps(reply).encode())
        except socket.error as e:
            # If error, stop loop
            print(e)
            break

    print("Lost connection")
    CURRENT_PLAYER -= 1
    conn.close()

# Launch client listening
CURRENT_PLAYER = 0
while True:
    # Connect with client
    conn, addr = SOCKET.accept()
    print("Connected to: ", addr)

    # Start listening to client
    start_new_thread(threaded_client, (conn, CURRENT_PLAYER))
    CURRENT_PLAYER += 1