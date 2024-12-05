from .TicTacToe import *


class HyperBoard(list):
	def __init__(self,size : int = 3):
		super().__init__([[Board(size) for i in range(size)] for i in range(size)])
		self.hyper_board = Board(size)
	
	@property
	def len(self):
		return len(self)

	def coord_to_subgrid(self,i : int,j:int):
		return (i//self.len,j//self.len) , (i%self.len,j%self.len)

	def play(self,i_row : int,j_col : int,player):
		(I,J) , (i, j) = self.coord_to_subgrid(i_row,j_col)
		if not self[I][J].play(i,j,player) : return False
		sub_chek = self[I][J].check() 
		if sub_chek : self.set_hyper_board(I,J,player)
		return True

	def check(self):
		return self.hyper_board.check()
	
	def set_hyper_board(self,I : int, J : int, player) :
		self.hyper_board.play(I,J,player)
		self[I][J]._fill(player)
	
	def __repr__(self):
		s = ''
		for K in range(self.len):
			s+='\n|'
			for I in range(self.len):
				for J in enumerate(self.len) :
					s += f'{self[K][I][K][J]}|'
		return s
