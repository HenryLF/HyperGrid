import PySimpleGUI as sg
from itertools import product
from .rules.NineQueens import Game
from .img.icon_44px import icon_44px
from .utils.Grid import GridElement
from .utils.GameExitCode import ExitCode,ExitQuery
sg.theme('DarkAmber')
BOARDSIZE = 8
DICT = {
'enable_events' : True,
'expand_x' : True
}
symbols = list(icon_44px.keys())

GREEN = '#2ec27e'
GREY = '#B3B3B3'
RED = "#E05656"
WHITE = '#ffffff'
def layout(board_size: int) -> list:
	return [
	[GridElement(board_size,cell_size = 44,key = 'BOARD')],
	[sg.Text('Board Size : '),sg.Combo(k='SIZE',default_value = board_size,values = [i for i in range(20)] ,**DICT)],
	[sg.Text('Symbol :'),sg.Combo(k='SYMBOL',default_value = symbols[0],values = symbols ,**DICT)],
	[sg.Button('Reset',k='RESET',**DICT),sg.Button('Quit',k='QUIT',**DICT)]
		]


def reset_window(win : sg.Window or None, board_size : int):
	if win : win.close()
	win = sg.Window('9Queens',layout(board_size),finalize = True)
	for i,j in product(range(board_size),range(board_size)):
		if (i+j)%2 : win['BOARD'].color_cell(i,j,GREY)
	board = Game(board_size)
	return win,board



def run(Player = None):
	board_size = BOARDSIZE
	symbol = symbols[0]
	win, board = reset_window(None,board_size)
	while(True):
		ev, val = win.read()
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
			case 'BOARD' :
				board[*val[ev]] = not board[*val[ev]]
				print(board)
				if board[*val[ev]] :
					 win[ev].draw_cell(*val[ev],data = icon_44px[symbol])
				else : 
					win[ev].erase_cell(*val[ev])
					win['BOARD'].color_cell(*val[ev],GREY if (val[ev][0]+val[ev][1])%2 else WHITE)
			case 'SYMBOL' :
				try :
					refresh_window(win,board,val[ev])
					symbol = val[ev]
				except KeyError : win[ev].update(value = symbol)
			case 'SIZE' : 
				try : board_size = int(val[ev])
				except ValueError : win[ev].update(value = board_size)
		for q in board.queens :
			if board.valid(q) : win['BOARD'].color_cell(*q,GREEN)
			else : win['BOARD'].color_cell(*q,RED)
if __name__ == '__main__':
	run()


