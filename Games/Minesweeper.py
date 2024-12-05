import PySimpleGUI as sg
from enum import EnumType
if __name__ == '__main__':
	from rules.Minesweeper import Minefield
	from utils.Player import DefaultPlayer
	from utils.Grid import GridElement
	from utils.GameExitCode import ExitCode,ExitQuery
	from img.icon_minesweeper import icon_minesweeper
else :
	from .rules.Minesweeper import Minefield
	from .utils.Player import DefaultPlayer
	from .utils.Grid import GridElement
	from .utils.GameExitCode import ExitCode,ExitQuery
	from .img.icon_minesweeper import icon_minesweeper

BOARD_SIZE = (10,10)
MINE_NUMBER = 8
CELL_SIZE = 44
DICT = {
'enable_events' : True,
'expand_x' : True
}
GREEN = '#2ec27e'
GREY = '#B3B3B3'

RED = "#E05656"
GAMEOVER ='You BLEW-UP !! TOO BAD :('
WIN_GAME = 'You just found all the mines ! GG !'
sg.theme('DarkAmber')

def layout(board_size : int or None = None,mine_number : int or None = None):
	board_size = board_size if board_size else BOARD_SIZE
	mine_number = mine_number if mine_number else MINE_NUMBER
	return [[
	GridElement(board_size,cell_size = (CELL_SIZE,CELL_SIZE),key = 'FIELD') ],
	[
	[sg.Button(k = 'DIG',button_text = 'DIG',disabled=True,**DICT),sg.Button(k = 'MARK',button_text = 'MARK',**DICT),sg.Button(k = 'UNMARK',button_text = 'UNMARK',**DICT)],
	[sg.Text('Size :'),sg.Combo(k='SIZEX',default_value = board_size[0],values = range(3,26),**DICT),
	sg.Text(' x '),sg.Combo(k='SIZEY',default_value = board_size[1],values = range(3,26),**DICT)],
	sg.Text('Mine number :'), sg.Combo(k='NMINE',default_value = mine_number, values = range(1,50),**DICT),
	[sg.Button('Reset',k='RESET',**DICT),sg.Button('Quit',k='QUIT',**DICT)]
	]
	]
	
def reset_window(win : sg.Window or None = None, board_size : int or None = None,mine_number : int or None = None) -> (sg.Window , Minefield,set):
	board_size = board_size if board_size else BOARD_SIZE
	mine_number = mine_number if mine_number else MINE_NUMBER
	if win: win.close()
	win = sg.Window('MinesweepaAAa',layout = layout(board_size,mine_number),finalize = True)
	field = Minefield(board_size,mine_number)
	render_all(win,field,GREY)
	return win,field,set()


def render_all(win : sg.Window,field : Minefield, color : str ) -> None:
	for i,_ in enumerate(field):
		for j,cell in enumerate(_):
			win['FIELD'].erase_cell(i,j)
			win['FIELD'].color_cell(i,j,color)
			win['FIELD'].draw_cell(i,j,data = icon_minesweeper[cell.value])

def render_field(win : sg.Window,field : Minefield) -> None:
	for (i,j) in field.played :
		win['FIELD'].erase_cell(i,j)
		win['FIELD'].draw_cell(i,j,data = icon_minesweeper[field[i][j].value])

def game_over(win : sg.Window, field : Minefield, i :int , j: int) -> None :
	render_all(win,field,RED)
	win['FIELD'].erase_cell(i,j)
	win['FIELD'].draw_cell(i,j,data = icon_minesweeper['Exploded'])
	popup = sg.Window('GAME OVER',layout =[[sg.Button(button_text = GAMEOVER,enable_events = True)]], finalize = True)
	popup.read()
	popup.close()
def mark(i,j,win : sg.Window,marked:set):
	marked.add((i,j))
	win['FIELD'].color_cell(i,j,RED)
	return marked

def unmark(i,j,win : sg.Window,marked:set):
	if (i,j) in marked :
		marked.remove((i,j))
		win['FIELD'].color_cell(i,j,GREY)
	return marked
	
def run(Players : EnumType or None = None) -> (ExitCode , None) :
	player = Player(0) if Players else DefaultPlayer.Player1
	win,field,marked = reset_window()
	DIG = 0
	while True :
		ev,val = win.read()
#		print(ev,win.key_dict )
		match ev :
			case sg.WINDOW_CLOSED | 'Cancel' : 
				return ExitQuery() , None
			case 'RESET' : 
				return ExitCode(2),None
			case 'QUIT':
				x =ExitQuery(True)
				if x :
					win.close()
					return x , None

			case 'FIELD' if DIG == 0 :
				x  = field.play(*val[ev])
				match x :
					case False : 
						game_over(win,field,*val[ev])
						win , field,marked = reset_window(win)
					case x if isinstance(x,str) : 
#						print(x)
						continue
					case True : render_field(win,field)
			
			case 'FIELD' if DIG == 1 :
				marked = mark(*val[ev],win,marked)
			case 'FIELD' if DIG == -1 :
				marked = unmark(*val[ev],win,marked)
			case 'MARK': 
				DIG = 1
				win['MARK'].update(disabled = True)
				win['DIG'].update(disabled = False)
				win['UNMARK'].update(disabled = False)
			case 'UNMARK' :
				DIG = -1 
				win['UNMARK'].update(disabled = True)
				win['MARK'].update(disabled = False)
				win['DIG'].update(disabled = False)
			case 'DIG' : 
				DIG = 0
				win['DIG'].update(disabled = False)
				win['MARK'].update(disabled = False)
				win['UNMARK'].update(disabled = False)
			case 'SIZEX':
				BOARDSIZE = (val[ev] , BOARDSIZE[1] )
			case 'SIZEY':
				BOARDSIZE = ( BOARDSIZE[0] ,  val[ev] ) 
			case 'NMINES' :
				MINE_NUMBER = val[ev]
#		print(marked,field.mines,marked == field.mines)
		if marked == field.mines:
			field = field.board
			render_all(win,field,GREEN)
			popup = sg.Window('GG YOU WON !!',layout =[[sg.Button(button_text = WIN_GAME,enable_events = True)]],keep_on_top = True, finalize = True)
			popup.read()
			popup.close()
			win.close()
			return ExitCode.REFRESH , None
	

if __name__ == '__main__':
	run()


