from .GameMode import GameBoard
from itertools import product
from time import sleep
class Game(GameBoard):
	def __post_init__(self,*a,**kw):
		self.max_living_cells = 0
	def cli_render(self,val):
		return int(val)
	def surrounding_cells(self,coord : tuple):
		i , j = coord
		yield (i+1) % self.board_size[0], j
		yield i, (j+1) % self.board_size[1]
		yield (i+1) % self.board_size[0], (j+1) % self.board_size[1]
		yield (i-1), j
		yield i, (j-1) 
		yield (i-1), (j-1 )
		yield (i+1) % self.board_size[0], (j-1) 
		yield (i-1) , (j+1) % self.board_size[1]

	def surrounding_live_cell_num(self,coord : tuple):
		count = 0
		for c in self.surrounding_cells(coord) :
#			print(c,self[*c])
			if self[*c] : count += 1
		return count
	@property
	def active_cells(self) :
		active_cells = set()
		for cell in self.indexes(True):
			active_cells.add(cell)
			for sur_cell in self.surrounding_cells(cell):
				active_cells.add(sur_cell)
		return active_cells
		
	
	def update_cells(self):
		update = dict()
		for c in self.active_cells :
			match self.surrounding_live_cell_num(c):
				case x if x<2 : update[c] = False
				case x if x>3 : update[c] = False
				case 3 if not self[*c]: update[c] = True
		for coord, state in update.items() :
			self[*coord] = state
		return update
	@property
	def live_cell_count(self):
		x = len([i for i in self.indexes(True)])
		self.max_living_cells = max(self.max_living_cells,x)
		return x
	
	def run(self,delay : int) :
		print(self)
		self.max_living_cells = 0
		while(self.active_cells):
			self.update_cells()
			print(self)
			sleep(delay)

if __name__ == '__main__':
	G = Game(20)
	G[4,5] = True
	G[4,4] = True
	G[5,5] = True
	G[6,5] = True
	
	
	


