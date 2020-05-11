import numpy as np


class Game:
	BOARD_SIZE = 10
	NUM_SHIPS = 3
	p1Board = np.zeros((BOARD_SIZE, BOARD_SIZE))
	p2Board = np.zeros((BOARD_SIZE, BOARD_SIZE))
	turn = 1
	state = 'setup'
	p1Ships = NUM_SHIPS
	p2Ships = NUM_SHIPS


	def __init__(self):
		self.reset()


	def reset(self):
		self.p1Board = np.zeros((self.BOARD_SIZE, self.BOARD_SIZE))
		self.p2Board = np.zeros((self.BOARD_SIZE, self.BOARD_SIZE))
		self.turn = 1
		self.state = 'setup'


	def p1Input(self,input):
		if self.inputCheck(input):
			if self.state == 'setup':
				if self.p1Ships>0:
					startCoord = input[0]
					orientation = input[1]
					if self.validShip(input,1):
						#place a ship
						if orientation == 'V':
							for i in range(3):
								self.p1Board[startCoord[1]+i][startCoord[0]] = 1
						else:
							for i in range(3):
								self.p1Board[startCoord[1]][startCoord[0]+i] = 1
						self.p1Ships-=1
						self.broadcastP1("placed a ship. "+str(self.p1Ships)+" left")
					else:
						self.broadcastP1("not a valid ship placement")
					self.broadcastBoards(1)

				#goto play state
				if self.p1Ships==0 and self.p2Ships==0:
					self.state = 'play'
				elif self.p1Ships==0:
					self.broadcastP1("waiting for P2 to place ships")
					self.broadcastP2("P1 ready")

			elif self.state == 'play':
				if self.turn == 1:
					self.fireP1(input)
					self.turn = 2
					if self.checkWon(1): return
					self.broadcastBoards(1)
				else:
					self.broadcastP1("wait your turn")
		else:
			self.broadcastP1("bad input. Try again")


	def p2Input(self,input):
		if self.inputCheck(input):
			if self.state == 'setup':
				if self.p2Ships>0:
					startCoord = input[0]
					orientation = input[1]
					if self.validShip(input,2):
						# place a ship
						if orientation == 'V':
							for i in range(3):
								self.p2Board[startCoord[1]+i][startCoord[0]] = 1
						else:
							for i in range(3):
								self.p2Board[startCoord[1]][startCoord[0]+i] = 1
						self.p2Ships-=1
						self.broadcastP2("placed a ship. "+str(self.p2Ships)+" left")
					else:
						self.broadcastP2("not a valid ship placement")
					self.broadcastBoards(2)
				#goto play state
				if self.p1Ships==0 and self.p2Ships==0:
					self.state = 'play'
				elif self.p2Ships==0:
					self.broadcastP2("waiting for P1 to place ships")
					self.broadcastP1("P2 ready")

			elif self.state == 'play':
				if self.turn == 2:
					self.fireP2(input)
					self.turn = 1
					if self.checkWon(2): return
					self.broadcastBoards(2)
				else:
					self.broadcastP1("wait your turn")
		else:
			self.broadcastP1("bad input. Try again")


	# this method checks if the input is of valid format for the game state
	def inputCheck(self,input):
		if self.state == 'setup':
			return isinstance(input,list) and len(input)==2 and isinstance(input[1],str) and \
				   (isinstance(input[0],list) or isinstance(input[0],tuple)) and len(input[0])==2 and\
				   isinstance(input[0][0],int) and isinstance(input[0][1],int)
		elif self.state == 'play':
			return (isinstance(input,list) or isinstance(input,tuple)) and len(input)==2 and isinstance(input[0],int) \
				   and isinstance(input[1],int)
		return False


	# check if the placement is valid on the board
	def validShip(self,input,player):
		if player ==1:
			board = self.p1Board
		else:
			board = self.p2Board
		startCoord = input[0]
		orientation = input[1]

		if orientation == 'V':
			if startCoord[1]>self.BOARD_SIZE - 3: return False
			for y in range(3):
				if board[startCoord[1]+y][startCoord[0]]==1:return False
		else:
			if startCoord[0] > self.BOARD_SIZE - 3: return False
			for x in range(3):
				if board[startCoord[1]][startCoord[0]+x]==1:return False
		return True


	# updates P2's board with an attack at coords
	def fireP1(self,coords):
		x = self.p2Board[coords[1]][coords[0]]
		if x==0: #hit water
			self.p2Board[coords[1]][coords[0]] = -1
			self.broadcastP1("miss")
			return False
		if x ==1: #hit ship
			self.p2Board[coords[1]][coords[0]] = 2
			self.broadcastP1("hit")
			return True
		else:
			self.broadcastP1("repeated fire")

	# updates p1's board with an attack at coords
	def fireP2(self,coords):
		x = self.p1Board[coords[1]][coords[0]]
		if x==0: #hit water
			self.p1Board[coords[1]][coords[0]] = -1
			return False
		if x ==1: #hit ship
			self.p1Board[coords[1]][coords[0]] = 2
			return True
		else:
			self.broadcastP1("repeated fire")


	# checks to see in player has won and, if so, broadcasts the win and resets the game
	def checkWon(self,player):
		if player == 1:
			hit = np.where(self.p2Board == 1, 1,0)
		else: #player == 2
			hit = np.where(self.p1Board == 1, 1,0)
		numfloating = np.sum(np.sum(hit))
		if numfloating==0:
			self.broadcastWin(player)
			self.reset()
			return True


	#send game over message to both players
	def broadcastWin(self,winner):
		self.broadcastP1("winner is P"+str(winner)+"!")
		self.broadcastP2("winner is P" + str(winner) + "!")


	#send p1 a message
	def broadcastP1(self,msg):
		print("P1:",msg)


	#send P2 a message
	def broadcastP2(self,msg):
		print("P2:",msg)


	#send the appropriate boards to player
	def broadcastBoards(self,player):
		if player==1:
			print("P1 Board:")
			print(self.p1Board)
			print("hidden P2 Board:")
			print(np.where(self.p2Board==1,0,self.p2Board)) #hides un-hit ships
		else:
			print("P2 Board:")
			print(self.p2Board)
			print("hidden P1 Board:")
			print(np.where(self.p1Board == 1, 0, self.p1Board)) #hides un-hit ships

g = Game()
g.p1Input([(0,9),'V'])
g.p1Input([(9,0),'H'])
g.p1Input([(0,7),'V'])
g.p1Input([(2,2),'V'])
g.p1Input([(5,3),'H'])
g.state = 'play'
g.p2Board[1][1]=1
g.p1Input([0,1])
g.p1Input([1,1])
g.turn=1
g.p1Input([1,1])


