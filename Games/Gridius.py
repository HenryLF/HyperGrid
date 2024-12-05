import PySimpleGUI as sg
from itertools import product
from random import choice,randint
from time import perf_counter
if __name__ == '__main__':
	
	from rules.Gridius import Game,Laser,Asteroid,PlayerShip,EnemyShip
	from utils.Grid import GridElement
	from utils.GameExitCode import ExitCode,ExitQuery
	from img.icon_gridius import icon
else :
	from .rules.Gridius import Game,Laser,Asteroid,PlayerShip,EnemyShip
	from .utils.Grid import GridElement
	from .utils.GameExitCode import ExitCode,ExitQuery
	from .img.icon_gridius import icon
BOARDSIZE = (15,15)
DICT = {
'enable_events' : True,
'expand_x' : True
}
Laser.icon = [icon['Laser']]
Asteroid.icon = [icon['Asteroid']]
PlayerShip.icon = [icon['PlayerShip']]
EnemyShip.icon = [icon['EnemyShip']]

GREEN = '#2ec27e'
SPACE_COLOR = '#131323'
RED = "#E05656"
WHITE = '#ffffff'
STAR_DENSITY = 1
DELAY = .5

def layout(board_size: tuple) -> list:
	return [
	[GridElement(board_size,cell_size = 44,key = 'SCREEN')],
	
	[sg.Button('UP',k='UP',**DICT),sg.Button('DOWN',k='DOWN',**DICT),
	sg.Button('LEFT',k='LEFT',**DICT),sg.Button('RIGHT',k='RIGHT',**DICT),
	sg.Button('SHOOT',k='SHOOT',**DICT),sg.Button('Scroll',k='SCROLL',**DICT)],
	[sg.Button('Reset',k='RESET',**DICT),sg.Button('Quit',k='QUIT',**DICT)],
	[sg.Text('Board Size : '),sg.Combo(k='SIZEX',default_value = board_size,values = [i for i in range(20)] ,**DICT),sg.Text('Board Size : '),sg.Combo(k='SIZEY',default_value = board_size,values = [i for i in range(20)] ,**DICT)],
		]


def reset_window(win : sg.Window or None, board_size : int):
	if win : win.close()
	win = sg.Window('Gridius',layout(board_size),return_keyboard_events=True,finalize = True)
	win['SCREEN'].update(background_color = SPACE_COLOR)
	X,Y =  win['SCREEN'].get_size()
	print(X)
	for i in range(int(STAR_DENSITY*X*Y/1936)):
		x,y = randint(0,X),randint(0,Y)
		win['SCREEN'].draw_point((x,y),size = randint(1,3), color = choice([WHITE,RED,GREEN]))
	board = Game(board_size)
	return win,board

def render_screen(win : sg.Window, board : Game) :
	win['SCREEN'].erase_all_cell()
	for i, obj in board.object.items() :
		for k,(y,x) in enumerate(obj) :
			win['SCREEN'].draw_cell(x,y,data = obj.icon[k])
def game_over(win : sg.Window, board : Game):
	win['SCREEN'].update(background_color = RED)
	
def run(Player = None):
	board_size = BOARDSIZE
	win, board = reset_window(None,board_size)
	render_screen(win,board)
	while(True):
		move,shoot = None,False
		t0 = perf_counter()
		ev, val = win.read(timeout = DELAY,timeout_key = 'Pass' )
		print(ev,val)
		match ev :
			case sg.WINDOW_CLOSED | 'Cancel' : 
				return ExitQuery() , None
			case 'RESET' : win , board = reset_window(win,board_size)
			case 'QUIT':
				x =ExitQuery(True)
				if x :
					win.close()
					return x , None
			case 'SIZEX' :
				try : board_size = (int(val[ev]),board_size[1])
				except ValueError : win[ev].update(value = board_size[0])
			case 'SIZEY' :
				try : board_size = (board_size[0],int(val[ev]))
				except ValueError : win[ev].update(value = board_size[1])
			case 'UP'|'Up:111': move = (1,0)
			case 'DOWN'|'Down:116': move = (-1,0)
			case 'LEFT'|'Left:113': move = (0,-1)
			case 'RIGHT'|'Right:114': move = (0,1)
			case 'SHOOT'| 'Control_R:105': shoot = True
			case 'SCROLL' : board.scroll()
		if randint(0,99) < 20: board.spawn_asteroid()
		if randint(0,99) < 10: board.spawn_enemyship()
		if not board.run(move,shoot) : 
			game_over(win,board)
			render_screen(win,board)
			x =ExitQuery(True)
			if x :
				win.close()
				return x , None
			win,board = reset_window(win,board_size)
			continue
		if randint(0,99) < 10:
			board.enemy_shoot()
		render_screen(win,board)
		win.refresh()
		t1 = perf_counter()-t0
		while( t1< DELAY) : t1 = perf_counter()-t0

if __name__ == '__main__':
	run()

