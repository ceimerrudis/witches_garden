from Input_System import Input_System
from Enums import Plant_Type

class Plant():
	plant_type = None
	age = None
	light = None
	water = None
	charge = None
	bugs = None
	poison = None
	flags = None

	def __init__(self):
		self.plant_type = Plant_Type.grass1
		self.age = 0
		self.flags = {}
		self.light = 0
		self.water = 0
		self.charge = 0
		self.bugs = 0
		self.poison = 0

	def __str__(self):
		return "Plant " + str(self.plant_type) + " age " + str(self.age) + " flags " + str(self.flags) + "."

def Get_Field(num):
	if num == 0:
		return [
		(3, 8),
		(4, 8),
		(5, 8),
			  
		(1, 7),
		(7, 7),
			  
		(4, 6),
			  
		(0, 5),
		(3, 5),
		(4, 5),
		(5, 5),
		(8, 5),
			  
		(0, 4),
		(2, 4),
		(3, 4),
		(4, 4),
		(5, 4),
		(6, 4),
		(8, 4),
			  
		(0, 3),
		(3, 3),
		(4, 3),
		(5, 3),
		(8, 3),
			 
		(4, 2),
			  
		(1, 1),
		(7, 1),
			 
		(3, 0),
		(4, 0),
		(5, 0)]
	else:
		return []

class Game_Data():
	action_q = None
	field_size_x = None
	field_size_y = None
	game_field = None
	seeds = None
	camera_pos = None
	initialized = None

	def __init__(self):
		self.action_q = []
		self.field_size_x = 9
		self.field_size_y = 9
		self.camera_pos = [0, 16]
		self.initialized = False

	def Initialize(self):
		self.game_field = [[{"plant": Plant(), "growable": False } for i in range(self.field_size_y)] for j in range(self.field_size_x)]
		field = Get_Field(0)

		for item in field:
			self.Set_New_Plant(self.game_field[item[0]][item[1]]["plant"], Plant_Type.plot)
			self.game_field[item[0]][item[1]]["growable"] = True

		self.AddSeeds()
		self.initialized = True

	def AddSeeds(self, seed_dict = None):
		if not seed_dict == None:
			self.seeds = seed_dict
		else:
			self.seeds = {}
			for i in range(5):
				self.seeds[Plant_Type(i + 6)] = 6 + i

	def Set_New_Plant(self, plantToSet, plantType):
		plantToSet.age = 0
		plantToSet.plant_type = plantType
		plantToSet.flags = {}
		return plantToSet
	
	def End_Turn(self):
		for row in self.game_field:
			for plant in row:
				plant["plant"].age += 10
		self.action_q.clear()

	def Plant(self, target_x, target_y, seed_type):
		if not ((target_x < len(self.game_field) and target_x >= 0) and (target_y < len(self.game_field[target_x]) and target_y >= 0)):
			return
		if self.game_field[target_x][target_y]["growable"] == False:
			print("ilegal action")
			return
		if not self.game_field[target_x][target_y]["plant"].plant_type == Plant_Type.plot:
			print("cant plant on top of other plants")
			return
		if not seed_type in self.seeds.keys():
			print("seed not found")
			return 
		if self.seeds[seed_type] <= 0:
			print("out of seeds")
			return

		self.action_q.append(("planted", target_x, target_y, self.game_field[target_x][target_y]["plant"], seed_type, -1))
		plant = self.Set_New_Plant(Plant(), seed_type)
		self.Change_Seed_Amount(seed_type, -1)
		self.game_field[target_x][target_y]["plant"] = plant	

	def Up_Root(self, target_x, target_y):
		if not ((target_x < len(self.game_field) and target_x >= 0) and (target_y < len(self.game_field[target_x]) and target_y >= 0)):
			return	

		if self.game_field[target_x][target_y]["growable"] == False:
			return
		plant = self.Set_New_Plant(Plant(), Plant_Type.plot)
		self.action_q.append(("removed", target_x, target_y, self.game_field[target_x][target_y]["plant"]))
		self.game_field[target_x][target_y]["plant"] = plant

	def Undo(self):
		if len(self.action_q) <= 0:
			print("nothing in the q")
			return
		if self.action_q[-1][0] == "removed":
			pos_x = self.action_q[-1][1]
			pos_y = self.action_q[-1][2]
			old_plant = self.action_q[-1][3]	
		
			self.game_field[pos_x][pos_y]["plant"] = old_plant
		elif self.action_q[-1][0] == "planted":
			seed_type = self.action_q[-1][4]
			seed_amount = self.action_q[-1][5]
			pos_x = self.action_q[-1][1]
			pos_y = self.action_q[-1][2]
			old_plant = self.action_q[-1][3]

			self.Change_Seed_Amount(seed_type, -seed_amount)
			self.game_field[pos_x][pos_y]["plant"] = old_plant
		else:
			print("Action not recognized")
		self.action_q.pop()

	def Change_Seed_Amount(self, seed_type, amount):
		self.seeds[seed_type] += amount
		if self.seeds[seed_type] <= 0:
			self.seeds.pop(seed_type)

	def Get_Plant(self, x, y):
		if x < self.field_size_x and x >= 0 and y < self.field_size_y and y >= 0:
			return self.game_field[x][y]["plant"]

	def update(self, inputs):
		camera_pos_change = [0, 0]
		if(inputs.spectator_mode.w() >= 2):
			camera_pos_change[1] += -2
		if(inputs.spectator_mode.s() >= 2):
			camera_pos_change[1] +=  2
		if(inputs.spectator_mode.a() >= 2):
			camera_pos_change[0] += -2
		if(inputs.spectator_mode.d() >= 2):
			camera_pos_change[0] +=  2
		self.camera_pos[0] += camera_pos_change[0]
		self.camera_pos[1] += camera_pos_change[1]

		if inputs.garden.end_turn() == 2:
			self.End_Turn()