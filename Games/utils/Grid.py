import PySimpleGUI as sg
import math
from itertools import product
from collections.abc import Iterable
from copy import deepcopy
#CONSTANTS
CELL_SIZE = (20,20)

def closestDivisors(n):
	a = round(math.sqrt(n))
	while n%a > 0: a -= 1
	return a,n//a


def key_to_coord(key : str) -> Iterable[int,int]:
	try :
		s = key.split('_')[-1].split(':')
		return int(s[0]),int(s[1])
	except Exception : return False


def Grid(size : int or Iterable[int,int],key_prefix :str = '',cell_size : Iterable[int,int] or None = None,right_click_menu : list or None = None,**kw):
	if isinstance(size,int) :
		I,J = closestDivisors(size)
	else : I,J = size
	if cell_size is None : cell_size = CELL_SIZE
	kwarg = {
	'canvas_size' : cell_size,
	'enable_events' : True,
	'graph_bottom_left' : (0,0),
	'pad' : (0,0),
	'graph_top_right' : cell_size,
	'background_color' : 'white',
	}
	kwarg.update(kw)
	return [
	[sg.Graph(k = key_prefix + f'_{i}:{j}',right_click_menu = ([[],[f'{m}_{i}:{j}' for m in right_click_menu]] if right_click_menu else None),**kwarg) for j in range(J)]
	 for i in range(I) ]


class GridElement(sg.Graph):
	def __init__(self,size : int or Iterable[int,int],cell_size : int or Iterable[int,int],**kw):
		if isinstance(size,int) :
			self.size = (size,size)
		else : self.size = size
		if isinstance(cell_size,int) :
			self.cell_size = (cell_size,cell_size)
		else : self.cell_size = cell_size
		I,J = self.size
		i,j = self.cell_size
		kwarg ={ 
	'canvas_size' : (i*I,j*J),
	'enable_events' : True,
	'graph_bottom_left' : (0,0),
	'pad' : (0,0),
	'graph_top_right' : (i*I,j*J),
	'background_color' : 'white',
	}
		kwarg.update(**kw)
		super().__init__(**kwarg)
		self.drawings = dict()
		self.backgrounds = dict()
	
	def _convert_canvas_xy_to_xy(self, x_in, y_in):
		 x_in, y_in = super()._convert_canvas_xy_to_xy(x_in, y_in)
		 return x_in//self.cell_size[0],y_in//self.cell_size[0]
	
	def color_cell(self,i : int,j : int ,color : str or Iterable) :
		self.uncolor_cell(i,j)
		I,J =  i*self.cell_size[0], j*self.cell_size[1]
		im = self.draw_rectangle((I,J),(I+self.cell_size[0],J+self.cell_size[0]),fill_color = color,line_color = color)
		self.tk_canvas.tag_lower(im)
		self.backgrounds[(i,j)]= (im,color)
	def uncolor_cell(self,i : int,j : int ) :
		if (i,j) in self.backgrounds : 
			self.delete_figure(self.backgrounds[(i,j)][0])
			self.backgrounds.pop((i,j))
		
	def draw_cell(self,i : int,j : int,**kw):
		I,J =  i*self.cell_size[0], (j+1)*self.cell_size[1]
		kwarg = {
		'location' : (I,J)
		}
		kwarg.update(kw)
		im = self.draw_image(**kwarg)
		if (i,j) in self.drawings : self.drawings[(i,j)].append(im)
		else: self.drawings[(i,j)] = [im] 
		
	def erase_cell(self,i:int,j:int):
		for im in self.drawings.get((i,j),[]):
#			print(im,type(im))
			self.delete_figure(im)
	def erase_all_cell(self):
		for k,it in self.drawings.items():
			for im in it : self.delete_figure(im)
	def grid(self,a:bool = True,**kw):
		if a :
			self.g=[]
			for i,j in zip(range(1,self.size[0]),range(1,self.size[1])):
				self.g.append(self.draw_line((i*self.cell_size[0],0),(i*self.cell_size[0],self.CanvasSize[1])))
				self.g.append(self.draw_line((0,j*self.cell_size[1]),(self.CanvasSize[0],j*self.cell_size[1])))
		else : 
			for im in self.g :
				self.delete_figure(im)



if __name__ == '__main__':
	g = GridElement(10,20,k='g')
	w = sg.Window('Hi',[[g],[sg.Button(k='d',button_text = 'Break')]],finalize = True)
	while(True):
		ev,val = w.read()
		print(ev,val)
		match ev :
			case 'd' : break 



