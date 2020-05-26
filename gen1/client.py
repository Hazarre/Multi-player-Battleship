import socket
PORT = 8080
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('54.81.106.48', PORT))
PLAY_GAME = True

while PLAY_GAME:
    print("recving")
    mes = s.recv(BUFFER_SIZE) 
    move = raw_input(mes)
    s.sendall(move)
    print("sent mes")
