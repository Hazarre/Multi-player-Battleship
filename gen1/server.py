import socket
PORT = 8080
PORT2 = 8081
NUM_SHIPS = 3
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), PORT))
s.listen(50)


def process_start(p1sock, p2sock):
    p1sock.send("You are player1")
    for i in range(NUM_SHIPS):
        p1sock.sendall("Please place your # %d ship: " % i)
        p1sock.recv(BUFFER_SIZE)

    p2sock.send("You are player2")
    for i in range(NUM_SHIPS):
        p2sock.send("Please place you ship:")

print("waiting")
while True:
    try:
        p1sock, p1addr = s.accept()
        print("connected to player 1")
        p2sock, p2addr = s.accept()
        print("connected to 2 client's")
        p = Process(target=Battleshipgame_start, args=(p1sock, p2sock))
        p.start()
    except socket.error:
        print('got a socket error')
    s.close()