import pygame
from pygame.locals import *

class Screen():
    def __init__(self):
        self.surface = pygame.display.set_mode((self.screen_min_width, self.screen_min_height), RESIZABLE | HWSURFACE)
        w,h=self.surface.get_size()
        self.resize(w, h)

    screen_min_width = 176 + 48
    screen_min_height = 176 + 64
    old_window_size_x = screen_min_width
    old_window_size_y = screen_min_height
    surface = None
    scale = 4
    game_window = pygame.Rect((0, 0), (screen_min_width, screen_min_height))
    viewport = pygame.Rect(0, 0, screen_min_width, screen_min_height)

    def move_camera(self, x, y):
        self.viewport.update(self.viewport.x + x, self.viewport.y + y, self.viewport.w, self.viewport.h)

    def calc_rect_place_on_viewport(self, rect):
        # Calculate the scaled rect
        tmpRect = pygame.Rect(
            (rect.x, rect.y, rect.w, rect.h)
        )

        from_left_side = (tmpRect.left + tmpRect.width) - self.viewport.left
        from_top_side = (tmpRect.top + tmpRect.height) - self.viewport.top
        from_right_side = tmpRect.w - ((tmpRect.left + tmpRect.width) - (self.viewport.left + self.viewport.width))
        from_bottom_side = tmpRect.h - ((tmpRect.top + tmpRect.height) - (self.viewport.top + self.viewport.height))

        # Make sure the scaled rect stays within the boundaries of the viewport
        if from_left_side < 0 or from_top_side < 0 or from_right_side < 0 or from_bottom_side < 0:
            return None

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
        
        tmpRect.update(((tmpRect.x - self.viewport.x) * self.scale) + self.game_window.x, ((tmpRect.y - self.viewport.y) * self.scale) + self.game_window.y, tmpRect.w * self.scale, tmpRect.w * self.scale)
        area.update(area.x * self.scale, area.y * self.scale, area.w * self.scale, area.h * self.scale)

        #tmpRect place on surface to blit
        #area blit param
        return tmpRect, area

    def resize(self, width, height, resize_window = True):
        if width < self.screen_min_width:
            width = self.screen_min_width
        if height < self.screen_min_height:
            height = self.screen_min_height
        #viewports
        self.scale = min(self.surface.get_width() // self.screen_min_width, self.surface.get_height() // self.screen_min_height)
        game_window_width = self.scale * self.screen_min_width
        game_window_height = self.scale * self.screen_min_height
        game_window_top = (height - game_window_height) / 2
        game_window_left = (width - game_window_width) / 2
        self.game_window.update(game_window_left, game_window_top, game_window_width, game_window_height)
        if resize_window:
            flags = self.surface.get_flags()
            self.surface = pygame.display.set_mode((width, height), flags)

    def fill(self, color):
        self.surface.fill(color)

    def blit(self, img, rect):
        return 7    

    def draw(self, color, rect):
        result = self.calc_rect_place_on_viewport(rect)
        if result is None:
            return
        tmpRect, area = result
        tmpRect.update(tmpRect.x + area.left, tmpRect.y + area.top, area.w, area.h)
        pygame.draw.rect(self.surface, color, tmpRect)

    def toggle_fullscreen(self):    
        tmp = self.surface.convert()
        caption = pygame.display.get_caption()
        
        flags = self.surface.get_flags()
        w, h = self.surface.get_size()

        cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007 
    
        flags = self.surface.get_flags()

        if flags & FULLSCREEN == 0:
            #turning on
            self.old_window_size_x, self.old_window_size_y = self.surface.get_size()
            pygame.display.quit()
            pygame.display.init()
            self.surface = pygame.display.set_mode((0,0), flags^FULLSCREEN)
        else:
            pygame.display.quit()
            pygame.display.init()
            w = self.old_window_size_x
            h = self.old_window_size_y
            self.surface = pygame.display.set_mode((w,h), flags^FULLSCREEN)
        w, h = self.surface.get_size()
        self.resize(w, h, False)
        self.surface.blit(tmp,(0,0))
        pygame.display.set_caption(*caption)

        pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??

        pygame.mouse.set_cursor( *cursor )  # Duoas 16-04-2007
    
        return self.surface