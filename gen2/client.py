import socket
from battleship import* 
PORT = 8080
BUFFER_SIZE = 1024
PLAY_GAME = True

def socket_to_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect(('54.81.106.48', PORT))
    return s

g = Game()
g.set_identity("client")


id = 0 
e_id = 1 # enemy's id
s = socket_to_server()
print("connected to server")


while PLAY_GAME:
    # add input error/placement success in both client and server.py, include with case my_turn
    # add case "waiting"
    mess = s.recv(BUFFER_SIZE).decode("utf-8") 
    print("CURRENT STATE %s" % MESSAGE_DECODING[mess])
    if mess == MESSAGE_ENCODING['target_miss']:
        move = g.parse_input(move)
        print("final",move,type(move))
        g.players[id].enemy_board[move['x']][move['y']] = STATUS['miss']
        g.players[id].visualize()
    elif mess == MESSAGE_ENCODING['target_hit']:
        move = g.parse_input(move)
        print("final",move,type(move))
        g.players[id].enemy_board[move['x']][move['y']] = STATUS['hit']
        g.players[id].visualize()
    elif mess == MESSAGE_ENCODING['under_fire']:
        mess = s.recv(BUFFER_SIZE).decode("utf-8")
        g.update_game(move,e_id)
    elif mess == MESSAGE_ENCODING['you_win']:
        print("You won")
    elif mess == MESSAGE_ENCODING['you_loss']:
        print("YOu loss")
    elif mess == MESSAGE_ENCODING['my_turn']:
        move = g.get_input_prompt()

        g.update_game(move,id)
        print(move,type(move))
        s.sendall(move.encode("utf-8"))
        mess = MESSAGE_ENCODING['waiting']
    
s.close()