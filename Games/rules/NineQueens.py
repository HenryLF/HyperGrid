from .GameMode import GameBoard
from itertools import product


class Game(GameBoard):
	def cli_render(self,val):
		return 'Q' if val else ' '
	@property
	def queens(self):
		return set([i for i in self.indexes(True)])
	
	def valid(self,coord):
		X,Y = self.board_size
		i,j = coord
		for k,l in zip(range(X),range(Y)) :
			if (i,(j+l)) in self.queens.difference({coord}) : 
				return False#(i,j-l)
			if ((i+k),j) in self.queens.difference({coord}) : 
				return False#(i-k,j)
			if ((i+k),(j+l)) in self.queens.difference({coord}) : 
				return False#((i+k)//X,(j+l)//Y)
			if (i-k,j+l) in self.queens.difference({coord}) : 
				return False#(i-k,(j+l)//Y)
			if (i,(j-l)) in self.queens.difference({coord}) : 
				return False#(i,j-l)
			if ((i-k),j) in self.queens.difference({coord}) : 
				return False#(i-k,j)
			if ((i-k),(j-l)) in self.queens.difference({coord}) : 
				return False#((i+k)//X,(j+l)//Y)
			if (i+k,j-l) in self.queens.difference({coord}) : 
				return False#(i-k,(j+l)//Y)

		return True
#	@property
#	def valid_queens(self):
#		return set( [ q for q in  self.queens if self.valid(q) ] )
#	@property
#	def invalid_queens(self):
#		return self.queens.difference(self.valid_queens)


if __name__ == '__main__':
	g= Game(5)
	g[1,1] = True
