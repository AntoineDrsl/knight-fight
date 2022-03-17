import socket
from dotenv import dotenv_values
from _thread import *
from functions import *
import json
from random import randrange

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

# Default values
POS = [
    CONFIG.get('P1_DEFAULT_X') + ',' + CONFIG.get('P1_DEFAULT_Y'),
    CONFIG.get('P2_DEFAULT_X') + ',' + CONFIG.get('P2_DEFAULT_Y')
]
SIDE = ['left', 'right']
DIRECTION = ['right', 'left']
LIFE = [CONFIG.get('DEFAULT_HEALTH'), CONFIG.get('DEFAULT_HEALTH')]
ATTACKING = [False, False]
HEARTH_X = randrange(int(CONFIG.get('WINDOW_WIDTH')))
HEARTH_Y = -10
HEARTH = str(HEARTH_X) + ',' + str(HEARTH_Y)

# Client listening
def threaded_client(conn, player):
    # Use global variables
    global CURRENT_PLAYER
    global HEARTH_X
    global HEARTH_Y
    global HEARTH

    # Connection info
    conn.send(json.dumps({
        'position': POS[player],
        'side': SIDE[player],
        'life': LIFE[player],
        'direction': DIRECTION[player],
        'attacking': ATTACKING[player],
        'hearth': HEARTH
    }).encode())

    reply = {}
    while True:
        try:
            # Get data send by network
            network_data = conn.recv(int(CONFIG.get('SERVER_BUFSIZE'))).decode()
            if network_data:
                data = json.loads(network_data)
                POS[player] = data['position']
                LIFE[player] = data['health']
                DIRECTION[player] = data['direction']
                ATTACKING[player]= data['attacking']
                if data['hearth']:
                    # If hearth, move it
                    if(HEARTH_Y <= int(CONFIG.get('GROUND_Y'))):
                        HEARTH_Y += 1
                    HEARTH = str(HEARTH_X) + ',' + str(HEARTH_Y)
                else:
                    # Else, create new
                    HEARTH_X = randrange(int(CONFIG.get('WINDOW_WIDTH')))
                    HEARTH_Y = -10
            
            # Prepare response
            reply['side'] = SIDE[player]
            reply['hearth'] = HEARTH
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

    # Remove user if disconnect
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