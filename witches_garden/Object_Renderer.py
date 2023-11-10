import pygame
import numpy
from pygame.locals import *
from Screen import Screen
from Game_Data import Plant, Plant_Type
from Get_Sprite import Get_Sprite, Get_Plant_Sprite

class Tilemap_Obj():
	def __init__(self, img, rect, p_type = None, age = 0):
		self.image = img
		self.rect = rect
		self.p_type = p_type
		self.age = age
	p_type = None
	age = 0
	rect = None
	image = None

class Object_Renderer():
	def __init__(self, screen, game_data):
		self.surface = screen
		self.background = numpy.array([[Tilemap_Obj(None, pygame.Rect(j * 16, (game_data.field_size_y * 16) - (i * 16), 16, 16)) for i in range(game_data.field_size_y)] for j in range(game_data.field_size_x)], dtype=Tilemap_Obj)
		self.plants = numpy.array([[Tilemap_Obj(None, pygame.Rect(j * 16, (game_data.field_size_y * 16) - (i * 16), 16, 16)) for i in range(game_data.field_size_y)] for j in range(game_data.field_size_x)], dtype=Tilemap_Obj)

	def render(self, game_data):	
		j = 0
		for x in game_data.game_field:
			i = 0
			for y in x:
                y = y["plant"]
				if y.plant_type == Plant_Type.plot or y.plant_type == Plant_Type.grass1 or y.plant_type == Plant_Type.grass2 or y.plant_type == Plant_Type.grass3 or y.plant_type == Plant_Type.grass4:
					if not (self.background[i][j].p_type == y.plant_type and self.background[i][j].age == y.age):
						self.background[i][j] = Tilemap_Obj(Get_Plant_Sprite(y), pygame.Rect(j * 16, (game_data.field_size_y * 16) - (i * 16), 16, 16), y.plant_type, y.age)
				else:
					if not (self.plants[i][j].p_type == y.plant_type and self.plants[i][j].age == y.age):
						self.plants[i][j] = Tilemap_Obj(Get_Plant_Sprite(y), pygame.Rect(j * 16, (game_data.field_size_y * 16) - (i * 16), 16, 16), y.plant_type, y.age)
				
				if not self.background[i][j].image == None:
					self.surface.blit(self.background[i][j].image, self.background[i][j].rect)
				if not self.plants[i][j].image == None:
					self.surface.blit(self.plants[i][j].image, self.plants[i][j].rect)
				i += 1
			j += 1
	min_width = 1
	min_height = 1
	
	#tilemap
	background = None
	plants = None

	surface = None