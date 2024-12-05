import PySimpleGUI as sg
from enum import EnumType,Enum
#absolute import
if __name__ == '__main__':
	from rules.TicTacToe import Board
	from utils.Player import DefaultPlayer
	from utils.Grid import GridElement
	from utils.GameExitCode import ExitCode,ExitQuery
	from img.icon_132px import icon_132px
	
else : #relative import
	from .rules.TicTacToe import Board
	from .utils.Player import DefaultPlayer
	from .utils.Grid import GridElement
	from .utils.GameExitCode import ExitCode, ExitQuery
	from .img.icon_132px import icon_132px

sg.theme('DarkAmber')
GREY ='#deddda'
DICT = {
'enable_events' : True,
'expand_x' : True
}
c = list(icon_132px.keys())
BOARD_SIZE = 3
CELL_SIZE = 132

def layout(player : EnumType) -> list :
	Column2 = [
	[sg.Text(p.name + ':'),sg.Combo(k=p.name,default_value = c[i],values = c ,**DICT)]
	for i,p in enumerate(player) ] +[ 
	[sg.Text('Size:'),sg.Combo(k='SIZE', default_value = BOARD_SIZE,values = [2*i+1 for i in range(1,5)] ,**DICT)] ,
	[sg.Button('Reset',k='RESET',**DICT),sg.Button('Quit',k='QUIT',**DICT)]
	]
	return [[
	GridElement(BOARD_SIZE,CELL_SIZE,key = 'BOARD'),
	sg.Column(Column2)
	]]



def refresh_board(window : sg.Window,board : Board, val : dict) -> None:
	for i,row in enumerate(board.g) :
		for j,cell in enumerate(row):
			window['BOARD'].erase_cell(i,j)
			window['BOARD'].draw_cell(i,j,data = icon_132px[val[cell.name]])

def reset_window(player : EnumType, window : sg.Window or None = None) -> (sg.Window , Board):
	Turn = 0
	if window : window.close()
	window = sg.Window('TicTacToe',layout(player),finalize = True)
	for i in range(0,BOARD_SIZE) :
		for j in range(0,BOARD_SIZE):
			if (i+j)%2 ==1 : window['BOARD'].color_cell(i,j,GREY)
	return window, Board(BOARD_SIZE)

def run(player : EnumType or None  = None,board_size : int or None = None) -> (ExitCode, Enum or None) :
	BOARD_SIZE = 3 if board_size is None else board_size
	Player = DefaultPlayer if player is None else player
	Turn = 0
	window,board = reset_window(Player,None)
	while(True):
		ev,val = window.read()
		print(ev,val)
		current_Player = Player(Turn%2)
		if Turn == BOARD_SIZE**2 : 
			Turn = 0
			window, board = reset_window(Player,window)
		match ev :
			case sg.WINDOW_CLOSED | 'Cancel' : 
				window.close()
				return ExitQuery() , None 
				window,board = reset_window(Player,window)
			case 'RESET' : 
				window, board = reset_window(Player,window)
			case 'QUIT':
				x = ExitQuery(True)
				if x : 
					window.close() 
					return x, None
			case 'BOARD' :
				if board.play(*val[ev],current_Player) :
					window[ev].draw_cell( *val[ev],data = icon_132px[val[current_Player.name]])
					Turn +=1
			case current_Player.name  :
				refresh_board(window,board,val)
				continue
			case 'SIZE' :
				BOARD_SIZE = val[ev]
		if board.check() :
			win = sg.Window('POP',[[sg.Text(f'{board.check().name} won !')]],keep_on_top = True,finalize = True)
			win.read()
			win.close()
			window.close()
			return ExitCode(1) , board.check()

if __name__ == '__main__':
	while(True):
		match run() :
			case ExitCode(3) | ExitCode(0): break



