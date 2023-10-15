import pygame
class Input_System():
    def get_inputs(self):
        pressed_keys = pygame.key.get_pressed()
        
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        #TODO overhaul
        #1 key module
        if pressed_keys[pygame.K_F11]:
            if self.f_11 == 0 or self.f_11 == 3:
                self.f_11 = 1
            else:
                self.f_11 = 2
        else:
            if self.f_11 == 1 or self.f_11 == 2:
                self.f_11 = 3
            else:
                self.f_11 = 0
        #1 key module end

        if pressed_keys[pygame.K_w]:
            if self.w == 0 or self.w == 3:
                self.w = 1
            else:
                self.w = 2
        else:
            if self.w == 1 or self.w == 2:
                self.w = 3
            else:
                self.w = 0

        if pressed_keys[pygame.K_a]:
            if self.a == 0 or self.a == 3:
                self.a = 1
            else:
                self.a = 2
        else:
            if self.a == 1 or self.a == 2:
                self.a = 3
            else:
                self.a = 0

        if pressed_keys[pygame.K_s]:
            if self.s == 0 or self.s == 3:
                self.s = 1
            else:
                self.s = 2
        else:
            if self.s == 1 or self.s == 2:
                self.s = 3
            else:
                self.s = 0
        #
        if pressed_keys[pygame.K_d]:
            if self.d == 0 or self.d == 3:
                self.d = 1
            else:
                self.d = 2
        else:
            if self.d == 1 or self.d == 2:
                self.d = 3
            else:
                self.d = 0
    #0 means not clicked 1 means just clicked 2 means held # 3 means released
    f_11 = 0
    w = 0
    a = 0
    s = 0
    d = 0
    mouse_0 = 0
    mouse_1 = 0
    mouse_pos_x = 0#position in pixels relative to window (0, 0) == top left corner
    mouse_pos_y = 0#position in pixels relative to window (0, 0) == top left corner