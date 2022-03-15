import socket
from dotenv import dotenv_values
from _thread import *
from functions import *

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
    (int(CONFIG.get('P1_DEFAULT_X')), int(CONFIG.get('P1_DEFAULT_Y'))),
    (int(CONFIG.get('P2_DEFAULT_X')), int(CONFIG.get('P2_DEFAULT_Y')))
]

# Client listening
def threaded_client(conn, player):
    conn.send(str.encode(make_pos(POS[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(int(CONFIG.get('SERVER_BUFSIZE'))).decode())
            POS[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = POS[0]
                else:
                    reply = POS[1]

                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
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