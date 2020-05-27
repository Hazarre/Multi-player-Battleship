import socket
import  battleship
flags = battleship.FLAGS
flags = {v: k for k, v in flags.items()}
PORT = 8080
BUFFER_SIZE = 6


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('3.95.242.45', PORT))
PLAY_GAME = True
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

while PLAY_GAME:
    print("recving")
    mes = s.recv(BUFFER_SIZE).decode("UTF-8")
    move = input(mes)
    s.sendall(move.encode("UTF-8"))
    print("sent mes")


