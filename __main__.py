import PySimpleGUI as sg
from enum import Enum,EnumType
from Games.utils.GameExitCode import ExitCode
from ScoreBoard import Scoreboard
NCOLUMN = 2
GAMELIST = [
'TicTacToe',
'HyperTTT',
'Minesweeper',
'PixelArt',
'ConwaysLife',
'NineQueens',
'Gridius'
]
GRAPH = {
'canvas_size' : (300,125),
'graph_bottom_left' : (0,0),
'graph_top_right' : (300,125),
'enable_events' : True
}
def set_window(window : sg.Window or None = None) -> sg.Window :
	if window : window.close()
	Layout = [
	[sg.Graph(k = game,**GRAPH)]
	for i,game in enumerate(GAMELIST)
	]
	win = sg.Window('Menu',Layout,finalize =True)
	for k in GAMELIST :
		win[k].draw_image(filename = f'./Games/img/{k}.png',location = (0,125) )
	return win
#for k in window.key_dict :
#	x,y = int(k[-2]),int(k[-1])
#	if (x//3 + y//3)%2 == 1 :
#		window[k].update(background_color = 'red')

def run(Players : EnumType or None = None) :
	window = set_window()
	scoreboard = Scoreboard(Players)
	while(True):
		if scoreboard.was_closed() : scoreboard = Scoreboard(scoreboard)
		ev, val = window.read()
		window.close()
		match ev :
			case sg.WINDOW_CLOSED | "Cancel" : break
			case 'TicTacToe' : import Games.TicTacToe as PLAY 
			case 'HyperTTT' : import Games.HyperTTT as PLAY 
			case 'Minesweeper' : import Games.Minesweeper as PLAY 
			case 'PixelArt' : import Games.PixelArt as PLAY
			case 'ConwaysLife' : import Games.ConwaysLife as PLAY
			case 'NineQueens' : import Games.NineQueens as PLAY
			case 'Gridius' : import Games.Gridius as PLAY
		while(True):
			ExCode , winner = PLAY.run(Players) 
			match ExCode :
				case x if x == ExitCode(0) :
					window = set_window()
					break
				case x if x == ExitCode(1) :
					scoreboard.add(winner)
					continue
				case x if x == ExitCode(2) :
					continue
				case x if x == ExitCode(3) :
					return 0
	window.close()
	return 0

if __name__ == '__main__':
	print(run())


