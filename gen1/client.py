import socket
PORT = 8080
BUFFER_SIZE = 6

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('3.95.242.45', PORT))
PLAY_GAME = True

while PLAY_GAME:
    print("recving")
    mes = s.recv(BUFFER_SIZE) 
    move = input(mes)
    s.sendall(move.encode("UTF-8"))
    print("sent mes")
