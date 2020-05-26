import socket
from battleship import* 
PORT = 8080
BUFFER_SIZE = 1024
PLAY_GAME = True

def socket_to_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(True)
    s.connect(('3.95.242.45', PORT))
    return s

g = Game()
g.set_identity("client")


id = 0 
e_id = 1 # enemy's id
s = socket_to_server()
print("connected to server")

mess = MESSAGE_ENCODING["waiting"]
while PLAY_GAME:
    # add input error/placement success in both client and server.py, include with case my_turn
    # add case "waiting"
    print("prev STATE %s %s" % (mess, MESSAGE_DECODING[int(mess)]))
    print("waiting for server")
    mess = s.recv(BUFFER_SIZE).decode("utf-8")
    print("CURRENT STATE %s %s" % (mess, MESSAGE_DECODING[int(mess)]))
    if mess == MESSAGE_ENCODING['under_fire']:
        move = s.recv(BUFFER_SIZE).decode("utf-8")
        print("recieved move %s under fire" %move)
        g.update_game(move,e_id)
        g.p1.visualize()
        mess = MESSAGE_ENCODING['my_turn']
        print("underfire done")
    elif mess == MESSAGE_ENCODING['you_win']:
        print("You won")
    elif mess == MESSAGE_ENCODING['you_loss']:
        print("YOu loss")
    elif mess == MESSAGE_ENCODING['my_turn']:
        print("my turn lll")
        move = g.get_input_prompt()
        s.sendall(move.encode("utf-8"))
        if g.state == STATE['fire']:
            mess = s.recv(BUFFER_SIZE).decode("utf-8") # hear from the server the result of the missle
            if mess == MESSAGE_ENCODING['target_hit']:
                print("recieved result mess %s under fire" % MESSAGE_DECODING[int(mess)])
                m = g.parse_input(move)
                g.players[id].enemy_board[m['x']][m['y']] = STATUS['ship']
        g.update_game(move,id)
        print(move,type(move))
        mess = MESSAGE_ENCODING['waiting']
    
s.close()