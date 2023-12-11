import pygame
from pygame.locals import *
from Screen import Screen
from Game_Data import Plant, Plant_Type
from Get_Sprite import Get_Plant_Sprite
from Display_Objects import Tile_Obj

class Object_Renderer():
	# Renders scene objects stored by ui_logic controler to the given screen
	surface = None

	def __init__(self, screen):
		self.surface = screen

	def render(self, game_data, scene):	
		# Renders scene objects stored by ui_logic controler
		if game_data.initialized == True:
			j = 0
			for x in game_data.game_field:
				i = 0
				for y in x:
					y = y["plant"]

					plnt = scene.plants.Get_Tile(i, j)
					bckgrnd = scene.background.Get_Tile(i, j)

					if	y.plant_type == Plant_Type.plot or y.plant_type == Plant_Type.grass1 or y.plant_type == Plant_Type.grass2 or y.plant_type == Plant_Type.grass3 or y.plant_type == Plant_Type.grass4:
						if not (bckgrnd.p_type == y.plant_type and bckgrnd.age == y.age):
							scene.background.Set_Tile(i, j, Tile_Obj(Get_Plant_Sprite(y), bckgrnd.rect, p_type = y.plant_type, age = y.age))

						if not plnt.p_type == None:
							scene.plants.Set_Tile(i, j, Tile_Obj(None, plnt.rect))
					else:
						if not (plnt.p_type == y.plant_type and plnt.age == y.age):
							scene.plants.Set_Tile(i, j, Tile_Obj(Get_Plant_Sprite(y), plnt.rect, p_type = y.plant_type, age = y.age))
				
					if not bckgrnd.image == None:
						self.surface.blit(bckgrnd.image, bckgrnd.rect)
					if not plnt.image == None:
						self.surface.blit(plnt.image, plnt.rect)
					i += 1
				j += 1