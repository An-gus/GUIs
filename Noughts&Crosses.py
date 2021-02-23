import tkinter as tk

class Game(tk.Frame):
	def __init__(self):
		tk.Frame.__init__(self)
		self.grid()
		self.master.title('Tick-Tack-Toe')
		self.master.resizable(False, False)

		self.turn = 'Crosses'
		self.nturn = 'Noughts'
		self.matrix = [['-']* 3 for i in range(3)]
		self.winner = None

		self.clr = {
			'Crosses':'#ac49ee',
			'Noughts':'#e12323',
			'board':'#c07b39',
			'cells':'#d7b365',
			'winText':'#ffba7a',
			'winBG':'#9b622c',
			'topColor':'#9b622c'
		}

		self.configure(bg=self.clr['topColor'])

		self.icon = {
			'Crosses':'X',
			'Noughts':'O'
		}

		self.board = tk.Frame(self, bg=self.clr['board'], bd=3, width=450, height=450)
		self.board.grid(pady=(75,0))
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
				celldata = {'frame':cellFrame, 'val':cellVal}
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
			if y >= 58 and y <= 208:
				pos = 0

			elif y >= 218 and y <= 368:
				pos = 3

			elif y >= 378 and y <= 528:
				pos = 6

		elif x >= 168 and x <= 318:
			if y >= 58 and y <= 208:
				pos = 1

			elif y >= 218 and y <= 368:
				pos = 4

			elif y >= 378 and y <= 528:
				pos = 7


		elif x >= 328 and x <= 478:
			if y >= 58 and y <= 208:
				pos = 2

			elif y >= 218 and y <= 368:
				pos = 5

			elif y >= 378 and y <= 528:
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

			if self.hasWon():
				self.winner = self.hasWon()
				winFrame = tk.Frame(self.board, borderwidth=2, bg=self.clr['winBG'])
				winFrame.place(relx=0.5, rely=0.5, anchor='center')
				tk.Label(
					winFrame,
					text=self.winner+' has won!',
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

	def hasWon(self):
		# check rows
		for i in range(3):
			i0 = self.matrix[i][0]
			i1 = self.matrix[i][1]
			i2 = self.matrix[i][2]
			if i0 == i1 and i1 == i2 and i1 != '-':
				return i0
		# check cols
		for i in range(3):
			i0 = self.matrix[0][i]
			i1 = self.matrix[1][i]
			i2 = self.matrix[2][i]
			if i0 == i1 and i1 == i2 and i1 != '-':
				return i0
		# check diag
		if self.matrix[0][0] == self.matrix[1][1] and self.matrix[1][1] == self.matrix[2][2] and self.matrix[1][1] != '-':
			return self.matrix[1][1]
		if self.matrix[0][2] == self.matrix[1][1] and self.matrix[1][1] == self.matrix[2][0] and self.matrix[1][1] != '-':
			return self.matrix[1][1]
		#no winner
		return None


if __name__ == '__main__':
	Game()
