import PySimpleGUI as sg
from .utils.Grid import GridElement
from .utils.GameExitCode import ExitCode,ExitQuery
from .utils.Logic import within,is_type,AND
from itertools import chain,product
from PIL import Image

DICT = {
'enable_events' : True
}
CELL_SIZE =(10,10)
CANVAS_SIZE = (100,100)
DEFAULT_BRUSH = 1
DEFAULT_COLOR = [0,0,0]
def layout(size : tuple,cell_size : tuple,color : list,brush : int):
	Column2 = [
	[sg.Text('Pixel_size :'),sg.Slider(k = 'CELL',range = (1,50),default_value = cell_size[0],resolution = 5,orientation = 'h',**DICT)	],
	[sg.Text('Size :'),sg.Combo(k='SIZEX',default_value = size[0],values = list(range(50,600,25)),**DICT),
	sg.Text(' x '),sg.Combo(k='SIZEY',default_value = size[1],values = list(range(50,600,25)),**DICT),
	sg.Button(button_text = 'NEW',k = 'NEW',**DICT)],
	[sg.Text('Color :'),sg.Graph(k = 'COLOR_SMP',canvas_size = (44,44),graph_bottom_left = (0,0),graph_top_right = (44,44),**DICT)],
	[ sg.Text('R:'),sg.Input(k='RGB_R',size=3,default_text = color[0],**DICT),
	sg.Text('G:'),sg.Input(k='RGB_G', size = 3,default_text = color[1],**DICT),
	sg.Text('B:'),sg.Input(k='RGB_B', size = 3,default_text = color[2],**DICT),
	],
	[sg.Text('Red :'),sg.Slider(k = 'SLIDER_R',range = (0,255),default_value = color[0],resolution = 1,orientation = 'h',**DICT)],
	[sg.Text('Green :'),sg.Slider(k = 'SLIDER_G',range = (0,255),default_value = color[1],resolution = 1,orientation = 'h',**DICT)],
	[sg.Text('Blue :'),sg.Slider(k = 'SLIDER_B',range = (0,255),default_value = color[2],resolution = 1,orientation = 'h',**DICT)],
	[sg.Text('Brush size :'),sg.Slider(k = 'BRUSH',range = (1,30),default_value = brush,resolution = 1,orientation = 'h',**DICT)],
	[sg.Checkbox(text = 'ERASE',k = 'ERASE',**DICT),sg.Button(button_text = 'SAVE',k = 'SAVE',**DICT),sg.Button(button_text = 'QUIT',k = 'QUIT',**DICT)],
	[sg.Checkbox(k='GRID',text = 'Grid',**DICT)],
	]
	return [
[GridElement(size,cell_size = cell_size,background_color = '#deddda',k='CANVAS',drag_submits = True ),
sg.Column(Column2)
	]]
	

def reset_window(window : sg.Window or None,size : tuple,cell_size,color,brush):
	if window : window.close()
	window = sg.Window('Pixel_Art',layout = layout(size,cell_size,color,brush),finalize = True)
	window[f'COLOR_SMP'].update(background_color = to_hex(*color))
	return window


RGB = {'R' : 0,'G' : 1,'B' : 2}
def update_color(window : sg.Window , l: list,c :str,val : int):
	window[f'SLIDER_{c}'].update(value = val)
	window[f'RGB_{c}'].update(value = val)
	l[RGB[c]] = val
	window[f'COLOR_SMP'].update(background_color = to_hex(*l))
	return l

def to_hex(r :str, g :str, b :str):
	r , g , b = hex(int(r))[2:],hex(int(g))[2:],hex(int(b))[2:]
	return f'#{r.zfill(2)}{g.zfill(2)}{b.zfill(2)}'
def to_rgb(h :str):
	print(h)
	return int(h[1:3],16),int(h[3:5],16),int(h[5:7],16)

	
def color_pixel(window : sg.Window,i:int,j:int,color : list, brush : int):
	window['CANVAS'].color_cell(i,j,to_hex(*color))
	if brush>1 :
		for k,l in product(range(-brush//2,brush//2),range(-brush//2,brush//2)):
			color_pixel(window,i+k,j,color,1)
			color_pixel(window,i,j+l,color,1)
			color_pixel(window,i+k,j+l,color,1)
			color_pixel(window,i+k,j-l,color,1)

def save_as(window : sg.Window, file_name : str):
	im = Image.new('RGB',window['CANVAS'].size,(0,0,0,0))
	lo,la = window['CANVAS'].size
	for (i,j),(_,color) in window['CANVAS'].backgrounds.items():
		im.putpixel((i,lo - j),to_rgb(color))
	im.save(file_name,format='png')

def erase_pixel(window : sg.Window, coord : tuple,brush : int):
	if coord in window['CANVAS'].backgrounds:
		im, _  = window['CANVAS'].backgrounds.pop(coord)
		window['CANVAS'].delete_figure(im)
	i,j = coord
	if brush>1 :
		for k,l in product(range(-brush//2,brush//2),range(-brush//2,brush//2)):
			erase_pixel(window,(i+k, j) ,1)
			erase_pixel(window,(i, j+k) ,1)
			erase_pixel(window,(i+k,j+k),1)
			erase_pixel(window,(i+k,j-k),1)



color_validation = within(0,255)
size_validation = AND(is_type(int),is_type(int))

def run(*a):
	color = DEFAULT_COLOR
	brush = DEFAULT_BRUSH
	DRAW = True
	window = reset_window(None,CANVAS_SIZE,CELL_SIZE,color,brush)
	while(True):
		ev,val = window.read()
		print(ev, val,color)
		match ev :
			case sg.WINDOW_CLOSED | 'Cancel' : 
				window.close()
				return ExitQuery() , None 
			case 'QUIT':
				x = ExitQuery(True)
				if x : 
					window.close() 
					return x, None
			case 'CANVAS' if DRAW : color_pixel(window,*val[ev],color,brush)
			case 'CANVAS' if not DRAW : erase_pixel(window,val[ev],brush)
			case 'ERASE' : DRAW = not val[ev]
			case 'RGB_R' if color_validation(val[ev]) : color = update_color(window,color,'R',val[ev])
			case 'RGB_G' if color_validation(val[ev]) : color = update_color(window,color,'G',val[ev])
			case 'RGB_B' if color_validation(val[ev]) : color = update_color(window,color,'B',val[ev])
			case 'SLIDER_R' : color = update_color(window,color,'R',val[ev])
			case 'SLIDER_G' : color = update_color(window,color,'G',val[ev])
			case 'SLIDER_B' : color = update_color(window,color,'B',val[ev])
			case 'GRID' : window['CANVAS'].grid(val[ev])
			case 'SAVE' :
				file_path = sg.popup_get_file("Where do you want to save your file?",default_extension = 'png',save_as = True)
				if file_path : save_as(window,file_path)
			case 'NEW' : 
				if size_validation.map([val['CELL'],val['SIZEX'],val['SIZEY']]):
					window = reset_window(window,( int(val['SIZEX']), int(val['SIZEY']) ),( int(val['CELL']), int(val['CELL']) ),color,brush)
			case 'BRUSH' : 
				brush = int(val[ev])


if __name__ == '__main__':
	run()





