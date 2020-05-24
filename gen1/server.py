from multiprocessing import Process
import socket
from time import sleep
PORT = 8080
PORT2 = 8081
NUM_SHIPS = 3
BUFFER_SIZE = 1024


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), PORT))
s.listen(50)


def game_start(p1sock, p2sock):
    for i in range(NUM_SHIPS):
        p1sock.send("Please place your number %d ship: " % i)
        move = p1sock.recv(BUFFER_SIZE)
	print("recieved move %s from player 1" % move)

    for i in range(NUM_SHIPS):
        p2sock.send("Please place younumber %d ship: " % i)
        move = p2sock.recv(BUFFER_SIZE)
        print("player2 move %s" % move)
   
 while
print("waiting")
while True:
    try:
        p1sock, p1addr = s.accept()
        print("connected to player 1")
        # p2sock, p2addr = s.accept()
        # print("connected to 2 client's")
        p = Process(target=game_start, args=(p1sock,0 ))
        p.start()
    except socket.error:
        break
        sleep(10)
print('got a socket error')
s.close()
