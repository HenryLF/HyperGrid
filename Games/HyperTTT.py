import PySimpleGUI as sg
from itertools import product
from enum import EnumType,Enum
#absolute import
if __name__ == '__main__':
	from rules.HyperTTT import HyperBoard
	from utils.Player import DefaultPlayer
	from utils.Grid import GridElement
	from utils.GameExitCode import ExitCode,ExitQuery
	from img.icon_132px import icon_132px
	from img.icon_44px import icon_44px
else :
	from .rules.HyperTTT import HyperBoard
	from .utils.Player import DefaultPlayer
	from .utils.Grid import GridElement
	from .utils.GameExitCode import ExitCode,ExitQuery
	from .img.icon_132px import icon_132px
	from .img.icon_44px import icon_44px

sg.theme('DarkAmber')
GREY ='#a6a6a6'
WHITE2 ='#DAE4ED'
GREY2 = '#A6C4DF'
DICT = {
'enable_events' : True,
'expand_x' : True
}
c = list(icon_132px.keys())
BOARD_SIZE = 3
CELL_SIZE = 44


def layout(player : EnumType) -> list:
	Row2 = [
	[sg.Text(p.name+': '),sg.Combo(k=p.name,default_value = c[i],values = c ,**DICT)]
	for i,p in enumerate(player)
	] + [sg.Button('Reset',k='RESET',**DICT),sg.Button('Quit',k='QUIT',**DICT)]
	return [
	[GridElement(BOARD_SIZE**2,cell_size = CELL_SIZE,key = 'BOARD')],
	[Row2]
	]

def refresh_board(window : sg.Window,board : HyperBoard,val : dict) -> None:
	for k , l in product(range(BOARD_SIZE**2),range(BOARD_SIZE**2)):
		I,J , i, j = k//BOARD_SIZE, l//BOARD_SIZE , k%BOARD_SIZE , l%BOARD_SIZE
		if not board[I][J][i][j] : continue
		window['BOARD'].erase_cell(k,l)
		window['BOARD'].draw_cell(k,l, data = icon_44px[val[board[I][J][i][j].name]])
	render_big_grid(window,board,val)

def reset_window(player : EnumType, window : sg.Window or None = None) -> (sg.Window , HyperBoard):
	if window : window.close()
	window= sg.Window('HyperTicTacToe',layout(player),finalize = True)
	for i , j in product(range(BOARD_SIZE**2),range(BOARD_SIZE**2)):
		if (i+j)%2 ==1 : 
			if (i//BOARD_SIZE + j // BOARD_SIZE)%2 :
				window['BOARD'].color_cell(i,j,GREY)
				continue
			window['BOARD'].color_cell(i,j, GREY2)
			continue
		elif (i//BOARD_SIZE + j // BOARD_SIZE)%2:
			window['BOARD'].color_cell(i,j, WHITE2)
	return window, HyperBoard(BOARD_SIZE)

def render_big_grid(window : sg.Window , board : HyperBoard, val : dict) -> None:
	for I,J in product(range(BOARD_SIZE) ,range(BOARD_SIZE)):
		if not board.hyper_board[I][J] : continue
		for i,j in product(range(BOARD_SIZE) ,range(BOARD_SIZE)): window['BOARD'].erase_cell(I*BOARD_SIZE+i,J*BOARD_SIZE+j)
		window['BOARD'].draw_image(data = icon_132px[val[board.hyper_board[I][J].name]], location = (I*CELL_SIZE*BOARD_SIZE,(J+1)*CELL_SIZE*BOARD_SIZE))

def run(player : EnumType or None  = None) -> (ExitCode , Enum):
	Player = DefaultPlayer if player is None else player
	Turn = 0
	window,board = reset_window(Player,None)
	while(True):
		ev,val = window.read()
		current_Player = Player(Turn%len(Player))
		if Turn == BOARD_SIZE**3 : 
			Turn = 0
			window.close()
			window , board = reset_window(window,Player)
		match ev :
			case sg.WINDOW_CLOSED | 'Cancel' : 
				return ExitQuery() , None
			case 'RESET' : 
				window, board = reset_window(Player,window)
				Turn = 0
			case 'QUIT':
				x =ExitQuery(True)
				if x :
					window.close()
					return x , None
			case 'BOARD' :
				if board.play(*val[ev],current_Player) :
					window['BOARD'].draw_cell(*val[ev],data = icon_44px[val[current_Player.name]])
					Turn +=1
			case current_Player.name :
				refresh_board(window, board, val)
		render_big_grid(window,board,val)
		x = board.check()
		if board.check() :
			win = sg.Window('POP',[[sg.Text(f'{board.check().name} won !')]],keep_on_top = True,finalize = True)
			win.read()
			win.close()
			window.close()
			return ExitCode(1), board.check()

if __name__ == '__main__':
	run()


