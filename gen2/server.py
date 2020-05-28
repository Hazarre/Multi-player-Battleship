from multiprocessing import Process
import socket
from time import sleep
from battleship import *
import cryptoWorkspace as cw
PORT = 8080
BUFFER_SIZE = 1024


class Session:
    def __init__(self, p1sock, p2sock, p1key,p2key,privkey,pubkey):
        self.psockets = [p1sock,p2sock]
        self.g=Game()
        self.priv_key,self.pub_key = privkey,pubkey # RSA keys: use pub for encrypting and priv for decrypting
        self.pkeys = [p1key,p2key]

    def recieve(self, bufsize):
        msg = s.recv(bufsize)
        msg = cw.decrypt(msg, self.priv_key).decode("utf-8")
        return msg

    def update_state(self, id, state):
        msg = MESSAGE_ENCODING[state]
        self.psockets[id].sendall(cw.encrypt(msg.encode("utf-8"),self.pkeys[id]))

    def start_game(self):
        forward = False
        while True:
            for id in range(2):
                # player id's turn
                print('start %d' %id)
                print('state %d' %self.g.state)
                self.update_state(id,'my_turn')
                if self.g.state == STATE["fire"]:
                    forward = True
                print('getting player%ds move' %(id+1))
                move = self.psockets[id].recv(BUFFER_SIZE).decode("utf-8") 
                print("recieved move %s from player %d" % (move, id+1))
                self.g.update_game(move,id)
                if forward: # let enemy know where they got hit
                    print('fstart')
                    self.update_state((id+1)%2, 'under_fire')
                    print('fstart1')
                    self.psockets[(id+1)%2].sendall(move.encode("utf-8"))
                    print('fend')
                if self.g.state == STATE["gameover"]:
                    print("gameover")
                    self.update_state(id, 'you_win')
                    self.update_state((id+1)%2,'you_lost')
                    break
                print('before end')
                self.update_state(id, self.g.players[id].message)
                print('end')


def start_session(p1sock,p2sock):
    Session(p1sock,p2sock).start_game()


# multiprocess server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setblocking(True)
s.bind((socket.gethostname(), PORT))
s.listen(50)
print("waiting")
privkey,pubkey = cw.generate_keys()
while True:
    try:
        p1sock, p1addr = s.accept()
        p1sock.sendall(cw.serialize_key(pubkey))
        p1key = p1sock.recv(3).decode("utf-8")
        print("connected to player 1")
        p2sock, p2addr = s.accept()
        p2sock.sendall(cw.serialize_key(pubkey))
        p2key = p2sock.recv(3).decode("utf-8")
        print("connected to player 2")
        p = Process(target=start_session, args=(p1sock, p2sock,p1key,p2key,privkey,pubkey))
        p.start()
    except socket.error:
        print('got a socket error')
        sleep(10)
        break
s.close()
