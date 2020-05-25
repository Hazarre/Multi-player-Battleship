FLAGS = {'bad input': 0,
		 'wait your turn': 1,
		 'waiting for other player to place ships': 2,
		 'not a valid ship placement': 3,
		 'other player ready': 4,
		 'placed a ship': 5,
		 'repeated fire': 6,
		 'game over': 7,
		 'fire result': 8}
ORIENTATION = {'V': True, 'H': False}


class Game:
	BOARD_SIZE = 10
	NUM_SHIPS = 3
	#p1Board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
	p1Board =[]
	p2Board=[]
	#p2Board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
	turn = 1
	state = 'setup'
	p1Ships = NUM_SHIPS
	p2Ships = NUM_SHIPS
	p1Out = []
	p2Out = []

	def __init__(self):
		self.reset()

	def reset(self):
		self.p1Board = [[0] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
		self.p2Board = [[0] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
		self.turn = 1
		self.state = 'setup'
		self.p1Ships = self.NUM_SHIPS
		self.p2Ships = self.NUM_SHIPS
		self.p2Out = []

	def p1Input(self, input):
		if self.inputCheck(input):
			if self.state == 'setup':
				if self.p1Ships > 0:
					startCoord = input[0]
					orientation = input[1]
					if self.validShip(input, 1):
						# place a ship
						if orientation == 'V':
							for i in range(3):
								self.p1Board[startCoord[1] + i][startCoord[0]] = 1
						else:
							for i in range(3):
								self.p1Board[startCoord[1]][startCoord[0] + i] = 1
						self.p1Ships -= 1
						self.p1Out.append([FLAGS['placed a ship'], self.p1Ships])
					else:
						self.p1Out.append([FLAGS['not a valid ship placement'], -1])

				# goto play state
				if self.p1Ships == 0 and self.p2Ships == 0:
					self.state = 'play'
				elif self.p1Ships == 0:
					self.p1Out.append([FLAGS['waiting for other player to place ships'], -1])
					self.p2Out.append([FLAGS['other player ready'], -1])

			elif self.state == 'play':
				if self.turn == 1:
					self.fireP1(input)
					self.turn = 2
					if self.checkWon(1): return
				else:
					self.p1Out.append([FLAGS['wait your turn'], -1])
		else:
			self.p1Out.append([FLAGS['bad input'],-1])

	def p2Input(self, input):
		if self.inputCheck(input):
			if self.state == 'setup':
				if self.p2Ships > 0:
					startCoord = input[0]
					orientation = input[1]
					if self.validShip(input, 2):
						# place a ship
						if orientation == 'V':
							for i in range(3):
								self.p2Board[startCoord[1] + i][startCoord[0]] = 1
						else:
							for i in range(3):
								self.p2Board[startCoord[1]][startCoord[0] + i] = 1
						self.p2Ships -= 1
						self.p2Out.append([FLAGS['placed a ship'], self.p2Ships])
					else:
						self.p2Out.append([FLAGS['not a valid ship placement'], -1])
				# goto play state
				if self.p1Ships == 0 and self.p2Ships == 0:
					self.state = 'play'
				elif self.p2Ships == 0:
					self.p2Out.append([FLAGS['waiting for other player to place ships'], -1])
					self.p1Out.append([FLAGS['other player ready'], -1])

			elif self.state == 'play':
				if self.turn == 2:
					self.fireP2(input)
					self.turn = 1
					if self.checkWon(2): return
				else:
					self.p1Out.append([FLAGS['wait your turn'], -1])
		else:
			self.p2Out.append([FLAGS['bad input'],-1])

	# this method checks if the input is of valid format for the game state
	# TODO update
	def inputCheck(self, input):
		if self.state == 'setup':
			return isinstance(input, list) and len(input) == 2 and isinstance(input[1], str) and \
				   (isinstance(input[0], list) or isinstance(input[0], tuple)) and len(input[0]) == 2 and \
				   isinstance(input[0][0], int) and isinstance(input[0][1], int)
		elif self.state == 'play':
			return (isinstance(input, list) or isinstance(input, tuple)) and len(input) == 2 and isinstance(input[0],
																											int) and isinstance(
				input[1], int)
		return False

	# check if the placement is valid on the board
	def validShip(self, input, player):
		if player == 1:
			board = self.p1Board
		else:
			board = self.p2Board
		startCoord = input[0]
		orientation = input[1]

		if orientation == 'V':
			if startCoord[1] > self.BOARD_SIZE - 3: return False
			for y in range(3):
				if board[startCoord[1] + y][startCoord[0]] == 1: return False
		else:
			if startCoord[0] > self.BOARD_SIZE - 3: return False
			for x in range(3):
				if board[startCoord[1]][startCoord[0] + x] == 1: return False
		return True

	# updates P2's board with an attack at coords
	def fireP1(self, coords):
		x = self.p2Board[coords[1]][coords[0]]
		if x == 0:  # hit water
			self.p2Board[coords[1]][coords[0]] = -1
			self.p1Out.append([FLAGS['fire result'], False])
			self.p2Out.append([False, coords[0], coords[1]])
			return False
		if x == 1:  # hit ship
			self.p2Board[coords[1]][coords[0]] = 2
			self.p1Out.append([FLAGS['fire result'], True])
			self.p2Out.append([True, coords[0], coords[1]])
			return True
		else:
			self.p1Out.append([FLAGS['repeated fire'],-1])

	# updates p1's board with an attack at coords
	def fireP2(self, coords):
		x = self.p1Board[coords[1]][coords[0]]
		if x == 0:  # hit water
			self.p1Board[coords[1]][coords[0]] = -1
			self.p2Out.append([FLAGS['fire result'], False])
			self.p1Out.append([False, coords[0], coords[1]])
			return False
		if x == 1:  # hit ship
			self.p1Board[coords[1]][coords[0]] = 2
			self.p2Out.append([FLAGS['fire result'], True])
			self.p1Out.append([True, coords[0], coords[1]])
			return True
		else:
			self.p2Out.append([FLAGS['repeated fire'],-1])

	# checks to see in player has won and, if so, broadcasts the win and resets the game
	def checkWon(self, player):
		if player == 1:
			board = self.p2Board
		else:  # player == 2
			board = self.p1Board
		numfloating = self.numFloating(board)
		if numfloating == 0:
			self.broadcastWin(player)
			self.reset()
			return True

	# send game over message to both players
	def broadcastWin(self, winner):
		self.p1Out.append([FLAGS['game over'],winner])
		self.p2Out.append([FLAGS['game over'],winner])

	# check if there is a message for P1
	def broadcastP1(self):
		m = self.p1Out
		self.p1Out = []
		return m

	# check if there is a message for P2
	def broadcastP2(self):
		m = self.p2Out
		self.p2Out = []
		return m

	def numFloating(self, board):
		num = 0
		for i in board:
			for j in i:
				if j == 1:
					num += 1
		return num

# g = Game()
# g.p1Input([(0,9),'V'])
# g.p1Input([(9,0),'H'])
# g.p1Input([(0,7),'V'])
# g.p1Input([(2,2),'V'])
# g.p1Input([(5,3),'H'])
# g.state = 'play'
# g.p2Board[1][1]=1
# g.p1Input([0,1])
# g.p1Input([1,1])
# g.turn=1
# g.p1Input([1,1])
