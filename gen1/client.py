import socket
PORT = 8080
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('54.81.106.48', PORT))

PLAY_GAME = True

while PLAY_GAME:
    mes = s.recv(BUFFER_SIZE) 
    move = input(mes)
    s.sendall(move)
