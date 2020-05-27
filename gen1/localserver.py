

def local_to_socket_msg(lm): 
	sm = ''
	for i in lm:
		sm = sm + str(i) + " "
	return sm

def socket_to_local_msg(sm):
	lm = []
	for i in sm.split(): 
		lm.append(int(i))
	return lm


game = Game()


game.NUM_SHIPS = 1
game.reset()

m1 = game.broadcastP1()
m2 = game.broadcastP2()
for m in m1: 
	print(m)
	sm = local_to_socket_msg(m)
	print(sm , type(sm))
	lm = socket_to_local_msg(sm)
	print(lm , type(lm))

game.p1Input([2,2,True])
m1 = game.broadcastP1()
m2 = game.broadcastP2()

input("")

game.p2Input([3,5,False])
m1 = game.broadcastP1()
m2 = game.broadcastP2()

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


