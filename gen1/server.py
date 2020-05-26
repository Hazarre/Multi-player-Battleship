from multiprocessing import Process
import socket
from time import sleep
import battleship
PORT = 8080
PORT2 = 8081
NUM_SHIPS = 3
BUFFER_SIZE = 1024

# This one unnecessarily  includes unnecessary game logic
def game_start(p1sock, p2sock):
    for i in range(NUM_SHIPS):
        p1sock.send("Please place your number %d ship: " % i)
        move = p1sock.recv(BUFFER_SIZE)
        print("received move %s from player 1" % move)
    p1sock.send("Wait for player 2 to place their ship.")
    
    for i in range(NUM_SHIPS):
        p2sock.send("Please place younumber %d ship: " % i)
        move = p2sock.recv(BUFFER_SIZE)
        print("player2 move %s" % move)
    GAME = True
    FIRSTROUND = True
    while GAME:
        if FIRSTROUND:
            p1sock.send("Please fire your missle (x,y) ")
            FIRSTROUND = False
        else: 
            p1sock.sendall("Your enemy fired a missle at %s, it's your turn to fire back. Enter the coordinate (x,y)" % move)
        move = p1sock.recv(BUFFER_SIZE)
        #updategame(move, player1)
        p2sock.sendall("Your enemy fired a missle at %s, it's your turn to fire back. Enter the coordinate (x,y)" % move)
        move = p2sock.recv(BUFFER_SIZE)
        #updategame(move, player2)


# Use this one 
def run_game(p1sock, p2sock):
    g = battleship.Game()
    while True:
        send_messages_to_player1()
        p1_move = p1sock.recv(BUFFER_SIZE)
        print("received move %s from player 1" % p1_move)
        p1_move = parse_move(p1_move)
        g.p1Input(p1_move)
        send_messages_to_player1()

        send_messages_to_player2()
        p2_move = p2sock.recv(BUFFER_SIZE)
        print("received move %s from player 1" % p2_move)
        p2_move = parse_move(p2_move)
        g.p2Input(p2_move)
        send_messages_to_player2()


def send_messages_to_player1():
    global g, p1sock
    o1 = g.broadcastP1()
    for msg in o1:
        p1sock.sendall(msg)

def send_messages_to_player2():
    global g, p2sock
    o2 = g.broadcastP2()
    for msg in o2:
        p2sock.sendall(msg)


def parse_move(move):
    newMove = []
    move = move.split()
    newMove.append([int(move[0]), int(move[1])])
    if len(move)==3:
        newMove.append(battleship.ORIENTATION[move[2]])
    return newMove

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
