import battleship


def messages_to_player1(g):
    msg = g.broadcastP1()
    if len(msg)==0:
        msg="no message"
    return msg

def messages_to_player2(g):
    msg = g.broadcastP2()
    if len(msg)==0:
        msg="no message"
    return msg

def parse_move(move):
    newMove = []
    move = move.split()
    newMove.append((int(move[0]), int(move[1])))
    if len(move)==3:
        newMove.append(battleship.ORIENTATION[move[2]])
    return newMove

g = battleship.Game()

while True:
    p1_move = input("Player 1 please enter move")
    print("recieved move %s from player 1" % p1_move)
    p1_move = parse_move(p1_move)
    g.p1Input(p1_move)
    print("move processed with result %s" % messages_to_player1(g))

    p2_move = input("Player 2 please enter move")
    print("recieved move %s from player 2" % p2_move)
    p2_move = parse_move(p2_move)
    g.p2Input(p2_move)
    print("move processed with result %s" % messages_to_player2(g))

 


