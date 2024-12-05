from enum import Enum, auto
from itertools import product, cycle
from dataclasses import dataclass
BOARD_SIZE = 10

class Figure(Enum) :
	PAWN = auto()
	DAME = auto()

class Color(Enum):
	WHITE = auto()
	BLACK = auto()
@dataclass
class Piece():
	rank : Figure
	owner : Color
	coord : tuple

class DameGame(list):
	PLAYERS = cycle([Color.WHITE,Color.BLACK])
	def __init__(self,size):
		super().__init__([[[None] for j in range(size//2)]for i in range(size)])
		for i in range(3):
			for j in range(size//2):
				
				self.append(Piece(rank = Figure.PAWN, owner = Color.WHITE, coord = (i,j) ))
				self.append(Piece(rank = Figure.PAWN, owner = Color.WHITE, coord = (size - 1 - i,j) ))
		self.size = (size,size//2)
	
	def jump(self,coord : tuple):
		i,j = coord
		for k in [1,-1] :
			for l in [0,-1] if i%2 else [0,1]:
				if  i+k in range(self.size[0]) and j+l in range(self.size[1]):
					yield i+k , j+l
	def board(self):
		l = [ [None for j in range(self.size[1]) ] for i in range(self.size[0]) ]
		for p in self:
			i,j = p.coord
			print(i,j)
			l[i][j] = p

	def next_player(self):
		self._turn_player = next(self.PLAYERS)
	def turn_player(self):
		return self._turn_player
	def turn_player_pieces(self):
		for i in self :
			if i.owner == self.turn_player : yield i
	def opponent_pieces(self):
		for i in self :
			if i.owner != self.turn_player : yield i
	def from_coord(self,coord : tuple):
		for i,p in enumerate(self) :
			if p.pos == coord : return self[i]
		return False
	def init_turn(self, coord : tuple):
		p = self.from_coord(coord)
		if p :
			match p.rank:
				case Figure.PAWN : self.legal_moves = self.pawn_move_search(p)
				case Figure.DAME : pass
		return True
	def pawn_move_search(self,p : Piece):
		moves = Moves()
		capt_check = set()
		for c in self.jump(p.coord) :
			if not self.from_coord(c) : Moves[Move].add(c)
			elif self.from_coord(c) in self.opponent_pieces : capt_check.add(self.from_coord(c))
		for p in capt_check:
			Moves['Capture'].add( self.pawn_capture_check(p,c)) )
			
	
	def pawn_capture_check(self, atk :piece, tgt : piece) :
		"""
			Recursive ckeck of capture, return a list[tuple or Move] ] )
		"""
		tgt_i,tgt_j = tgt.coord
		atk_i,atk_j = atk.coord
		k = tgt_i - atk_i
		l = tgt_j - atk_j
		chain = []
		if ( tgt_i + k in range(self.size[0]]) ) and ( tgt_j + l in range(self.size[1]) ) :
			if not self.from_coord((tgt_i +k), (tgt_j + l) ) :
				chain+=[ ( (tgt_i +k), (tgt_j + l) ) ]
		pass		
		
	def __repr__(self):
		l = self.board()
		s = ''
		for i in range(self.size[0]):
			s+='\n|'
			for j in range(self.size[1]):
				s+=f'{l[i][j]}|'.zfill(5)
		return s
	
class Moves(dict):
	def __init__(self):
		super().__init__(('Move',set()),('Capture',set()))
	pass
