from enum import Enum
from random import sample
from itertools import product
BOARD_SIZE = (5,5)
MINE_NUMBER = 8

class Cell(Enum) :
	Hidden = '?'
	NoMine = 0
	OneMines = 1
	TwoMines = 2
	ThreeMines = 3
	FourMines = 4
	FiveMines = 5
	SixMines = 6
	SevenMines = 7
	EightMines = 8
	IsAMine = 'X'
class Minefield(list) :
	def __init__(self,board_size : tuple or None = None,n_mines : int or None = None):
		self.size = board_size if board_size else BOARD_SIZE
		self.n_mines = n_mines if n_mines else MINE_NUMBER
		self.turns = 0
		self.mines = {None}
		self.played = set()
		super().__init__([ [Cell.Hidden for j in range(self.size[1])] for i in range(self.size[0])])
	def play(self,i :int, j : int)  -> bool:
		if self.turns == 0 : self.pick_mine_location(i,j)
		x =  self.reveal_cell(i,j)
		if isinstance(x,str) : return x
		self.turns +=1
		return x
	def pick_mine_location(self, i : int, j : int) :
		loc = [i for i in range(self.size[0]*self.size[1])]
#		print((i,j),loc)
		loc.remove(i*self.size[0]+j)
		self.mines = set([ (i//self.size[0],i%self.size[1]) for i in sample(loc,self.n_mines)])
		self._board = [ [None for i in range(self.size[1]) ] for i in range(self.size[0])]
		for i, row in enumerate(self):
			for j , _  in enumerate(row) :
				if (i,j) in self.mines : 
					self._board[i][j] =Cell('X')
					continue
				self._board[i][j] = Cell(self.neighboring_bombs(i,j))

	@property
	def board(self):
		return self._board
		
	def neighboring_bombs(self,i: int,j: int):
		count = 0
		for k in [1,-1] :
			if (i+k,j) in self.mines : count +=1
			if (i,j+k) in self.mines : count +=1
			if (i+k,j+k) in self.mines : count +=1
			if (i-k,j+k) in self.mines : count +=1
		return count

	def reveal_cell(self,i : int,j : int):
		if any([i<0,j<0,i>=self.size[0],j>=self.size[1]]) : return 'Invalid'
		if (i,j) in self.mines : 
			self._reveal_board()
			return False
		if (i,j) in self.played : return True
		self.played.add((i,j))
		self[i][j] = self.board[i][j]
		
		if self.neighboring_bombs(i,j) > 0 :	
			return True
		for k in [1,-1] :
			self.reveal_cell(i+k,j)
			self.reveal_cell(i,j+k)
			self.reveal_cell(i+k,j+k)
			self.reveal_cell(i-k,j+k)
		return True
	def _reveal_board(self):
		for i, _ in enumerate(self.board):
			for j , cell in enumerate(_) :
				self[i][j] = cell
	def __repr__(self):
		s = ''
		for i, _ in enumerate(self):
			s+='\n|'
			for j , cell in enumerate(_) :
				s += f'{cell.value}|'
		return s
	def show(self) :
		s = ''
		for i, _ in enumerate(self.board):
			s+='\n|'
			for j , cell in enumerate(_) :
				s += f'{cell.value}|'
		print(s)

		
			

if __name__ == '__main__':
	m = Minefield()
	print(m)
	m.play(2,3)
	print(m)


