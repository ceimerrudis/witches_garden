import pygame
from pygame.locals import *
import thorpy

class Object_Renderer():
	def render(self, surface):	
		object2 = pygame.Rect((-8, 10), (16, 16))
		surface.draw((0, 0, 255), object2)
	min_width = 1
	min_height = 1