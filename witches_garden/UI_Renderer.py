import pygame
from pygame.locals import *
from Screen import Screen

def Nine_Slice_Rect(rect, left, top, right, bottom, img_width = False, img_height = False):
    width = rect.w - left - right
    height = rect.h - top - bottom 
    if (img_height == False or img_height == False):
        img_width = width
        img_height = height

    top_left_slice = pygame.Rect(       rect.x + 0,             rect.y + 0,             left,   top)
    
    #
    top_slice_total = pygame.Rect(            rect.x + left,          rect.y + 0,             width,  top)
    top_slice = []
    x = 0
    while x < top_slice_total.width:
        w = top_slice_total.width - x
        if w > img_width:
            w = img_width
        top_slice.append((pygame.Rect(top_slice_total.x + x, top_slice_total.y, w, top), 1))
        x += img_width

    top_right_slice = pygame.Rect(      rect.x + left + width,  rect.y + 0,             right,  top)
    
    #
    left_slice_total = pygame.Rect(           rect.x + 0,             rect.y + top,           left,   height)
    left_slice = []
    y = 0
    while y < left_slice_total.height:
        h = left_slice_total.height - y
        if h > img_height:
            h = img_height
        left_slice.append((pygame.Rect(left_slice_total.x, left_slice_total.y + y, left, h), 3))
        y += img_height

    #
    center_total = pygame.Rect(         rect.x + left,          rect.y + top,           width,  height)
    center = []
    y = 0
    while y < center_total.height:
        x = 0
        while x < center_total.width:
            w = center_total.width - x
            if w > img_width:
                w = img_width

            h = center_total.height - y
            if h > img_height:
                h = img_height
            center.append((pygame.Rect(center_total.x + x, center_total.y + y, w, h), 4))
            x += img_width
        y += img_height

    #
    right_slice_total = pygame.Rect(          rect.x + left + width,  rect.y + top,           right,  height)
    right_slice = []
    y = 0
    while y < right_slice_total.height:
        h = right_slice_total.height - y
        if h > img_height:
            h = img_height
        right_slice.append((pygame.Rect(right_slice_total.x, right_slice_total.y + y, right, h), 5))
        y += img_height

    bottom_left_slice = pygame.Rect(    rect.x + 0,             rect.y + top + height,  left,   bottom)
    
    #
    bottom_slice_total = pygame.Rect(         rect.x + left,          rect.y + top + height,  width,  bottom)
    bottom_slice = []
    x = 0
    while x < bottom_slice_total.width:
        w = bottom_slice_total.width - x
        if w > img_width:
            w = img_width
        bottom_slice.append((pygame.Rect(bottom_slice_total.x + x, bottom_slice_total.y, w, bottom), 7))
        x += img_width


    bottom_right_slice = pygame.Rect(   rect.x + left + width,  rect.y + top + height,  right,  bottom)

    ktv = []
    ktv.append((top_left_slice, 0))
    ktv += top_slice
    ktv.append((top_right_slice, 2))
    ktv += left_slice
    ktv += center
    ktv += right_slice
    ktv.append((bottom_left_slice, 6))
    ktv += bottom_slice
    ktv.append((bottom_right_slice, 8))
    return ktv

def nine_slice(image, left, top, right, bottom):
    image_rect = image.get_rect()
    sliced_image_rect = Nine_Slice_Rect(image_rect, left, top, right, bottom)

    result = []
    for rect in sliced_image_rect:
        result.append(image.subsurface(rect[0]))
    
    return result, image_rect.w - left - right, image_rect.h - top - bottom 


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

class UI_Object():
    def __init__(self, image, rect, image_type):
        self.image = image
        self.rect = rect
        self.image_type = image_type

    image = None
    rect = None
    image_type = 0
    #0 for normal image 
    #1 for nine sliced

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
            surface.blit(item.image, item.rect, True)

class UI_Screen():
    static = []
    dynamic = []
    
    def draw(self, surface):        
        drawList(self.static, surface)
        drawList(self.dynamic, surface)
    
class UI_Renderer():
    def __init__(self, Screen):
        self.surface = Screen
        btm_pnl_slice_val = (26, 26, 26, 26)
        btm_pnl_sliced_images, center_width, center_height = nine_slice(Get_Sprite("bottom"), btm_pnl_slice_val[0], btm_pnl_slice_val[1], btm_pnl_slice_val[2], btm_pnl_slice_val[3])
        btm_pnl_target_rect_on_viewport = pygame.Rect(0, self.surface.screen_min_height - 64, self.surface.screen_min_width, 64)
        btm_pnl_sliced_rect = Nine_Slice_Rect(btm_pnl_target_rect_on_viewport, btm_pnl_slice_val[0], btm_pnl_slice_val[1], btm_pnl_slice_val[2], btm_pnl_slice_val[3], center_width, center_height)
        self.garden_UI.static = [UI_Object(btm_pnl_sliced_images, btm_pnl_sliced_rect, 1)]
        #self.garden_UI.static = [UI_Object(Get_Sprite("bottom"), pygame.Rect(0, self.surface.screen_min_height - 64, self.surface.screen_min_width, 64), 0)]

    def render(self):
        # self.surface.blit(Get_Sprite("bottom"), pygame.Rect(0, self.surface.screen_min_height - 64, self.surface.screen_min_width, 64))

        if self.active_screens["garden"]:
            self.garden_UI.draw(self.surface)

    active_screens = {"garden": True, "main_menu": False}

    main_Menu = UI_Screen()
    garden_UI = UI_Screen()
    surface = None
