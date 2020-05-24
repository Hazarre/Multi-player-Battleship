from multiprocessing import Process
import socket
from time import sleep
PORT = 8080
PORT2 = 8081
NUM_SHIPS = 3
BUFFER_SIZE = 1024


def game_start(p1sock, p2sock):
    for i in range(NUM_SHIPS):
        p1sock.send("Please place your number %d ship: " % i)
        move = p1sock.recv(BUFFER_SIZE)
        print("recieved move %s from player 1" % move)
    p1sock.send("Wait for player 2 to place their ship.")
    
    for i in range(NUM_SHIPS):
        p2sock.send("Please place younumber %d ship: " % i)
        move = p2sock.recv(BUFFER_SIZE)
        print("player2 move %s" % move)
    
    GAME = True
    ROUND = 0 
    while GAME:
        if round == 0:
            p1sock.send("Please fire your missle (x,y) ")
        else: 
            p1sock.sendall("Your enemy fired a missle at %s, it's your turn to fire back. Enter the coordinate (x,y)" % move)
        move = p1sock.recv(BUFFER_SIZE)
        #updategame(move, player1)
        p2sock.sendall("Your enemy fired a missle at %s, it's your turn to fire back. Enter the coordinate (x,y)" % move)
        move = p2sock.recv(BUFFER_SIZE)
        #updategame(move, player2)
       

   

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), PORT))
s.listen(50)
print("waiting")
while True:
    try:
        p1sock, p1addr = s.accept()
        print("connected to player 1")
        p2sock, p2addr = s.accept()
        print("connected to player 2")
        p = Process(target=game_start, args=(p1sock, p2sock))
        p.start()
    except socket.error:
        print('got a socket error')
        sleep(10)
        break
s.close()