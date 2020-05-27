from multiprocessing import Process
import socket
from time import sleep
import battleship
PORT = 8080
NUM_SHIPS = 3
BUFFER_SIZE = 6

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
        send_messages_to_player1(g,p1sock)
        p1_move = p1sock.recv(BUFFER_SIZE).decode("UTF-8")
        print("recieved move %s from player 1" % p1_move)
        g.p1Input(socket_to_local_msg(p1_move))
        send_messages_to_player1(g,p1sock)
        print('P1:',parse_out(g.broadcastP1()))
        print('P2:',parse_out(g.broadcastP2()))

        send_messages_to_player2(g,p2sock)
        p2_move = p2sock.recv(BUFFER_SIZE).decode("UTF-8")
        print("recieved move %s from player 2" % p2_move)
        g.p1Input(socket_to_local_msg(p1_move))
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
   for lm in g.broadcastP1():
        sm = local_to_socket_msg(lm)
        p1sock.sendall(sm.encode("UTF-8"))

def send_messages_to_player2(g,p2sock):
    for lm in g.broadcastP2():
        sm = local_to_socket_msg(lm)
        p2sock.sendall(sm.encode("UTF-8"))
    p2sock.sendall(sm.encode("UTF-8"))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
