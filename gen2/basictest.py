from battleship import*
from common import* 
from time import sleep

# Test 1: set game to N 
BOARD_SIZE, NUM_SHIPS, SHIP_SIZE  = 4, 1, 2

g = Game()

#ship placemet
print("player1 makes move")
g.update_game("0 0 h", 0)
print("player1 result:", g.players[0].out)
print("player2 result:", g.players[1].out)
print()

print("player2 makes move")
g.update_game("0 0 v",1)
print("player1 result:", g.players[0].out)
print("player2 result:", g.players[1].out)
print()


# fire 
print("player1 makes move")
g.update_game("0 0",0)
print("player1 result:", g.players[0].out)
print("player2 result:", g.players[1].out)
print()

print("player2 makes move")
g.update_game("0 0",1)
print("player1 result:", g.players[0].out)
print("player2 result:", g.players[1].out)
print()


print("player1 makes move")
g.update_game("0 1",0)
print("player1 result:", g.players[0].out)
print("player2 result:", g.players[1].out)
print()

print("player2 makes move")
g.update_game("0 1",1)
print("player1 result:", g.players[0].out)
print("player2 result:", g.players[1].out)
print()
