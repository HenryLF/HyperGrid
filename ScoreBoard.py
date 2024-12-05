import PySimpleGUI as sg
from enum import EnumType,Enum
from Games.utils.Player import DefaultPlayer
DICT = {
'expand_x' : True
}
class Scoreboard(sg.Window):
	kwarg = {
	'title' : 'Scoreboard',
	'finalize' : True,
	}
	def __init__(self,Players : EnumType or Scoreboard or None = None,**kw) :
		if isinstance(Players,Scoreboard) : self.Players = Players.Players
		else : self.Players=Players if Players else DefaultPlayer
		self.scores = { p : 0 for p in self.Players}
		Layout = [
		[
		sg.Text(f'{p.name} :',**DICT),
		sg.Text(f'{self.scores[p]}',k = p,**DICT), 
		] for p in self.Players
		]
		kw.update(self.kwarg)
		super().__init__(layout = Layout,**kw)
	
	def add(self,player : Enum or None) :
		if not player : return
		self.scores[player]+=1
		self[player].update(value = f'{self.scores[player]} :')
	
	def reset_score(self,player : Enum or None = None):
		if player :
			for p in self.Players :
				self.scores[p] = 0
				self[p].update(value = f'{self.scores[p]}')
		else :
			self.scores[player]+=1
			self[player].update(value = f'{self.scores[p]}')
