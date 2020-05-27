# This client code is written for testing purposes on the server
# Not the full client

import socket
import  battleship
flags = battleship.FLAGS
flags = {v: k for k, v in flags.items()}
PORT = 8080
BUFFER_SIZE = 6

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('3.95.242.45', PORT))
PLAY_GAME = True


while PLAY_GAME:
    print("recving")
    mes = s.recv(BUFFER_SIZE).decode("UTF-8")
    move = input(mes)
    s.sendall(move.encode("UTF-8"))
    print("sent mes")


