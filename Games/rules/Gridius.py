from .GameMode import Scroller,ScrollerObject
from random import randint
from copy import copy
class Laser(ScrollerObject):
	icon = ''
	def __post_init__(self,direction : tuple = (0,1)):
		self.dir = direction
	def scroll(self,*a) :
		for (i,j) in self.copy() :
			self.remove((i,j))
			self.add(( i + self.dir[0], j + self.dir[1] ) )
class Asteroid(Laser):
	icon = ''



class PlayerShip(ScrollerObject):
	icon = ''
	def shoot(self):
#		print(max(self,key  = lambda c : c[1]))
		return Laser([max(self,key  = lambda c : c[1])],direction = (0,1))
	def move(self,direction):
		for (i,j) in self.copy() :
			self.remove((i,j))
			self.add( (i + direction[0], j + direction[1] ) )

class EnemyShip(ScrollerObject):
	def __post_init__(self):
		self.dir = 1
	def shoot(self):
		x , y = min(self,key = lambda c : c[1])
		return Laser([(x,y-1)],direction = (0,-1))
	def scroll(self,board_size):
		X,Y = board_size
#		print(X,Y,self.back()[1],Y//2)
#		if self.back[1] > Y//2 :
		for (i,j) in self.copy() :
			if i == X-1 or i == 0 : self.dir = -self.dir
			self.remove((i,j))
			self.add( ( i , (j-1)) if j>Y//2 else ((i+self.dir),j))
#		else :
#			for (i,j) in self.copy() :
#				self.remove((i,j))
#				self.add( ( i+self.dir , j ) )
class Game(Scroller):
	def __post_init__(self,*a,**kw):
		x = PlayerShip( [(self.board_size[0]//2,1)] )
		self.add(x)
	
	def run(self,player_move : tuple or None = None,shoot :bool = False):
		if player_move : self.player_move(player_move)
		for i in self.player_colision() : return False
		if shoot : self.player_shoot()
		self.scroll()
		for (id1,id2),x in self.object_colision():
			x = set(x)
			if x=={EnemyShip, Laser} :
				self.delete_object(id1)
				self.delete_object(id2)
			if x=={EnemyShip,Asteroid} :
				self.delete_object(id1)
				self.delete_object(id2)
			if x=={Asteroid,Laser} :
				self.delete_object(id1)
				self.delete_object(id2)
				
		return True
	def player_move(self,direction):
		self.mask_object(0)
		x = copy( self.object[0] )
		self.object[0].move(direction)
		if self.is_object_offscreen(0) : self.object[0] = x
		self.render_object(0)
	def player_shoot(self):
		self.add(self.object[0].shoot())
	def enemy_shoot(self,obj_id : int or None = None):
		if obj_id :
			self.add(self.object[obj_id].shoot())
		else :
			for k , obj in self.object.copy().items():
				if k == 0 : continue
				if hasattr(obj,'shoot'):
					self.add(obj.shoot())
	def player_colision(self):
		for id_,obj in list(self.object.items())[1:] :
				if self.object[0].intersection(obj) : yield id_ , obj.__class__
	def object_colision(self):
		for i,(id1,obj1) in enumerate(list(self.object.items())[1:-1]) :
			for id2,obj2 in list(self.object.items())[i+1:] :
				if id1==id2 : continue
				if obj1.intersection(obj2) : yield (id1,id2) , (obj1.__class__,obj2.__class__)
		
	def spawn_asteroid(self):
		self.add( Asteroid( [(randint(0,self.board_size[0]),self.board_size[1])],direction = (0,-1)) )
	def spawn_enemyship(self ):
		 self.add(EnemyShip( [(randint(0,self.board_size[0]),self.board_size[1])]) )
