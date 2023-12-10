import pygame
from pygame.locals import *
from Screen import Screen
from Enums import UI_Object_Type, Image_Type
from Nine_Slice import Nine_Slice_Rect, nine_slice

def Draw_Nine_Sliced_Image(imageObject, surface):
    i = 0
    j = 0
    for piece in imageObject.image:
        while j < len(imageObject.rects):
            if not imageObject.rects[j][1] == i:
                break
            surface.blit(piece, imageObject.rects[j][0], True)
            j += 1
        i += 1
    
class UI_Renderer():
    #renders the ui elements that are stored in ui_logic_controler class
    ui_logic_ctrl = None#Holds objects
    surface = None #Screen obj to which the display the objects

    def __init__(self, Screen, ui_logic_ctrl):
        self.surface = Screen
        self.ui_logic_ctrl = ui_logic_ctrl

    def render(self):
        #the order is important because pause layer has to be rendered above game window
        for i in range(len(self.ui_logic_ctrl.active_screens)):
            screen = self.ui_logic_ctrl.active_screens[i]
            for item in screen.ui_objects:
                if item.image_type == Image_Type.nine_sliced:
                    Draw_Nine_Sliced_Image(item, self.surface)
                else:
                    if item.object_type == UI_Object_Type.text:
                        #to preserve text resolution do not scale
                        self.surface.blit(item.image, item.rect, True, False)
                    else:
                        self.surface.blit(item.image, item.rect, True)
        