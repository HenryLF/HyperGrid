from enum import Enum
import PySimpleGUI as sg
class ExitCode(Enum):
	RETURN = 0
	RESUME = 1
	REFRESH = 2
	QUIT = 3

BUTTONS = {
'expand_x' : True,
'enable_events' : True,
}
def layout(cancel : bool):
	l = [
[sg.Text('Quit or Go to Menu ?')],
[sg.Button('Quit',k='Quit'),
sg.Button('Menu',k='Menu') ]
	]
	if cancel : l[-1] += [sg.Button('Cancel',k='Cancel')]
	return l

def ExitQuery(cancel : bool = False):
	win = sg.Window('',layout(cancel),finalize = True)
	ev,val = win.read()
	win.close()
	match ev :
		case 'Quit' :
			return ExitCode(3)
		case 'Menu' :
			return ExitCode(0)
		case _ :
			return None
