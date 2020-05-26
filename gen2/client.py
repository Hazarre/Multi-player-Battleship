import socket
from battleship import* 
PORT = 8080
BUFFER_SIZE = 1024
PLAY_GAME = True

def socket_to_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
    if mess == MESSAGE_ENCODING['target_miss']:
        move = parse_input(move)
        g.players[id].enemy_board[int(move[0])][int(move[1])] = STATUS['miss']
    elif mess == MESSAGE_ENCODING['target_hit']:
        move = parse_input(move)
        g.players[id].enemy_board[int(move[0])][int(move[1])] = STATUS['hit']
    elif mess == MESSAGE_ENCODING['under_fire']:
        mess = s.recv(BUFFER_SIZE).decode("utf-8")
        g.update_game(move,e_id)
    elif mess == MESSAGE_ENCODING['you_win']:
        print("You won")
    elif mess == MESSAGE_ENCODING['you_win']:

    elif mess == MESSAGE_ENCODING['my_turn']:
        move = g.get_input_prompt()
        g.update_game(move,id)
        s.sendall(move.encode("utf-8"))
        mess = MESSAGE_ENCODING['waiting']
        

        
    
