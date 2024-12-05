from collections.abc import Iterable


class GameBoard(list):

	def __init__(self,board_size :int or tuple,*arg,default_value : object or None = None,**kw):
		if isinstance(board_size,int)  : board_size = (board_size, board_size)
		super().__init__( [ [default_value for j in range(board_size[1])] for i in range(board_size[0]) ] )
		self.board_size = board_size
		self.default_value = default_value
		self.__post_init__(self,*arg,**kw)


	def __post_init__(self,*a,**kw) :
		pass
	def __getitem__(self,c : tuple):
		i , j = c
		return super().__getitem__(i).__getitem__(j)
	def __setitem__(self,c : tuple,val):
		i , j = c
		return super().__getitem__(i).__setitem__(j,val)
	
	def indexes(self, val):
		result = []
		for i,row in enumerate(self) :
			offset = -1
			while(True):
				try : 
					offset = row.index(val,offset+1)
				except ValueError : break
				yield i,offset
	def cli_render(self,val) :
		return val
	
	def __repr__(self):
		s = ''
		for i in range(self.board_size[0]):
			s+='\n|'
			for j in range(self.board_size[1]):
				s+=f'{self.cli_render(self[i,j])}|'
		return s


class ScrollerObject(set):
	def __init__(self , coords : Iterable,*arg, **kw):
		super().__init__()
		self.__post_init__(*arg,**kw)
		for i in coords : self.add(i)
	def __post_init__(self,*a,**kw):
		pass
	def front(self):
		I,J = [], 0
		for i,j in self :
			I+=[i]
			J = max(j,J)
		return (sum(I)//len(I)), J 
	def back(self):
		I,J = [], 0
		for i,j in self :
			I+=[i]
			J = min(j,J)
		return (sum(I)//len(self)), J 
	def top(self):
		I,J = 0, []
		for i,j in self :
			I = max(i,I)
			J+=[j]
		return I, (sum(J)//len(self))
	def bottom(self):
		I,J = 0, []
		for i,j in self :
			I = max(i,I)
			J+=[j]
		return I, (sum(J)//len(self))
	def scroll(self,*a) :
		pass
class Scroller(GameBoard):
	def __init__(self,board_size :int or tuple,*arg,default_value : object or None = None,**kw):
		self.object = dict()
		self.object_count = 0
		super().__init__(board_size,*arg,default_value = default_value,**kw)

	def add(self,obj : ScrollerObject ):
		self.object[self.object_count] = obj
		for coord in obj :
#			print(coord,obj)
			try: self[*coord] = self.object_count
			except IndexError : pass
		self.object_count+=1
				
	def is_object_offscreen(self,obj_id : int):
		I,J = self.board_size
		return all([ (not (0<=i<I) or not (0<=j<J)) for i,j in self.object[obj_id] ])


	def scroll(self,next_col : Iterable or None = None ):
		for i, obj in self.object.copy().items() :
			self.mask_object(i)
			obj.scroll(self.board_size)
			if self.is_object_offscreen(i) : self.object.pop(i)
			else : self.render_object(i)
	
	def mask_object(self,obj_id : int):
		for coord in self.object[obj_id]:
			if coord[0]<0 or coord[1]<0 : continue
			try: self[*coord] = self.default_value
			except IndexError : pass
	def delete_object(self,obj_id : int):
		self.mask_object(obj_id)
		self.object.pop(obj_id)
	def render_object(self,obj_id: int):
		for coord in self.object[obj_id]:
			if coord[0]<0 or coord[1]<0 : continue
			try: self[*coord] = obj_id
			except IndexError : pass

