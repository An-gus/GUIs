import tkinter as tk


class Game(tk.Frame):

	def __init__(self):
		tk.Frame.__init__(self)
		self.grid()
		self.master.title('Connect Four')
		self.master.resizable(False, False)

		self.turn = 'Red'  #Human
		self.nturn = 'Purple'  #AI
		self.winner = None
		self.matrix = [['-'] * 7 for i in range(6)]

		self.clr = {
			'Purple':   '#ac49ee',
			'Red':      '#e12323',
			'board':    '#c07b39',
			'cells':    '#d7b365',
			'winText':  '#ffba7a',
			'winBG':    '#9b622c',
			'topColor': '#9b622c'
		}

		self.configure(bg=self.clr['topColor'])

		self.board = tk.Frame(self, bg=self.clr['board'], bd=3, width=700, height=600)
		self.board.grid(pady=(75, 0))

		self.master.bind('<1>', self.pos)
		self.makeGUI()

		self.mainloop()

	def reset(self):
		self.destroy()
		self.__init__()

	def makeGUI(self):
		self.cells = []
		for y in range(6):
			row = []
			for x in range(7):
				cellFrame = tk.Frame(
					self.board,
					bg=self.clr['board'],
					width=100,
					height=100
				)
				cellFrame.grid(row=y, column=x, padx=5, pady=5)
				cellcan = tk.Canvas(
					cellFrame,
					bg=self.clr['board'],
					width=100,
					height=100,
					bd=0,
					highlightthickness=0
				)
				cellcirc = cellcan.create_oval(0, 0, 100, 100, fill=self.clr['cells'], width=0)
				cellcan.pack()
				row.append([cellcan, cellcirc])
			self.cells.append(row)

		turnFrame = tk.Frame(self, bg=self.clr['topColor'])
		turnFrame.place(relx=0.5, y=38, anchor='center')
		tk.Label(turnFrame, text='Turn:', font=('Courier, 15'), bg=self.clr['topColor']).grid(row=0)
		self.turnLable = tk.Label(turnFrame, text=self.turn, font=('Courier, 20'), bg=self.clr['topColor'])
		self.turnLable.grid(row=1)

	def pos(self, event):
		# print('x:{0} y:{1}'.format(self.winfo_pointerx() - self.winfo_rootx(), self.winfo_pointery() - self.winfo_rooty()))
		x = self.winfo_pointerx() - self.winfo_rootx()
		y = self.winfo_pointery() - self.winfo_rooty()
		pos = None

		if y >= 75:
			if x >= 8 and x <= 108:
				pos = 0
			elif x >= 118 and x <= 218:
				pos = 1
			elif x >= 228 and x <= 328:
				pos = 2
			elif x >= 338 and x <= 438:
				pos = 3
			elif x >= 448 and x <= 548:
				pos = 4
			elif x >= 558 and x <= 658:
				pos = 5
			elif x >= 668 and x <= 768:
				pos = 6
		if pos != None:
			self.placed(pos)

	def placed(self, pos):
		if self.winner == None:
			for i in range(5, -1, -1):
				if self.matrix[i][pos] == '-':
					self.matrix[i][pos] = self.turn
					self.cells[i][pos][0].itemconfig(self.cells[i][pos][1], fill=self.clr[self.turn])
					break
			self.turn, self.nturn = self.nturn, self.turn
			self.turnLable.configure(text=self.turn)
			self.update_idletasks()
			if self.hasWon(self.matrix):
				self.winner = self.hasWon(self.matrix)
				if self.winner != 'd':
					txt = self.winner + ' has won!'
				else:
					txt = 'It\'s a draw!'
				winFrame = tk.Frame(self.board, borderwidth=2, bg=self.clr['winBG'])
				winFrame.place(relx=0.5, rely=0.5, anchor='center')
				tk.Label(
					winFrame,
					text=txt,
					fg=self.clr['winText'],
					bg=self.clr['winBG'],
					font=('Courier, 25')
				).pack()
				tk.Button(
					winFrame,
					text='Reset',
					fg=self.clr['winText'],
					bg=self.clr['winBG'],
					activebackground=self.clr['winBG'],
					activeforeground=self.clr['winText'],
					borderwidth=0,
					font=('Courier, 20'),
					command=self.reset
				).pack()

			coords = self.aiMove(self.matrix)
			if coords != None:
				x = coords['x']
				y = coords['y']
				self.matrix[y][x] = self.turn
				self.cells[y][x][0].itemconfig(self.cells[y][x][1], fill=self.clr[self.turn])
				self.turn, self.nturn = self.nturn, self.turn
				self.turnLable.configure(text=self.turn)
				self.update_idletasks()
				if self.hasWon(self.matrix):
					self.winner = self.hasWon(self.matrix)
					if self.winner != 'd':
						txt = self.winner+' has won!'
					else:
						txt = 'It\'s a draw!'
					winFrame = tk.Frame(self.board, borderwidth=2, bg=self.clr['winBG'])
					winFrame.place(relx=0.5, rely=0.5, anchor='center')
					tk.Label(
						winFrame,
						text=txt,
						fg=self.clr['winText'],
						bg=self.clr['winBG'],
						font=('Courier, 25')
					).pack()
					tk.Button(
						winFrame,
						text='Reset',
						fg=self.clr['winText'],
						bg=self.clr['winBG'],
						activebackground=self.clr['winBG'],
						activeforeground=self.clr['winText'],
						borderwidth=0,
						font=('Courier, 20'),
						command=self.reset
					).pack()



	def hasWon(self, board):
		Height = 6
		Width = 7
		# check horizontal spaces
		for y in range(Height):
			for x in range(Width - 3):
				x1 = board[y][x]
				x2 = board[y][x+1]
				x3 = board[y][x+2]
				x4 = board[y][x+3]
				if x1 == x2 and x2 == x3 and x3 == x4 and x1 != '-':
					return x1
		# check vertical spaces
		for x in range(Width):
			for y in range(Height - 3):
				x1 = board[y][x]
				x2 = board[y+1][x]
				x3 = board[y + 2][x]
				x4 = board[y + 3][x]
				if x1 == x2 and x2 == x3 and x3 == x4 and x1 != '-':
					return x1
		# check / diagonal spaces
		for x in range(Width - 3):
			for y in range(3, Height):
				x1 = board[y][x]
				x2 = board[y - 1][x + 1]
				x3 = board[y - 2][x + 2]
				x4 = board[y - 3][x + 3]
				if x1 == x2 and x2 == x3 and x3 == x4 and x1 != '-':
					return x1
		# check \ diagonal spaces
		for x in range(Width - 3):
			for y in range(Height - 3):
				x1 = board[y][x]
				x2 = board[y + 1][x + 1]
				x3 = board[y + 2][x + 2]
				x4 = board[y + 3][x + 3]
				if x1 == x2 and x2 == x3 and x3 == x4 and x1 != '-':
					return x1
		# check draw
		if not any('-' in x for x in board):
			return 'd'
		# no winner
		return None

	def aiMove(self, board):
		depth = 7 #This is the search depth of the MinMax, increasing it makes the AI 'smarter' but exponentially extends run time
		if self.winner == None:
			_x, _y = None, None
			pos = None
			MaxVal = -99
			plays = self.getPlays(self.matrix)
			for play in plays:
				_x,_y = play['x'], play['y']
				board[_y][_x] = 'Purple'
				val = self.minmax(board, -999, 999, depth, False)
				board[_y][_x] = '-'
				if val > MaxVal:
					MaxVal = val
					pos = {'x':_x, 'y':_y}
			return pos



	def minmax(self, board, alpha, beta, depth, amMax):
		wnr = self.hasWon(board)
		if wnr != None or depth == 0:
			if wnr == 'Purple':
				return 100
			elif wnr == 'Red':
				return -100
			elif wnr == 'd':
				return 0
			else:
				return self.score(board)
		if amMax:
			MaxVal = -999
			plays = self.getPlays(board)
			for play in plays:
				x,y = play['x'], play['y']
				board[y][x] = 'Purple'
				MaxVal = max(self.minmax(board, alpha, beta, depth-1, False), MaxVal)
				board[y][x] = '-'
				alpha = max(alpha, MaxVal)
				if alpha >= beta: return MaxVal
			return MaxVal
		else:
			MinVal = 999
			plays = self.getPlays(board)
			for play in plays:
				x,y = play['x'],play['y']
				board[y][x] = 'Red'
				MinVal = min(self.minmax(board, alpha, beta, depth-1, True), MinVal)
				board[y][x] = '-'
				beta = min(beta, MinVal)
				if beta <= alpha: return MinVal
			return MinVal


	def getPlays(self, board):
		plays = []
		for x in range(6):
			for y in range(5, -1, -1):
				if board[y][x] == '-':
					plays.append({'x':x, 'y':y})
					break
		return plays

	def score(self, board):
		score = 0
		#check horizontal
		for y in range(6):
			for x in range(6):
				if board[y][x] == board[y][x+1]:
					score += (board[y][x]=='Purple')-(board[y][x]=='Red')
		#check vertical
		for x in range(7):
			for y in range(5):
				if board[y][x] == board[y+1][x]:
					score += (board[y][x] == 'Purple')-(board[y][x] == 'Red')
		#cehck /
		for x in range(6):
			for y in range(5,0,-1):
				if board[y][x] == board[y-1][x+1]:
					score += (board[y][x] == 'Purple')-(board[y][x] == 'Red')
		#check \
		for x in range(6):
			for y in range(4, -1, -1):
				if board[y][x] == board[y+1][x+1]:
					score += (board[y][x] == 'Purple')-(board[y][x] == 'Red')
		return score


if __name__ == '__main__':
	Game()