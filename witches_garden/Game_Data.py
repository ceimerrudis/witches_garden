from Input_System import Input_System
from Plant_Info import *
import random

class Plant():
	# The main data class holds the info about a particular planted plant
	plant_type = None # See enum in Plant_Info
	age = None # integer from 0 - 100 (all plants die at age 100)
	temperature = None # int
	light = None # int
	water = None # int
	charge = None # int parameter like tempereture except mesures magic resedue
	bugs = None # int
	poison = None # int
	flags = None # currenly unused but could be used to set on fire etc.

	def __init__(self):
		self.plant_type = Plant_Type.grass1
		self.age = 0
		self.flags = {}
		self.light = 0
		self.temperature = 0
		self.water = 0
		self.charge = 0
		self.bugs = 0
		self.poison = 0

	def __str__(self):
		# for easy debuging
		return "Plant " + str(self.plant_type) + " age " + str(self.age) + " flags " + str(self.flags) + "."

def Get_Field(num):
	# essentialy a level selector but has just 1 level
	if num == 0:
		return ([ # all plantable spots
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
		(5, 0)], # end of plantable spots

		[
		(4, 0), # all magic circle spots IN ORDER
		(5, 0),
		(7, 1),
		(8, 3),
		(8, 4),
		(8, 5),
		(7, 7),
		(5, 8),
		(4, 8),
		(3, 8),
		(1, 7),
		(0, 5),
		(0, 4),
		(0, 3),
		(1, 1),
		(3, 0),# end of magic circle
		],
		9, 9, # field size
		
		{ "temperature": 20, "light": 30, "water": 20, "charge": 0, "bugs": 0, "poison": 0, "flags": {} }
		# conditions that the enviorment tries to enforce
		)
	else:
		return None

def Apply_Effects(effects, plant):
	#applies the given effects to the designated tile
	# the list must include all attributes
	plant.temperature += effects["temperature"]
	plant.light += effects["light"]
	if plant.light < 0:
		plant.light = 0
	plant.water += effects["water"]
	if plant.water < 0:
		plant.water = 0
	plant.charge += effects["charge"]
	if plant.charge < 0:
		plant.charge = 0
	plant.poison += effects["poison"]
	if plant.poison < 0:
		plant.poison = 0
	plant.bugs += effects["bugs"]
	if plant.bugs < 0:
		plant.bugs = 0
	plant.flags = { k: plant.flags.get(k, 0) + effects["flags"].get(k, 0) for k in set(plant.flags) | set(effects["flags"]) }

def Calculate_Growth(plant, optimal_conditions):
	# calculates growth according to the plants optimal_conditions 
	growth = 60
	growth -= abs(plant.temperature - optimal_conditions["temperature"])
	growth -= abs(plant.light - optimal_conditions["light"])
	growth -= abs(plant.water - optimal_conditions["water"])
	growth -= abs(plant.charge - optimal_conditions["charge"])
	growth -= abs(plant.poison - optimal_conditions["poison"])
	growth -= abs(plant.bugs - optimal_conditions["bugs"])

	if growth < 0:
		growth = 0 
	if growth > 20:#limit growth 
		growth = 20
	return growth

