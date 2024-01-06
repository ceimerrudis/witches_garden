import pygame
from pygame.locals import *

class Screen():
    # This class draws the objects on the screen and is in charge of the viewport
    # (the part of the window that objects are displayed in)
    
    # The other components assume that a screen is a constant pixel window 
    screen_width = None # In this class screen_width is the viewport width minimum value
    screen_height = None
    old_window_size_x = None# used to preserve the window size after turning off fullscrn
    old_window_size_y = None
    surface = None # The actual pygame window surface
    scale = None # multiplier for game viewport pixels to fit in screen pixels (changes display size of game)
    game_window = None # a rect holding the info where on screen the viewport should be drawn
    viewport = None # a rect unaware of the existance of the rest of the screen
    # also its x, y attributes function as camera position

    def __init__(self):
        self.screen_width = (176 + 48) # calculated tilemap size + space for ui
        self.screen_height = (176 + 64)
        self.old_window_size_x = self.screen_width
        self.old_window_size_y = self.screen_height
        self.scale = 2
        self.game_window = pygame.Rect((0, 0), (self.screen_width, self.screen_height))
        self.viewport = pygame.Rect(0, 0, self.screen_width, self.screen_height)

        self.surface = pygame.display.set_mode((self.screen_width * 2, self.screen_height * 2), RESIZABLE | HWSURFACE)
        w,h=self.surface.get_size()
        self.resize(w, h)# calling resize so the the code knows the true dimensions
        # and can calculate scale

    def Calc_Mouse_Viewport_Position(self, x, y):
        # Mouse data is given in screen pixels so we use game window to calculate viewport position
        return int((x - self.game_window.x) / self.scale), int((y - self.game_window.y) / self.scale)

    def move_camera(self, x, y):
        self.set_camera_pos((self.viewport.x + x, self.viewport.y + y))

    def set_camera_pos(self, pos):
        self.viewport.update(pos[0], pos[1], self.viewport.w, self.viewport.h)

    def calc_rect_place_on_viewport(self, rect, use_camera_position = False):
        # Calculates the visible part of the rect
        # as well as scales it

        # in human language where on the camera (if anywhere) is this objects image located
        tmpRect = pygame.Rect( #will be performing changes on the object so we use a temporary
            (rect.x, rect.y, rect.w, rect.h)
        )

        if use_camera_position: # ui for example does not care about position
            left = self.viewport.x
            top = self.viewport.y
        else:
            left = 0
            top = 0

        # distance from cameras edges to object
        # distance calculated is the furthest edges distance 
        from_left_side = (tmpRect.left + tmpRect.width) - left
        from_top_side = (tmpRect.top + tmpRect.height) - top
        from_right_side = tmpRect.w - ((tmpRect.left + tmpRect.width) - (left + self.viewport.width))
        from_bottom_side = tmpRect.h - ((tmpRect.top + tmpRect.height) - (top + self.viewport.height))

        # Make sure the scaled rect stays within the boundaries of the viewport
        if from_left_side < 0 or from_top_side < 0 or from_right_side < 0 or from_bottom_side < 0:
            return None

        # cropping the rect so that half of an object can be seen 
        area = pygame.Rect((0, 0), (tmpRect.w, tmpRect.h))
        if from_left_side < tmpRect.width:
            area.left = tmpRect.width - from_left_side
            area.width -= area.left
        if from_right_side < tmpRect.width:
            area.width -= (tmpRect.width - from_right_side)
        if from_top_side < tmpRect.height:
            area.top = tmpRect.height - from_top_side
            area.height -= area.top
        if from_bottom_side < tmpRect.height:
            area.height -= (tmpRect.height - from_bottom_side)
        
        # scaling up the image to fit on the actual screen
        tmpRect.update(((tmpRect.x - left) * self.scale) + self.game_window.x, ((tmpRect.y - top) * self.scale) + self.game_window.y, tmpRect.w * self.scale, tmpRect.w * self.scale)
        area.update(area.x * self.scale, area.y * self.scale, area.w * self.scale, area.h * self.scale)

        # return the position on screen and the rect of the part of the image that has to be displayed
        return tmpRect, area

    def resize(self, width, height, resize_window = True):
        # resizes the window and updates attributes
        
        # if smaller than the possinle minimum force larger 
        if width < self.screen_width * 2:# multiplied by 2 to increase minimum screen size
            width = self.screen_width * 2
        if height < self.screen_height * 2:
            height = self.screen_height * 2

        # calculates the maximum scale that can be used without going out of bounds
        self.scale = min(self.surface.get_width() // self.screen_width, self.surface.get_height() // self.screen_height)
        if self.scale < 2:
            self.scale = 2

        # recalculate the screen spaced used to display the game
        game_window_width = self.scale * self.screen_width
        game_window_height = self.scale * self.screen_height
        game_window_top = (height - game_window_height) / 2
        game_window_left = (width - game_window_width) / 2
        self.game_window.update(game_window_left, game_window_top, game_window_width, game_window_height)
        
        # this process destroys the window and recreates it
        if resize_window: # When changing fullscreen mode this destruction causes  problems            
            # so when changing fullscreen this gets skipped
            flags = self.surface.get_flags()
            self.surface = pygame.display.set_mode((width, height), flags)

    def fill(self, color):
        #wrapper function
        self.surface.fill(color)

    def blit(self, img, rect, UI = False, scale = True):
        # draws an image on the screen at the specified position
        cropped = False
        # if target are is smaller than picture it must be cropped
        if rect.width < img.get_rect().width:
            crop_w = rect.width
            cropped = True
        else:
            crop_w = img.get_rect().width

        if rect.height < img.get_rect().height:
            crop_h = rect.height
            cropped = True
        else:
            crop_h = img.get_rect().height

        if cropped:
            img = pygame.transform.scale(img, (crop_w, crop_h))

        # Get position on the real screen from game position
        result = self.calc_rect_place_on_viewport(rect, not UI)
        if result is None:
            return

        # the function return position of full rect if it is only partialy on camera 
        # it has to be adjusted
        viewport_rect, area = result
        viewport_rect.update(viewport_rect.x + area.left, viewport_rect.y + area.top, area.w, area.h)

        # scaling the image
        # different scaling rules apply for text (to preserve resolution)
        if scale:
            img = pygame.transform.scale(img, (rect.w * self.scale, rect.h * self.scale))
        else:
            a = max((4-self.scale), 1)
            img = pygame.transform.scale(img, (rect.w / a, rect.h / a))

        self.surface.blit(img, viewport_rect, area)# pygame function

    def draw(self, color, rect):
        # draws a colored rect to the viewport
        # used for the green backdrop
        result = self.calc_rect_place_on_viewport(rect)
        if result is None:
            return
        viewport_rect, area = result
        viewport_rect.update(viewport_rect.x + area.left, viewport_rect.y + area.top, area.w, area.h)
        pygame.draw.rect(self.surface, color, viewport_rect)

    def toggle_fullscreen(self): 
        # does what it says
        tmp = self.surface.convert() # makes sure there isnt a black frame during switch
        
        # the basic idea is that we save the window info destroy it and create a new one
        caption = pygame.display.get_caption()
        
        flags = self.surface.get_flags()
        w, h = self.surface.get_size()

        if flags & FULLSCREEN == 0:
            # turning on
            self.old_window_size_x, self.old_window_size_y = self.surface.get_size()
            pygame.display.quit()
            pygame.display.init()
            self.surface = pygame.display.set_mode((0,0), flags^FULLSCREEN)
        else:
            # turning off
            pygame.display.quit()
            pygame.display.init()
            w = self.old_window_size_x
            h = self.old_window_size_y
            self.surface = pygame.display.set_mode((w,h), flags^FULLSCREEN)
        w, h = self.surface.get_size()
        self.resize(w, h, False)
        self.surface.blit(tmp,(0,0))
        pygame.display.set_caption(*caption)

        # Do not know what this is
        pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??
    
        return self.surface

    def ViewportToWorldPos(self, x, y):
        # account for camera position
        x = x + self.viewport.x
        y = y + self.viewport.y
        return x, y