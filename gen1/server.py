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

# used for testing server
# def parse_out(m):
#     for msg in m:
#         if msg[0] == 0: #flag
#             msg[1] = flags[msg[1]]
#         if msg[0] == 1:
#             if msg[1]:
#                 msg[1] = 'you hit target on your previous shot '
#             else:
#                 msg[1] = 'you missed on your previous shot'
#         if msg[0] == 2:
#            msg[0] = 'you are under attack at ' + str((msg[1],msg[2]))
#     return m

# Use this one 
def run_game(p1sock, p2sock):
    g = battleship.Game()
    g.NUM_SHIPS = 1
    g.reset()
    while True:
        send_messages_to_player1(g,p1sock)
        # print("waiting for player1\n")
        p1_move = p1sock.recv(BUFFER_SIZE).decode("UTF-8")
        # print("recieved move %s from player 1\n" % p1_move)
        g.p1Input(socket_to_local_msg(p1_move))
        send_messages_to_player1(g,p1sock)
        # print('P1:',parse_out(g.p1Out))
        # print('P2:',parse_out(g.p2Out))

        send_messages_to_player2(g,p2sock)
        # print("waiting for player2\n")
        p2_move = p2sock.recv(BUFFER_SIZE).decode("UTF-8")
        # print("recieved move %s from player 2\n" % p2_move)
        g.p2Input(socket_to_local_msg(p2_move))
        send_messages_to_player2(g,p1sock)
        # print('P1:',parse_out(g.p1Out))
        # print('P2:',parse_out(g.p2Out))

def local_to_socket_msg(lm): 
    # convert message game ouput -> bytestring for socket
    sm = ''
    for i in lm:
        sm = sm + str(i) + " "
    return sm

def socket_to_local_msg(sm):
    # convert message bytestring from socket-> game input (list of ints)
    lm = []
    for i in sm.split():
        lm.append(int(i))
    lm.pop(0)
    return lm

def send_messages_to_player1(g,p1sock):
    # flush out all p1Out to client player1
    mess = g.broadcastP1()
    if len(mess)==0:
        print("no message")
        p1sock.sendall("1 -1".encode("UTF-8"))
    for lm in mess:
        sm = local_to_socket_msg(lm)
        p1sock.sendall(sm.encode("UTF-8"))

def send_messages_to_player2(g,p2sock):
    # flush out all p2Out to client player2
    mess = g.broadcastP2()
    if len(mess)==0:
        print("no message")
        p2sock.sendall("1 -1".encode("UTF-8"))
    for lm in mess:
        sm = local_to_socket_msg(lm)
        p2sock.sendall(sm.encode("UTF-8"))


# multiprocess server 
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