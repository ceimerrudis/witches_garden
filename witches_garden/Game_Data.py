from Input_System import Input_System
from Enums import Plant_Type
import random

class Plant():
	plant_type = None
	age = None
	temperature = None
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
		self.temperature = 0
		self.water = 0
		self.charge = 0
		self.bugs = 0
		self.poison = 0

	def __str__(self):
		return "Plant " + str(self.plant_type) + " age " + str(self.age) + " flags " + str(self.flags) + "."

def Get_Field(num):
	if num == 0:
		return ([
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
		(5, 0)], 

		[
		(4, 0),
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
		(3, 0),
		],
		9, 9,
		{ "temperature": 20, "light": 30, "water": 20, "charge": 0, "bugs": 0, "poison": 0, "flags": {} }
		)
	else:
		return []

def Apply_Effects(effects, plant):
	#applies the effects of the circle to the designated tile
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

def Get_Plant_Effect(plant_type, age = 0):
	if plant_type == Plant_Type.fireplant:
		return { "temperature": 3 * (age // 5), "light": 2 * (age // 5), "water": -5, "charge": 10 * (age // 10), "bugs": -5, "poison": 0, "flags": {} }
	return { "temperature": 0, "light": 0, "water": 0, "charge": 0, "bugs": 0, "poison": 0, "flags": {} }

def Get_Plant_Conditions(plant_type):
	if plant_type == Plant_Type.hrelay:
		return { "temperature": 10, "light": 10, "water": 10, "charge": 10, "bugs": 0, "poison": 5, "flags": {} }
	if plant_type == Plant_Type.brelay:
		return { "temperature": 10, "light": 10, "water": 10, "charge": 10, "bugs": 0, "poison": 5, "flags": {} }
	if plant_type == Plant_Type.drelay:
		return { "temperature": 10, "light": 10, "water": 10, "charge": 10, "bugs": 0, "poison": 5, "flags": {} }
	if plant_type == Plant_Type.fireplant:
		return { "temperature": 10, "light": 10, "water": 30, "charge": 10, "bugs": 0, "poison": 5, "flags": {} }
	return { "temperature": 0, "light": 0, "water": 0, "charge": 0, "bugs": 0, "poison": 0, "flags": {} }

def Calculate_Growth(plant, conditions):
	growth = 60
	growth -= abs(plant.temperature - conditions["temperature"])
	growth -= abs(plant.light - conditions["light"])
	growth -= abs(plant.water - conditions["water"])
	growth -= abs(plant.charge - conditions["charge"])
	growth -= abs(plant.poison - conditions["poison"])
	growth -= abs(plant.bugs - conditions["bugs"])

	#TODO make flags like on fire decrease growth

	if growth < 0:
		growth = 0
	if growth > 20:
		growth = 20
	return growth

class Game_Data():
	action_q = None
	field_size_x = None
	field_size_y = None
	game_field = None
	seeds = None
	camera_pos = None
	initialized = None
	magic_circle = None
	score = None
	outside_conditions = None

	def __init__(self):
		self.action_q = []
		self.field_size_x = 9
		self.field_size_y = 9
		self.camera_pos = [0, 16]
		self.initialized = False
		self.score = 0

	def Initialize(self):
		self.game_field = [[{"plant": Plant(), "growable": False } for i in range(self.field_size_y)] for j in range(self.field_size_x)]
		field_obj = Get_Field(0)
		self.field_size_x = field_obj[2]
		self.field_size_y = field_obj[3]
		field = field_obj[0]
		self.magic_circle = field_obj[1]
		self.outside_conditions = field_obj[4]
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

	def Get_Plant_Event(self, plant, x, y, age_before):
		if plant.plant_type == Plant_Type.fireplant:
			event_age = 20
			if age_before < event_age and plant.age >= event_age:
				self.score += 20#TODO fire blast
				self.Up_Root(x, y + 1)
				self.Up_Root(x, y - 1)
				self.Up_Root(x + 1, y)
				self.Up_Root(x - 1, y)

			event_age = 20
			if plant.age >= event_age:
				self.score += 2

		event_age = 100#aplicable to all plants
		if age_before < event_age and plant.age >= event_age:
			self.Up_Root(x, y)

	def Relay(self, effects, pos, passed = []):
		for item in passed:
			if item == pos:
				return #Already checked this relay

		if not len(passed) == 0:#So as not to applyu the same effect twice on the starting relay
			Apply_Effects(effects, self.game_field[pos[0]][pos[1]]["plant"])
			
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

				self.Get_Plant_Event(plant["plant"], i, j, age_before)
		self.action_q.clear()

		effects = Get_Plant_Effect(None)
		for item in self.magic_circle:
			#apply effects to tile
			Apply_Effects(effects, self.game_field[item[0]][item[1]]["plant"])

			plant_t = self.game_field[item[0]][item[1]]["plant"].plant_type
			if plant_t == Plant_Type.hrelay or plant_t == Plant_Type.brelay or plant_t == Plant_Type.drelay:
				self.Relay(effects, item)
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