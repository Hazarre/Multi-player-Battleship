from multiprocessing import Process
import socket
from time import sleep
from battleship import *
PORT = 8080
BUFFER_SIZE = 1024


class Session:
    def __init__(self, p1sock, p2sock):
        self.psockets = [p1sock,p2sock]
        self.g=Game()
    def update_state(self, id, state):
        self.psockets[id].sendall(MESSAGE_ENCODING[state])
    def start_game(self):
        while True:
            for id in range(2):
                # player id's turn
                self.update_state(id,'my_turn')
                move = self.psockets[id].recv(BUFFER_SIZE)
                print("recieved move %s from player %d" % (move, id+1))
                self.g.update_game(move,id)
                if self.g.state == STATE["gameover"]:
                    self.update_state(id, 'you_win')
                    self.update_state((id+1)%2,'you_lost')
                self.update_state(id, self.g.players[id].message)

def start_session(p1sock,p2sock):
    Session(p1sock,p2sock).start_game()


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
        p = Process(target=start_session, args=(p1sock, p2sock))
        p.start()
    except socket.error:
        print('got a socket error')
        sleep(10)
        break
s.close()
