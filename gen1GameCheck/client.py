# This client code is written for testing purposes on the server
# Not the full client

import socket
import  battleship
flags = battleship.FLAGS
flags = {v: k for k, v in flags.items()}
PORT = 8080
BUFFER_SIZE = 6

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('3.95.242.45', PORT))
PLAY_GAME = True


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

while PLAY_GAME:
    print("recving")
    mes = s.recv(BUFFER_SIZE).decode("UTF-8")
    move = input(mes)
    s.sendall(move.encode("UTF-8"))
    print("sent mes")


