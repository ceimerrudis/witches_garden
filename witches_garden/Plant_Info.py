from enum import Enum

#To add a plant an entry must be added to the following 6 "functions"

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
	aquagrape = 10
	azurevine = 11
	demonfern = 12
	evergreencabbage = 13
	siphonrose = 14

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
	"aquagrape": [0, 10, 20, 30, 70],
	"azurevine": [0, 10, 25],
	"demonfern": [0, 20, 40],
	"evergreencabbage": [0, 35, 50, 85],
	"siphonrose": [0, 30, 50, 80],
	}

#3 display name
def Plant_Type_To_Display_Name(plant_type):
	#could be turned into a dictionary
	if plant_type == Plant_Type.fireplant:
		return "ignililly"
	elif plant_type == Plant_Type.evergreencabbage:
		return "everg-cab"

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
		temp = 5 + 3 * (age // 5)
		light = 5 + 2 * (age // 5)
		water = -5
		charge = 5 + 10 * (age // 10)
		bugs = -5
		poison = 0
		flags = {}
	if plant_type == Plant_Type.aquagrape:
		temp = 0
		light = 0
		water = 5 + 2 * (age // 2)
		charge = 10
		bugs = 5
		poison = 0
		flags = {}
	if plant_type == Plant_Type.azurevine:
		temp = 5
		light = 10
		water = 5 + 10 * (age // 8)
		charge = 5 + 6 * (age // 5)
		bugs = 0
		poison = 0
		flags = {}
	if plant_type == Plant_Type.demonfern:
		temp = 0
		light = 5 + 3 * (age // 5)
		water = 5
		charge = 0
		bugs = 0
		poison = 5 + 1 * (age // 1)
		flags = {}
	if plant_type == Plant_Type.evergreencabbage:
		temp = -5
		light = 0
		water = 5
		charge = 5 + 2 * (age // 2)
		bugs = 5 +  15 * (age // 8)
		poison = 0
		flags = {}
	if plant_type == Plant_Type.siphonrose:
		temp =  5 + 2 * (age // 6)
		light = 0
		water = 0
		charge = -5 + -2 * (age // 3)
		bugs = 0
		poison = 3 + 2 * (age // 6)
		flags = {}

	return { "temperature": temp, "light": light, "water": water, "charge": charge, "bugs": bugs, "poison": poison, "flags": flags }

#5 Conditions that the plant grows best at
def Get_Plant_Conditions(plant_type):
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
		temp = 25
		light = 10
		water = 30
		charge = 10
		bugs = 0
		poison = 0
		flags = {}
	if plant_type == Plant_Type.aquagrape:
		temp = 20
		light = 50
		water = 20
		charge = 100
		bugs = -15
		poison = 0
		flags = {}
	if plant_type == Plant_Type.azurevine:
		temp = 70
		light = 70
		water = 20
		charge = 10
		bugs = 0
		poison = 5
		flags = {}
	if plant_type == Plant_Type.demonfern:
		temp = 50
		light = 20
		water = 10
		charge = 10
		bugs = -30
		poison = 20
		flags = {}
	if plant_type == Plant_Type.evergreencabbage:
		temp = 10
		light = 30
		water = 50
		charge = 0
		bugs = -10
		poison = -10
		flags = {}
	if plant_type == Plant_Type.siphonrose:
		temp = 30
		light = 20
		water = 30
		charge = 80
		bugs = 0
		poison = 5
		flags = {}
	
	return { "temperature": temp, "light": light, "water": water, "charge": charge, "bugs": bugs, "poison": poison, "flags": flags }

#6 Events that happen when the plant is growing
def Get_Plant_Event(game_data, plant, x, y, age_before):
	event_age = 100#aplicable to all plants at age 100 die (get destroyed (be no longer (stop existing(...))))
	if age_before < event_age and plant.age >= event_age:
		game_data.Up_Root(x, y)
		return

	if plant.plant_type == Plant_Type.fireplant:
		event_age = 20
		if age_before < event_age and plant.age >= event_age:
			game_data.score += 20

			#Fire blast destroys horizontaly and verticaly adjacent plants 
			game_data.Up_Root(x, y + 1)
			game_data.Up_Root(x, y - 1)
			game_data.Up_Root(x + 1, y)
			game_data.Up_Root(x - 1, y)

		event_age = 20
		if plant.age >= event_age:
			game_data.score += 2

	if plant.plant_type == Plant_Type.azurevine:
		event_age = 25
		if age_before < event_age and plant.age >= event_age:
			game_data.score += 30

			#Affect the whole field with light rain and charge
			#TODO

	if plant.plant_type == Plant_Type.aquagrape:
		event_age = 30
		if age_before < event_age and plant.age >= event_age:
			if plant.age <= 70:
				game_data.score += 5
				plant.age += 2

	if plant.plant_type == Plant_Type.demonfern:
		event_age = 40
		if age_before < event_age and plant.age >= event_age:
			game_data.score += -10

			#Poison sets over field
			#set flag as sprayed
			#TODO

	if plant.plant_type == Plant_Type.evergreencabbage:
		event_age = 85
		if age_before < event_age and plant.age >= event_age:
			game_data.score += 150

			#Attract bugs
			#TODO

		event_age = 50
		if age_before < event_age and plant.age >= event_age:
			pass
			#Attract bugs
			#TODO

	if plant.plant_type == Plant_Type.siphonrose:
		event_age = 50
		if age_before < event_age and plant.age >= event_age:
			game_data.score += 15