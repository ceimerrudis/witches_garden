from Game_Data import Game_Data

class Game_Action_Wrapper():
	# This class exists so the amount of references to game data would be limited 
	# as well as spliting the parameter tuple
	game_data = None

	def __init__(self, game_data):
		self.game_data = game_data

	def Plant(self, params):
		self.game_data.Plant(params[0], params[1], params[2])

	def Up_Root(self, params):
		self.game_data.Up_Root(params[0], params[1])
		
	def Undo(self):
		self.game_data.Undo()