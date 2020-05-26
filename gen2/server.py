from multiprocessing import Process
import socket
from time import sleep
from battleship import *
PORT = 8080
BUFFER_SIZE = 1024


def update_state(id, state):
    psockets[id].sendall(MESSAGE_ENCODING[state])

def game2p(p1sock, p2sock):
    g = Game()
    psockets = [p1sock,p2sock]
    while True:
        for id in range(2):
            # player id's turn
            update_state(id,'my_turn')
            move = psockets[id].recv(BUFFER_SIZE)
            print("recieved move %s from player %d" % (move, id+1))
            g.update_game(move,id)
            if g.state == STATE["gameover"]:
                update_state(id, 'you_win')
                update_state((id+1)%2,'you_lost')
            update_state(id, g.players[id].message)




# multiprocess server
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
        p = Process(target=game2p, args=(p1sock, p2sock))
        p.start()
    except socket.error:
        print('got a socket error')
        sleep(10)
        break
s.close()
