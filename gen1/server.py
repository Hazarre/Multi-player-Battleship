from multiprocessing import Process
import socket
from time import sleep
import battleship
import pdb
PORT = 8080
NUM_SHIPS = 3
BUFFER_SIZE = 6


flags = battleship.FLAGS
flags = {v: k for k, v in flags.items()}
def parse_out(m):
    for i in range(len(m)):
        msg = m[i]
        if len(msg) == 2:
            msg[0] = flags[msg[0]]
        elif len(msg) == 3:
            if msg[0]:
                msg = 'you were hit at '+str((msg[1],msg[2]))
            else:
                msg = 'op missed at '+str((msg[1],msg[2]))
        m[i] = msg
    return m

# Use this one 
def run_game(p1sock, p2sock):
    g = battleship.Game()
    g.NUM_SHIPS = 1
    g.reset()
    while True:
        print("before send p1 out")
        print(g.p1Out)
        send_messages_to_player1(g,p1sock)
        print("after send p1 out")
        print(g.p1Out)
        print("waiting for player1\n")
        p1_move = p1sock.recv(BUFFER_SIZE).decode("UTF-8")
        print("recieved move %s from player 1\n" % p1_move)
        print("move socket data type", type(p1_move))
        l_move1 = socket_to_local_msg(p1_move)
        print("move local data type", type(l_move1))
        print(type(l_move1[0]))
        print(l_move1)
        g.p1Input(l_move1)
        #pdb.set_trace()
        print("before send p1 out")
        print(g.p1Out)
        send_messages_to_player1(g,p1sock)
        print("after send p1 out")
        print(g.p1Out)
        print('P1:',parse_out(g.broadcastP1()))
        print('P2:',parse_out(g.broadcastP2()))

        send_messages_to_player2(g,p2sock)
        print("waiting for player2\n")
        p2_move = p2sock.recv(BUFFER_SIZE).decode("UTF-8")
        print("recieved move %s from player 2\n" % p2_move)
        print("move socket data type", type(p2_move))
        l_move2 = socket_to_local_msg(p2_move)
        print("move local data type", type(l_move2))
        print(l_move2)
        g.p1Input(l_move2)
        send_messages_to_player2(g,p1sock)
        print('P1:',parse_out(g.broadcastP1()))
        print('P2:',parse_out(g.broadcastP2()))

def local_to_socket_msg(lm): 
	sm = ''
	for i in lm:
		sm = sm + str(i) + " "
	return sm

def socket_to_local_msg(sm):
	lm = []
	for i in sm.split(): 
		lm.append(int(i))
	return lm

def send_messages_to_player1(g,p1sock):
    mess = g.p1Out
    if len(mess)==0:
        print("no message")
        p1sock.sendall("1 -1".encode("UTF-8"))
    for lm in mess:
        sm = local_to_socket_msg(lm)
        p1sock.sendall(sm.encode("UTF-8"))

def send_messages_to_player2(g,p2sock):
    mess = g.p2Out
    if len(mess)==0:
        print("no message")
        p2sock.sendall("1 -1".encode("UTF-8"))
    for lm in mess:
        sm = local_to_socket_msg(lm)
        p2sock.sendall(sm.encode("UTF-8"))
    


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setblocking(True)
s.bind((socket.gethostname(), PORT))
s.listen(50)
print("waiting for client")
while True:
    try:
        p1sock, p1addr = s.accept()
        print("connected to player 1")
        p2sock, p2addr = s.accept()
        print("connected to player 2")
        p = Process(target=run_game, args=(p1sock, p2sock))
        p.start()
    except socket.error:
        print('got a socket error')
        sleep(10)
        break
s.close()
