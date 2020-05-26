from multiprocessing import Process
import socket
from time import sleep
import battleship
PORT = 8080
PORT2 = 8081
NUM_SHIPS = 3
BUFFER_SIZE = 1024

# Use this one 
def run_game(p1sock, p2sock):
    g = battleship.Game()
    while True:
        send_messages_to_player1(g,p1sock)
        p1_move = p1sock.recv(BUFFER_SIZE)
        print("recieved move %s from player 1" % p1_move)
        p1_move = parse_move(p1_move)
        g.p1Input(p1_move)
        print("move processed")
        send_messages_to_player1(g,p1sock)

        print("sending message to player 2")
        send_messages_to_player1(g,p2sock)
        p2_move = p2sock.recv(BUFFER_SIZE)
        print("recieved move %s from player 2" % p2_move)
        p2_move = parse_move(p2_move)
        g.p2Input(p2_move)
        send_messages_to_player2(g,p2sock)


def send_messages_to_player1(g,p1sock):
    msg = g.broadcastP1()
    if len(msg)==0:
        msg="no message"
    p1sock.sendall(msg)

def send_messages_to_player2(g,p2sock):
    msg = g.broadcastP2()
    if len(msg)==0:
        msg="no message"
    p2sock.sendall(msg)


def parse_move(move):
    newMove = []
    move = move.split()
    newMove.append((int(move[0]), int(move[1])))
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
