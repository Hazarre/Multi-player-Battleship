#define BOARD_SIZE 10;
#define NUM_SHIPS 3;
#define TOTAL_HITS_TO_WIN

struct Game{
    char board[2][BOARD_SIZE][BOARD_SIZE] = {0};
    char hits[2];
};


	def reset(self):
		self.p1Board = np.zeros((self.BOARD_SIZE, self.BOARD_SIZE))
		self.p2Board = np.zeros((self.BOARD_SIZE, self.BOARD_SIZE))
		self.turn = 1
		self.state = 'setup'
		self.p1Ships = self.NUM_SHIPS
		self.p2Ships = self.NUM_SHIPS


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
						self.p1Out.append("placed a ship. "+str(self.p1Ships)+" left")
					else:
						self.p1Out.append("not a valid ship placement")

				#goto play state
				if self.p1Ships==0 and self.p2Ships==0:
					self.state = 'play'
				elif self.p1Ships==0:
					self.p1Out.append("waiting for P2 to place ships")
					self.p2Out.append("P1 ready")

			elif self.state == 'play':
				if self.turn == 1:
					self.fireP1(input)
					self.turn = 2
					if self.checkWon(1): return
				else:
					self.p1Out.append("wait your turn")
		else:
			self.p1Out.append("bad input. Try again")


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
						self.p2Out.append("placed a ship. "+str(self.p2Ships)+" left")
					else:
						self.p2Out.append("not a valid ship placement")
				#goto play state
				if self.p1Ships==0 and self.p2Ships==0:
					self.state = 'play'
				elif self.p2Ships==0:
					self.p2Out.append("waiting for P1 to place ships")
					self.p1Out.append("P2 ready")

			elif self.state == 'play':
				if self.turn == 2:
					self.fireP2(input)
					self.turn = 1
					if self.checkWon(2): return
				else:
					self.p1Out.append("wait your turn")
		else:
			self.p2Out.append("bad input. Try again")


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
			self.p1Out.append("miss")
			self.p2Out.append(["miss",(coords[0],coords[1])])
			return False
		if x ==1: #hit ship
			self.p2Board[coords[1]][coords[0]] = 2
			self.p1Out.append("hit")
			self.p2Out.append(["hit", (coords[0], coords[1])])
			return True
		else:
			self.broadcastP1("repeated fire")

	# updates p1's board with an attack at coords
	def fireP2(self,coords):
		x = self.p1Board[coords[1]][coords[0]]
		if x==0: #hit water
			self.p1Board[coords[1]][coords[0]] = -1
			self.p2Out.append("miss")
			self.p1Out.append(["miss", (coords[0], coords[1])])
			return False
		if x ==1: #hit ship
			self.p1Board[coords[1]][coords[0]] = 2
			self.p2Out.append("hit")
			self.p1Out.append(["hit", (coords[0], coords[1])])
			return True
		else:
			self.p2Out.append("repeated fire")


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
		self.p1Out.append("winner is P"+str(winner)+"!")
		self.p2Out.append("winner is P" + str(winner) + "!")


	#check if there is a message for P1
	def broadcastP1(self,msg):
		m = self.p1Out
		self.p1Out = []
		return m


	#check if there is a message for P2
	def broadcastP2(self,msg):
		m = self.p2Out
		self.p2Out = []
		return m


	#send the appropriate boards to player NO MORE
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


