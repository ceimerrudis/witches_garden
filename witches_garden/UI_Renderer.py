import pygame
from pygame.locals import *
from Screen import Screen
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
    ui_logic_ctrl = None
    surface = None

    def __init__(self, Screen, ui_logic_ctrl):
        self.surface = Screen
        self.ui_logic_ctrl = ui_logic_ctrl

    def render(self):
        for i in range(len(self.ui_logic_ctrl.active_screens)):
            screen = self.ui_logic_ctrl.active_screens[i]
            for item in screen.ui_objects:
                if item.image_type == 1:
                    Draw_Nine_Sliced_Image(item, self.surface)
                else:
                    if item.object_type == 2:
                        #to preserve text resolution do not scale
                        self.surface.blit(item.image, item.rect, True, False)
                    else:
                        self.surface.blit(item.image, item.rect, True)
        