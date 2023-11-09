import pygame
from pygame.locals import *
from Screen import Screen
from Nine_Slice import Nine_Slice_Rect, nine_slice

def Draw_Nine_Sliced_Image(imageObject, surface):
    i = 0
    j = 0
    for piece in imageObject.image:
        while j < len(imageObject.rect):
            if not imageObject.rect[j][1] == i:
                break
            surface.blit(piece, imageObject.rect[j][0], True)
            j += 1
        i += 1

def drawList(ui_obj_list, surface):
    for item in ui_obj_list:
        if item.image_type == 1:
            Draw_Nine_Sliced_Image(item, surface)
        else:
            surface.blit(item.image, item.rect[0], True)
    
class UI_Renderer():
    def __init__(self, Screen, ui_logic_ctrl):
        self.surface = Screen
        self.ui_logic_ctrl = ui_logic_ctrl
        
    def render(self):
        for screen in self.ui_logic_ctrl.active_screens:
            drawList(screen.static, self.surface)
            drawList(screen.dynamic, self.surface)

    ui_logic_ctrl = None
    surface = None
