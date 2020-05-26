# game meta data
client = True

STATUS = {  'water': 0,
    'ship': 1,
            'miss':2,
            'hit':3}

STATE ={'setup':0,      # possible game states
        'fire':1,
        'gameover':2,
         }


MESSAGE_DECODING = ['my_turn','waiting','input_error','placement_success','target_hit','target_miss','you_loss','you_win']
MESSAGE_ENCODING = {}
for i in range(len(MESSAGE_DECODING)):
    MESSAGE_ENCODING[MESSAGE_DECODING[i]] = str(i) 

ORIENTATION = {'V': 1, 'H': 0, 'v': 1, 'h':0}
BOARD_SIZE, NUM_SHIPS, SHIP_SIZE  = 10 , 3, 3

class Player:
    def __init__(self):
        self.my_board =  [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.enemy_board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.nships_to_place = NUM_SHIPS
        self.nships_alive = NUM_SHIPS
        self.nspots_ontarget = 0

    def placement_check(self, x, y, o):
        is_valid = True
        if o == ORIENTATION['V']:
            for i in range(SHIP_SIZE):
                is_valid = is_valid and (self.my_board[x][y+i] == STATUS['water'])
        else:
            for i in range(SHIP_SIZE):
                is_valid = is_valid and (self.my_board[x+i][y] == STATUS['water'])
        print(is_valid)
        return is_valid

    def place_ship(self, x, y, o):
        if self.placement_check(x,y,o):
            self.nships_to_place-=1
            if o == ORIENTATION['V']:
                for i in range(SHIP_SIZE):
                    self.my_board[x][y+i] = STATUS['ship']
            else:
                for i in range(SHIP_SIZE):
                    self.my_board[x+i][y] = STATUS['ship']
            return True
        return False 
    
    def take_missle(self,x,y):
        if self.my_board[x][y]==STATUS['ship']:
            self.my_board[x][y] = STATUS["hit"]
            return STATUS["hit"]
        self.my_board[x][y] = STATUS["miss"]
        return STATUS["miss"]
    
    def visualize(self):
        print("My Game Board: ")
        for j in range(BOARD_SIZE):
            for i in range(BOARD_SIZE):
                print(self.my_board[i][j], end = " ")
            print()
        print("\nEnemy's Board:")
        for j in range(BOARD_SIZE):
            for i in range(BOARD_SIZE):
                print(self.enemy_board[i][j], end = " ")
            print()
        print("\n\n\n")

class Game:
    state = STATE["setup"] # either SETUP or FIRE
    def __init__(self):
        self.reset()

    def reset(self):
        self.p1 = Player()
        self.p2 = Player()
        self.players = [self.p1, self.p2]
        self.state = STATE["setup"]
        self.identity = "server" # or server
 
    def set_identity(self, identity):
        self.identity = identity
        if self.identity is not "server": # client
            self.p2.nships_to_place = 0

    def get_input_prompt(self):
        if self.state == STATE["setup"]:
            mes = "Please place your ship with its upper left coordinate (0<x,y<10) and orientation(V or H) x y o: \n" 
        elif self.state == STATE["fire"]:
            mes = "Please fire your missle towards x y: \n" 
        elif self.state == STATE["gameover"]:
            mes = "GAMEOVER\n"
        return input(mes)
        
    def parse_input(self,str_in): # str_inshould be str()
        str_in = str_in.split()
        if (len(str_in) < 3 and self.state == STATE["setup"]) or len(str_in) < 2:
            print("input error")
        move = {}
        move['x'] = int(str_in[0])
        move['y'] = int(str_in[1])
        if len(str_in) >= 3:
            move['o'] = ORIENTATION[str_in[2]]
        return move
    
    # this method checks if the input is of valid format for the game state
    def move_check(self, move):
        x_max, y_max = BOARD_SIZE, BOARD_SIZE
        if self.state == STATE["setup"]:
            if move['o'] == ORIENTATION['V']:
                y_max -= SHIP_SIZE
            else:
                x_max -= SHIP_SIZE
        return move['x'] <= x_max and move['x'] >= 0 and move['y'] <= y_max and move['y'] >= 0

    def update_game(self, str_in, id):
        if self.state ==STATE["gameover"]:
            print("You Lost")
            return
        print("player %d" % id)
        # process move specified by input string str_in and changes game state
        move = self.parse_input(str_in)
        # player id is 0 for player1 and 1 for player2
        p, o = self.players[id], self.players[(id+1)%2]  #player with id
        if not self.move_check(move):
            p.message = "input_error"
            return
        # place ship   
        if p.nships_to_place > 0:
            p.place_ship(move["x"], move['y'], move['o'])
            p.message = "placement_success"
            if o.nships_to_place == 0 and p.nships_to_place==0:
                self.state = STATE["fire"]
        # fire missle at p2
        elif self.state == STATE["fire"]: 
            if self.missle_result(move["x"], move['y'], id) == STATUS["hit"]:
                p.nspots_ontarget += 1
                p.message = 'target_hit'
                if self.check_win(id):
                    p.message = "you_win"
                    self.state=STATE["gameover"]
            else:
                p.message = 'target_miss'
        if True:  #self.identity is not "server"
            p.visualize()
        return 


    def missle_result(self,x,y,id): # id is the player that fired the missle
        if self.identity is "server": # if the machine is the server
            result = self.players[(id+1)%2].take_missle(x,y) #
            self.players[id].enemy_board[x][y] = result
            return result
        else: 

            # send request to the server for response 
            pass

    def check_win(self, id):
        return self.players[id].nspots_ontarget == NUM_SHIPS*SHIP_SIZE

