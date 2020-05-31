from multiprocessing import Process
import socket
from time import sleep
from battleship import *
from common import *

class Session:
    def __init__(self, p1sock, p2sock):
        self.psockets = [p1sock,p2sock]
        self.g=Game()

    def start_game(self):
        start_mes = MSG_TYPE['flag'] + " " + FLAGS["my turn"]
        self.psockets[0].sendall(start_mes.encode("utf-8"))

        while self.g.state != STATE["gameover"]:
            for id in range(2):
                # player id's turn
                print('player %ds turn' % (id+1))
                # get move from client 
                move = self.psockets[id].recv(BUFFER_SIZE).decode("utf-8") 
                self.g.update_game(move,id)
                #update results to client
                ply_mes = self.g.players[id].out
                opp_mes = self.g.players[(id+1)%2].out
                self.psockets[id].sendall(ply_mes.encode("utf-8"))
                self.psockets[(id+1)%2].sendall(opp_mes.encode("utf-8"))
            
def start_session(p1sock,p2sock):
    Session(p1sock,p2sock).start_game()

# multiprocess server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setblocking(True)
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
