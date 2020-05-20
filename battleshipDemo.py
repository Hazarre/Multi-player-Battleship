import  battleship

game = battleship.Game()

game.NUM_SHIPS = 1
game.reset()

game.p1Input([(2,2),'V'])
input("")
game.p2Input([(3,5),'H'])
input("")
game.p1Input((2,5))
input("")
game.p2Input((2,2))
input("")
game.p1Input((3,5))
game.p2Input((2,3))
game.p1Input((7,8))
game.p2Input((2,4))