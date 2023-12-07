from enum import Enum

#To add a plant an entry must be added to the following 6 functions

#1 Plant enum
class Plant_Type(Enum):
	#The number does not matter it just has to be unique
	plot = 1
	grass1 = 2
	grass2 = 3
	grass3 = 4
	grass4 = 5
	drelay = 6
	brelay = 7
	hrelay = 8
	fireplant = 9
	#iceplant = 10
	#seedplant = 11

#2 Aka ages at which sprites change
def Get_Plant_Stages():
	return {#Must be ascending
	"plot": [0],
	"grass1": [0],
	"grass2": [0],
	"grass3": [0],
	"grass4": [0],
	"hrelay": [0, 10, 20],
	"brelay": [0, 10, 20],
	"drelay": [0, 10, 20],
	"fireplant": [0, 10, 20],
	}

#3 display name
def Plant_Type_To_Display_Name(plant_type):
	if plant_type == Plant_Type.fireplant:
		return "fire augs"

	return plant_type.name

#4 Effects when passing through the magic circle
def Get_Plant_Effect(plant_type, age = 0):
	temp = 0
	light = 0
	water = 0
	charge = 0
	bugs = 0
	poison = 0
	flags = {}

	if plant_type == Plant_Type.fireplant:
		temp = 3 * (age // 5)
		light = 2 * (age // 5)
		water = -5
		charge = 10 * (age // 10)
		bugs = -5
		poison = 0
		flags = {}

	return { "temperature": temp, "light": light, "water": water, "charge": charge, "bugs": bugs, "poison": poison, "flags": flags }

#5 Conditions that the plant grows best at
def Get_Plant_Conditions(plant_type):
	#Order does not matter
	temp = 0
	light = 0
	water = 0
	charge = 0
	bugs = 0
	poison = 0
	flags = {}

	if plant_type == Plant_Type.hrelay:
		temp = 10
		light = 10
		water = 10
		charge = 10
		bugs = 0
		poison = 0
		flags = {}
	if plant_type == Plant_Type.brelay:
		temp = 10
		light = 10
		water = 10
		charge = 10
		bugs = 0
		poison = 0
		flags = {}
	if plant_type == Plant_Type.drelay:
		temp = 10
		light = 10
		water = 10
		charge = 10
		bugs = 0
		poison = 0
		flags = {}
	if plant_type == Plant_Type.fireplant:
		temp = 10
		light = 10
		water = 30
		charge = 10
		bugs = 0
		poison = 0
		flags = {}
	
	return { "temperature": temp, "light": light, "water": water, "charge": charge, "bugs": bugs, "poison": poison, "flags": flags }

#6 Events that happen when the plant is growing
def Get_Plant_Event(game_data, plant, x, y, age_before):
	if plant.plant_type == Plant_Type.fireplant:
		event_age = 20
		if age_before < event_age and plant.age >= event_age:
			game_data.score += 20#TODO fire blast
			game_data.Up_Root(x, y + 1)
			game_data.Up_Root(x, y - 1)
			game_data.Up_Root(x + 1, y)
			game_data.Up_Root(x - 1, y)

		event_age = 20
		if plant.age >= event_age:
			game_data.score += 2

	event_age = 100#aplicable to all plants
	if age_before < event_age and plant.age >= event_age:
		game_data.Up_Root(x, y)