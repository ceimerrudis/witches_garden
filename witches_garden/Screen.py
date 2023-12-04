import pygame
from pygame.locals import *

class Screen():
    screen_width = None
    screen_height = None
    old_window_size_x = None
    old_window_size_y = None
    surface = None
    scale = None
    game_window = None
    viewport = None

    def __init__(self):
        self.screen_width = 176 + 48
        self.screen_height = 176 + 64
        self.old_window_size_x = self.screen_width
        self.old_window_size_y = self.screen_height
        self.surface = None
        self.scale = 4
        self.game_window = pygame.Rect((0, 0), (self.screen_width, self.screen_height))
        self.viewport = pygame.Rect(0, 0, self.screen_width, self.screen_height)

        self.surface = pygame.display.set_mode((self.screen_width, self.screen_height), RESIZABLE | HWSURFACE)
        w,h=self.surface.get_size()
        self.resize(w, h)

    def Calc_Mouse_Viewport_Position(self, x, y):
        return int((x - self.game_window.x) / self.scale), int((y - self.game_window.y) / self.scale)

    def move_camera(self, x, y):
        self.viewport.update(self.viewport.x + x, self.viewport.y + y, self.viewport.w, self.viewport.h)

    def set_camera_pos(self, pos):
        self.viewport.update(pos[0], pos[1], self.viewport.w, self.viewport.h)

    def calc_rect_place_on_viewport(self, rect, use_viewport_position = False):
        # Calculate the scaled rect
        tmpRect = pygame.Rect(
            (rect.x, rect.y, rect.w, rect.h)
        )

        if use_viewport_position:
            left = self.viewport.left
            top = self.viewport.top
        else:
            left = 0
            top = 0

        from_left_side = (tmpRect.left + tmpRect.width) - left
        from_top_side = (tmpRect.top + tmpRect.height) - top
        from_right_side = tmpRect.w - ((tmpRect.left + tmpRect.width) - (left + self.viewport.width))
        from_bottom_side = tmpRect.h - ((tmpRect.top + tmpRect.height) - (top + self.viewport.height))

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
        
        tmpRect.update(((tmpRect.x - left) * self.scale) + self.game_window.x, ((tmpRect.y - top) * self.scale) + self.game_window.y, tmpRect.w * self.scale, tmpRect.w * self.scale)
        area.update(area.x * self.scale, area.y * self.scale, area.w * self.scale, area.h * self.scale)

        #tmpRect place on surface to blit
        #area blit param
        return tmpRect, area

    def resize(self, width, height, resize_window = True):
        if width < self.screen_width:
            width = self.screen_width
        if height < self.screen_height:
            height = self.screen_height
        #viewports
        self.scale = min(self.surface.get_width() // self.screen_width, self.surface.get_height() // self.screen_height)
        if self.scale == 0:
            self.scale = 1
        game_window_width = self.scale * self.screen_width
        game_window_height = self.scale * self.screen_height
        game_window_top = (height - game_window_height) / 2
        game_window_left = (width - game_window_width) / 2
        self.game_window.update(game_window_left, game_window_top, game_window_width, game_window_height)
        if resize_window:
            flags = self.surface.get_flags()
            self.surface = pygame.display.set_mode((width, height), flags)

    def fill(self, color):
        self.surface.fill(color)

    def blit(self, img, rect, UI = False, scale = True):
        cropped = False
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

        result = self.calc_rect_place_on_viewport(rect, not UI)
        if result is None:
            return
        viewport_rect, area = result
        viewport_rect.update(viewport_rect.x + area.left, viewport_rect.y + area.top, area.w, area.h)

        if scale:
            img = pygame.transform.scale(img, (rect.w * self.scale, rect.h * self.scale))
        else:
            a = max((4-self.scale), 1)
            img = pygame.transform.scale(img, (rect.w / a, rect.h / a))

        self.surface.blit(img, viewport_rect, area)

    def draw(self, color, rect):
        result = self.calc_rect_place_on_viewport(rect)
        if result is None:
            return
        viewport_rect, area = result
        viewport_rect.update(viewport_rect.x + area.left, viewport_rect.y + area.top, area.w, area.h)
        pygame.draw.rect(self.surface, color, viewport_rect)

    def toggle_fullscreen(self):    
        tmp = self.surface.convert()
        caption = pygame.display.get_caption()
        
        flags = self.surface.get_flags()
        w, h = self.surface.get_size()

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
    
        return self.surface

    def ScreenToWorldPos(self, x, y):
        x = x + self.viewport.x
        y = y + self.viewport.y
        return x, y