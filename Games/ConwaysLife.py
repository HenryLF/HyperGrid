from .utils.Grid import GridElement
from .rules.Conway import Game
from .utils.GameExitCode import ExitCode,ExitQuery
from time import sleep
import PySimpleGUI as sg
BOARD_SIZE = (100,50)
CELL_SIZE = (10,10)
ALIVE_COLOR = '#23c45e'
DEAD_COLOR = '#55665c'
SPEED = 1
DICT = {
'enable_events': True
}
def layout(board_size : tuple, cell_size : tuple,speed : int):
	return [
	[GridElement(board_size,cell_size = cell_size,key = 'BOARD',background_color = DEAD_COLOR,drag_submits = True),
	sg.Column([
	[sg.Text('Current living cells:'),sg.Text(0 , k = 'LIVE',font = ('Courier' ,42 ) ),sg.Text('',k='MAX')],
	[sg.Text('Cell size :'),sg.Slider(k = 'CELL',range = (10,50),default_value = cell_size[0],resolution = 5,orientation = 'h',**DICT)	],
	[sg.Text('Universe size :'),sg.Combo(k='SIZEX',default_value = board_size[0],values = [i for i in range(5,201,5)],**DICT),
	sg.Text(' x '),sg.Combo(k='SIZEY',default_value = board_size[1],values = [i for i in range(5,201,5)],**DICT)],
	[sg.Text('Speed:'), sg.Slider(k='SPEED',range = (1,10),resolution = 1, default_value = 1,orientation = 'h',**DICT)],
	[sg.Button('Run',k='RUN',**DICT),sg.Button('Step',k='STEP',**DICT),sg.Button('Reset',k='RESET',**DICT),sg.Button('Quit',k='QUIT',**DICT)],
	[sg.Checkbox('KILL CELL',k='KILL',**DICT)]
		])
	]]


def run(Player):
	speed = SPEED
	cell_size = CELL_SIZE
	board_size = BOARD_SIZE
	window = sg.Window("Conway's Life",layout = layout(board_size,cell_size,speed),finalize  = True)
	conway = Game(board_size)
	while(True):
		ev,val = window.read()
		if ev == sg.WINDOW_CLOSED : window.close()
		print(ev,val)
		match ev :
			case sg.WINDOW_CLOSED  : 
				return ExitQuery() , None 
			case 'QUIT':
				x = ExitQuery(True)
				if x : 
					window.close() 
					return x, None
			case 'RESET' :
				window.close()
				window = sg.Window("Conway's Life",layout = layout(board_size,cell_size,speed),finalize  = True)
				conway = Game(board_size)
			case 'SPEED': speed = int(val[ev])
			case 'BOARD' :
				conway[*val[ev]] = False if val['KILL'] else True
				window[ev].color_cell(*val[ev], ALIVE_COLOR if conway[*val[ev]] else DEAD_COLOR)
				window['LIVE'].update(value = f'{conway.live_cell_count}')
			case 'SIZEX' : 
				try : board_size= (int(val[ev]),board_size[1])
				except ValueError : window[ev].update(value = board_size[0])
			case 'SIZEY' : 
				try : board_size = (board_size[0],int(val[ev]))
				except ValueError : window[ev].update(value = board_size[1])
			case 'CELL' :
				try : cell_size = (int(val[ev]),int(val[ev]))
				except ValueError : window[ev].update(value = cell_size)
			case 'RUN' :
				window[ev].update(text = 'STOP')
				while(conway.active_cells):
					if window.read(timeout = 1000/speed,timeout_key = None )[0] == 'RUN' : break
					update = conway.update_cells()
					for coord , state in update.items():
						window['BOARD'].color_cell(*coord, ALIVE_COLOR if state else DEAD_COLOR)
					window['LIVE'].update(value = f'{conway.live_cell_count}')
					window['MAX'].update(value = f'(Max : {conway.max_living_cells})')
					window.refresh()
				window[ev].update(text = 'RUN')
			case 'STEP':
				update = conway.update_cells()
				for coord , state in update.items():
					window['BOARD'].color_cell(*coord, ALIVE_COLOR if state else DEAD_COLOR)
				
