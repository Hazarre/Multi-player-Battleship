import  battleship

game = battleship.Game()

END = False
game.NUM_SHIPS = 1
game.reset()

while not END:
    # player plays from command line:
    move = input('Player 1 please enter move x y orientation:')
    move = move.split()

    #send move to server as an array/string 
    #send(move)

    # the player process its move locally, and the server updates another copy remotely 
    game.p1Input([(int(move[0]), int(move[1])), move[2]])

    # or player 1 can process the game state and send it to server (which I don't recommend)
    # because it takes way lot more internet traffic
    print("this is the updated game board. \n")
    gameboard1 = game.p1Board 
    print(gameboard1)   
    print("or I can send this board over to the server. \n")

    # receives move from player2 => should become to wait for an array containing the result of 
    # recv(result_of_my_move) 
    # recv(move_player2)
    # update player2's hidden board on player1's end
   
   

    