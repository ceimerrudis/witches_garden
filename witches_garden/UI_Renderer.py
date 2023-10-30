import pygame
from pygame.locals import *
from Screen import Screen

def Get_Sprite(ui_element):
	spritepath = "witches_garden/sprites/ui_elements/"
	if ui_element == "slot":
		name = "seedSlot"
	elif ui_element == "bottom":
		name = "bottomPannel"
	elif ui_element == "top":
		name = "topPannel"
	elif ui_element == "arrowLeft":
		name = "arrowLeft"
	elif ui_element == "arrowRight":
		name = "arrowRight"

	return pygame.image.load(spritepath + name + ".png")

class UI_Renderer():
	def __init__(self, Screen):
		self.surface = Screen

	def render(self):
		a = None

	surface = None