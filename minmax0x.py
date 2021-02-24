import tkinter as tk


class Game(tk.Frame):
	def __init__(self):
		tk.Frame.__init__(self)
		self.grid()
		self.master.title('Tick-Tack-Toe')
		self.master.resizable(False, False)

		self.turn = 'Crosses' # Player
		self.nturn = 'Noughts' # AI
		self.matrix = [['-'] * 3 for i in range(3)]
		self.winner = None

		self.clr = {
			'Crosses':  '#ac49ee',
			'Noughts':  '#e12323',
			'board':    '#c07b39',
			'cells':    '#d7b365',
			'winText':  '#ffba7a',
			'winBG':    '#9b622c',
			'topColor': '#9b622c'
		}

		self.configure(bg=self.clr['topColor'])

		self.icon = {
			'Crosses': 'X',
			'Noughts': 'O'
		}

		self.board = tk.Frame(self, bg=self.clr['board'], bd=3, width=450, height=450)
		self.board.grid(pady=(75, 0))
		self.makeGui()

		self.master.bind('<1>', self.pos)

		self.mainloop()

	def reset(self):
		self.destroy()
		self.__init__()

	def makeGui(self):
		self.cells = []
		for i in range(3):
			row = []
			for j in range(3):
				cellFrame = tk.Frame(
					self.board,
					bg=self.clr['cells'],
					width=150,
					height=150
				)
				cellFrame.grid(row=i, column=j, padx=5, pady=5)
				cellVal = tk.Label(self.board, bg=self.clr['cells'])
				cellVal.grid(row=i, column=j)
				celldata = {'frame': cellFrame, 'val': cellVal}
				row.append(celldata)
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

		if x >= 8 and x <= 158:
			if y >= 83 and y <= 233:
				pos = 0

			elif y >= 243 and y <= 393:
				pos = 3

			elif y >= 403 and y <= 553:
				pos = 6

		elif x >= 168 and x <= 318:
			if y >= 83 and y <= 233:
				pos = 1

			elif y >= 243 and y <= 393:
				pos = 4

			elif y >= 403 and y <= 553:
				pos = 7


		elif x >= 328 and x <= 478:
			if y >= 83 and y <= 233:
				pos = 2

			elif y >= 243 and y <= 393:
				pos = 5

			elif y >= 403 and y <= 553:
				pos = 8

		if pos != None:
			self.placed(pos)

	def placed(self, pos):
		y = pos % 3
		x = pos // 3
		if self.matrix[x][y] == '-' and self.winner == None:
			self.matrix[x][y] = self.turn
			self.cells[x][y]['frame'].configure(bg=self.clr[self.turn])
			self.cells[x][y]['val'].configure(bg=self.clr[self.turn], text=self.icon[self.turn], font=('Courier, 50'))
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
			x = coords['x']
			y = coords['y']
			self.matrix[y][x] = self.turn
			self.cells[y][x]['frame'].configure(bg=self.clr[self.turn])
			self.cells[y][x]['val'].configure(bg=self.clr[self.turn], text=self.icon[self.turn], font=('Courier, 50'))
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


	def hasWon(self, board):
		# check rows
		for i in range(3):
			i0 = board[i][0]
			i1 = board[i][1]
			i2 = board[i][2]
			if i0 == i1 and i1 == i2 and i1 != '-':
				return i0
		# check cols
		for i in range(3):
			i0 = board[0][i]
			i1 = board[1][i]
			i2 = board[2][i]
			if i0 == i1 and i1 == i2 and i1 != '-':
				return i0
		# check diag
		if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[1][1] != '-':
			return board[1][1]
		if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[1][1] != '-':
			return board[1][1]
		# check draw
		if not any('-' in x for x in board):
			return 'd'
		# no winner
		return None

	def minmax(self, board, amMax):
		wnr = self.hasWon(board)
		if wnr != None:
			if wnr == 'Noughts': return 10
			elif wnr == 'Crosses': return -10
			else: return 0
		if amMax:
			MaxVal = -999
			for y in range(3):
				for x in range(3):
					if board[y][x] == '-':
						board[y][x] = 'Noughts'
						val = self.minmax(board, False)
						board[y][x] = '-'
						MaxVal = max(val, MaxVal)
			return MaxVal
		else:
			MaxVal = 999
			for y in range(3):
				for x in range(3):
					if board[y][x] == '-':
						board[y][x] = 'Crosses'
						val = self.minmax(board, True)
						board[y][x] = '-'
						MaxVal = min(val, MaxVal)
			return MaxVal

	def aiMove(self,board):
		if self.winner == None:
			pos = None
			Maxval = -99
			for y in range(3):
				for x in range(3):
					if board[y][x] == '-':
						board[y][x] = 'Noughts'
						val = self.minmax(board, False)
						board[y][x] = '-'
						if val > Maxval:
							Maxval = val
							pos = {'x':x, 'y':y}
			return pos


if __name__ == '__main__':
	Game()