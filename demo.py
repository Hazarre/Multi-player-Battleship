import  battleship
flags = battleship.FLAGS
flags = {v: k for k, v in flags.items()}


def local_to_socket_msg(lm): 
    sm = ''
    for i in lm:
        sm = sm + str(i) + " "
    return sm

def socket_to_local_msg(sm):
    lm = []
    for i in sm.split():
        lm.append(int(i))
    lm.pop(0)
    return lm

def parse_out(m):
    for msg in m:
        if msg[0] == 0: #flag
            msg[1] = flags[msg[1]]
        if msg[0] == 1:
            if msg[1]:
                msg[1] = 'you hit target on your previous shot '
            else:
                msg[1] = 'you missed on your previous shot'
        if msg[0] == 2:
           msg[0] = 'you are under attack at ' + str((msg[1],msg[2]))
    return m


print("Example of server parsing message parsing input from client for game methods calling")
print(socket_to_local_msg("1 1 5"))
print(socket_to_local_msg("2 1 1 1"))
print("end of packets")


game = battleship.Game()
game.NUM_SHIPS = 1
game.reset()
game.p1Input([2,2,1]) # places ship at starting at (2,2) with vertical orientation

print("Example of server parsing message from game result to send to client")
for i in game.p1Out: 
    print(local_to_socket_msg(i))
for i in game.p2Out:
    print(local_to_socket_msg(i))


print("Demo of game")
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