class Game_Data():
	# This class holds and changes the game data
	action_q = None # this turns actions stored so they can be undone
	field_size_x = None # map size
	field_size_y = None
	game_field = None # list of lists where each place is a 2 item dictionary
	seeds = None # dictionary of players seeds and their amounts
	camera_pos = None # used by main to update the actual camera
	initialized = None # bool that makes sure no updates run on  half empty class
	magic_circle = None # lsit of coordinates for the magic circle positions
	score = None # player score
	outside_conditions = None # the conditions the enviorment tries to enforce

	def __init__(self):
		self.action_q = []
		self.camera_pos = [0, 16]
		self.initialized = False
		self.score = 0

	def Initialize(self, lv = 0):
		# loads the level and fills the empty data fields
		field_obj = Get_Field(lv)
		self.field_size_x = field_obj[2]
		self.field_size_y = field_obj[3]
		self.game_field = [[{"plant": Plant(), "growable": False } for i in range(self.field_size_y)] for j in range(self.field_size_x)]
		field = field_obj[0]
		self.magic_circle = field_obj[1]
		self.outside_conditions = field_obj[4]
		for item in field:
			# create empty plots
			self.Set_New_Plant(self.game_field[item[0]][item[1]]["plant"], Plant_Type.plot)
			self.game_field[item[0]][item[1]]["growable"] = True
	
		# use random generation to create seeds
		self.AddSeeds()
		self.initialized = True

	def AddSeeds(self, seed_dict = None):
		# has 2 modes random gen and set mode when the list of seeds is known
		if not seed_dict == None:
			self.seeds = seed_dict
		else:
			self.seeds = {}
			seed_types = list(Plant_Type)
			for i in range(30):
				# add 30 seeds each seed randomly picked from allowed ones
				seed_type = Plant_Type.plot
				while seed_type == Plant_Type.plot or seed_type == Plant_Type.grass1 or seed_type == Plant_Type.grass2 or seed_type == Plant_Type.grass3 or seed_type == Plant_Type.grass4:
					seed_type = random.choice(seed_types)
				
				if Plant_Type(seed_type) in self.seeds.keys():
					self.seeds[Plant_Type(seed_type)] += 1
				else:
					self.seeds[Plant_Type(seed_type)] = 1

	def Relay(self, effects, pos, passed = []):
		# relay a magic circle effect through relay plants
		for item in passed:
			if item == pos:
				return #Already checked this relay

		if not len(passed) == 0:#So as not to apply the same effect twice on the starting relay
			Apply_Effects(effects, self.game_field[pos[0]][pos[1]]["plant"])
			
		# different patterns for the three relay plants are described hear

		if self.game_field[pos[0]][pos[1]]["plant"].plant_type == Plant_Type.hrelay:
			passed.append(pos)
			for i in range(pos[0], 0, -1):
				self.Relay(effects, (i, pos[1]), passed)
			for i in range(pos[0], self.field_size_x, +1):
				self.Relay(effects, (i, pos[1]), passed)
		
		if self.game_field[pos[0]][pos[1]]["plant"].plant_type == Plant_Type.drelay:
			passed.append(pos)
			i = pos[0] - 1
			j = pos[1] - 1
			while i >= 0 and j >= 0:
				self.Relay(effects, (i, j), passed)
				i += -1
				j += -1

			i = pos[0] - 1
			j = pos[1] + 1
			while i >= 0 and j < self.field_size_y:
				self.Relay(effects, (i, j), passed)
				i += -1
				j +=  1 

			i = pos[0] + 1
			j = pos[1] + 1
			while i < self.field_size_x and j < self.field_size_y:
				self.Relay(effects, (i, j), passed)
				i +=  1
				j +=  1 

			i = pos[0] + 1
			j = pos[1] - 1
			while i < self.field_size_x and j >= 0:
				self.Relay(effects, (i, j), passed)
				i +=  1
				j += -1 

		if self.game_field[pos[0]][pos[1]]["plant"].plant_type == Plant_Type.brelay:
			passed.append(pos)	
			for i in range(3):
				for j in range(3):
					x = pos[0] + i - 1
					y = pos[1] + j - 1
					self.Relay(effects, (x, y), passed)

	def Set_New_Plant(self, plantToSet, plantType):
		# sets the default stats for a new plant
		plantToSet.age = 0
		plantToSet.temperature = 20
		plantToSet.charge = 0
		plantToSet.water = 30
		plantToSet.light = 30
		plantToSet.bugs = 0
		plantToSet.poison = 0
		plantToSet.plant_type = plantType
		plantToSet.flags = {}
		return plantToSet
	
	def End_Turn(self):
		# Does multiple things:
			# 1 applies envo=iorments effects and mkes plants grow 
			# 2 clears the undo queue
			# 3 applies magic circle spells
		
		# 1
		for i in range(len(self.game_field)):
			for j in range(len(self.game_field[i])):
				plant = self.game_field[i][j]
				
				plant["plant"].temperature -= int((plant["plant"].temperature - self.outside_conditions["temperature"]) / random.randint(3, 5))
				plant["plant"].charge -= int((plant["plant"].charge - self.outside_conditions["charge"]) / random.randint(3, 5))
				plant["plant"].light -= int((plant["plant"].light - self.outside_conditions["light"]) / random.randint(3, 5))
				plant["plant"].water -= int((plant["plant"].water - self.outside_conditions["water"]) / random.randint(3, 5))
				plant["plant"].poison -= int((plant["plant"].poison - self.outside_conditions["poison"]) / random.randint(3, 5))
				plant["plant"].bugs -= int((plant["plant"].bugs - self.outside_conditions["bugs"]) / random.randint(3, 5))
				
				plant["plant"].water += random.randint(-5, 5)
				plant["plant"].light += random.randint(-5, 5)
				plant["plant"].temperature += random.randint(-5, 5)

				conditions = Get_Plant_Conditions(plant["plant"].plant_type)
				growth = Calculate_Growth(plant["plant"], conditions)

				age_before = plant["plant"].age #Used when calling effects
				plant["plant"].age += growth

				Get_Plant_Event(self, plant["plant"], i, j, age_before)
		
		# 2		
		self.action_q.clear()

		# 3
		effects = Get_Plant_Effect(None)
		for item in self.magic_circle:
			#apply effects to tile
			Apply_Effects(effects, self.game_field[item[0]][item[1]]["plant"])

			plant_t = self.game_field[item[0]][item[1]]["plant"].plant_type
			if plant_t == Plant_Type.hrelay or plant_t == Plant_Type.brelay or plant_t == Plant_Type.drelay:
				self.Relay(effects, item, [])
				effects = Get_Plant_Effect(None)
				additional_eff = effects
			else:
				additional_eff = Get_Plant_Effect(plant_t, self.game_field[item[0]][item[1]]["plant"].age)
			
			#add this tiles effects to the pile
			effects["temperature"] += additional_eff["temperature"]
			effects["light"] += additional_eff["light"]
			effects["water"] += additional_eff["water"]
			effects["charge"] += additional_eff["charge"]
			effects["bugs"] += additional_eff["bugs"]
			effects["poison"] += additional_eff["poison"]
			effects["flags"] = { k: effects["flags"].get(k, 0) + additional_eff["flags"].get(k, 0) for k in set(effects["flags"]) | set(additional_eff["flags"]) }

	def Plant(self, target_x, target_y, seed_type):
		# Plants the given seed(plant)_type in the given spot
		
		if not ((target_x < len(self.game_field) and target_x >= 0) and (target_y < len(self.game_field[target_x]) and target_y >= 0)):
			return # out of bounds
		
		if self.game_field[target_x][target_y]["growable"] == False:
			return # planting on an unplantable location

		if not self.game_field[target_x][target_y]["plant"].plant_type == Plant_Type.plot:
			return # trying to plant on top of other plants
		
		if not seed_type in self.seeds.keys():
			return # seed not found
		
		if self.seeds[seed_type] <= 0:
			return # out of seeds

		#add to undo q
		self.action_q.append(("planted", target_x, target_y, self.game_field[target_x][target_y]["plant"], seed_type, -1))
		
		# override previous plant
		plant = self.Set_New_Plant(Plant(), seed_type)
		self.Change_Seed_Amount(seed_type, -1)
		self.game_field[target_x][target_y]["plant"] = plant	

	def Up_Root(self, target_x, target_y):
		# Destroys the plant at specified location
		if not ((target_x < len(self.game_field) and target_x >= 0) and (target_y < len(self.game_field[target_x]) and target_y >= 0)):
			return # out of bounds

		if self.game_field[target_x][target_y]["growable"] == False:
			return # cant uproot grass

		plant = self.Set_New_Plant(Plant(), Plant_Type.plot)
		# add to undo q
		self.action_q.append(("removed", target_x, target_y, self.game_field[target_x][target_y]["plant"]))
		self.game_field[target_x][target_y]["plant"] = plant

	def Undo(self):
		# goes back one step in the q
		if len(self.action_q) <= 0:
			return # q is empty
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
		pass
		# I used to want hotkeys but now the game is mouyse only so the update is empty
		"""camera_pos_change = [0, 0]
		if(inputs.spectator_mode.w() >= 2):
			camera_pos_change[1] += -2
		if(inputs.spectator_mode.s() >= 2):
			camera_pos_change[1] +=  2
		if(inputs.spectator_mode.a() >= 2):
			camera_pos_change[0] += -2
		if(inputs.spectator_mode.d() >= 2):
			camera_pos_change[0] +=  2
		self.camera_pos[0] += camera_pos_change[0]
		self.camera_pos[1] += camera_pos_change[1]"""

		#if inputs.garden.end_turn() == 2:
			#self.End_Turn()