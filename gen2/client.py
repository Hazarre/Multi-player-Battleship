import socket
from battleship import* 
PORT = 8080
BUFFER_SIZE = 1024
PLAY_GAME = True

def socket_to_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('54.81.106.48', PORT))
    return s

g = Game().set_identity("client")
id = 0 
s = socket_to_server()
print("connected to server")

while PLAY_GAME:
    mess = s.recv(BUFFER_SIZE)
    if mess == MESSAGE_ENCODING['you_loss']:
        print("You Lost")
    elif mess == MESSAGE_ENCODING['you_win']:
        print("You won")
    elif mess == MESSAGE_ENCODING['my_turn']:
        move = g.get_input_prompt()
        g.update_game(move,id)
        s.sendall(move)
        mess = MESSAGE_ENCODING['waiting']
        

        
    
