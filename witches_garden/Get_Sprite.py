import pygame
from Game_Data import Plant
from Plant_Info import Get_Plant_Stages, Plant_Type

def Get_Sprite(sprite_name):
	spritepath = "witches_garden/sprites/ui_elements/"
	if sprite_name == "slot":
		name = "seedSlot"
	elif sprite_name == "bottom":
		name = "bottomPannel"
	elif sprite_name == "top":
		name = "topPannel"
	elif sprite_name == "arrowLeft":
		name = "arrowLeft"
	elif sprite_name == "arrowRight":
		name = "arrowRight"
	elif sprite_name == "hourglass":
		name = "hourglass_icon"
	elif sprite_name == "pause":
		name = "pause_icon"
	elif sprite_name == "shovel":
		name = "shovel_icon"
	elif sprite_name == "undo":
		name = "undo_icon"
	elif sprite_name == "start_btn":
		name = "start_game_btn"
	elif sprite_name == "back_btn":
		name = "back_btn"
	elif sprite_name == "menu_btn":
		name = "menu_btn"
	elif sprite_name == "gray":
		name = "gray"
	return pygame.image.load(spritepath + name + ".png")

#Gets plants sprite accoding to its state
def Get_Seed_Sprite(plant):
	spritepath = "witches_garden/sprites/seeds/"
	name = Plant_Type_To_Sprite_Name(plant)
	name += "_seed"

	return pygame.image.load(spritepath + name + ".png")


#Gets plants sprite accoding to its state
def Get_Plant_Sprite(plant):
	spritepath = "witches_garden/sprites/plant_tilemap/"
	name = Plant_Type_To_Sprite_Name(plant.plant_type)

	current = 0
	plant_stages = Get_Plant_Stages()
	for possible_age in plant_stages[name]:
		if plant.age >= possible_age:
			current = possible_age
	name += "_age_" + str(current)

	return pygame.image.load(spritepath + name + ".png")

def Plant_Type_To_Sprite_Name(plant):
	name = plant.name
	"""if plant == Plant_Type.plot:
		name = "plot"
	elif plant == Plant_Type.grass1:
		name = "grass1"
	elif plant == Plant_Type.grass2:
		name = "grass2"
	elif plant == Plant_Type.grass3:
		name = "grass3"
	elif plant == Plant_Type.grass4:
		name = "grass4"
	elif plant == Plant_Type.fireplant:
		name = "fireplant"
	elif plant == Plant_Type.iceplant:
		name = "iceplant"
	#elif plant == Plant_Type.seedplant:
	#	name = "seedplant"
	elif plant == Plant_Type.hrelay:
		name = "hrelay"
	elif plant == Plant_Type.drelay:
		name = "drelay"
	elif plant == Plant_Type.brelay:
		name = "brelay"
	"""
	return name