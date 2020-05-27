import  battleship
flags = battleship.FLAGS
flags = {v: k for k, v in flags.items()}


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


game = battleship.Game()

game.NUM_SHIPS = 1
game.reset()
print(game.broadcastP1())
print(game.broadcastP2())

game.p1Input([2,2,1])
print('P1:',parse_out(game.broadcastP1()))
print('P2:',parse_out(game.broadcastP2()))
input("")

game.p2Input([3,5,0])
print('P1:',parse_out(game.broadcastP1()))
print('P2:',parse_out(game.broadcastP2()))
input("")

game.p1Input([2,5])
print('P1:',parse_out(game.broadcastP1()))
print('P2:',parse_out(game.broadcastP2()))
input("")

game.p2Input([2,2])
print('P1:',parse_out(game.broadcastP1()))
print('P2:',parse_out(game.broadcastP2()))
input("")

game.p1Input([3,5])
print('P1:',parse_out(game.broadcastP1()))
print('P2:',parse_out(game.broadcastP2()))
print('')

game.p2Input([2,3])
print('P1:',parse_out(game.broadcastP1()))
print('P2:',parse_out(game.broadcastP2()))
print('')

game.p1Input([7,8])
print('P1:',parse_out(game.broadcastP1()))
print('P2:',parse_out(game.broadcastP2()))
print('')

game.p2Input([2,4])
print('P1:',parse_out(game.broadcastP1()))
print('P2:',parse_out(game.broadcastP2()))
print('')


