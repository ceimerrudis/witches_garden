import pygame
class utility():#keyset
    def __init__(self, input_system):
        self.input_system = input_system
    
    def fullscreen(self):
        return self.input_system.keys[self.fullscreen_key] 

    input_system = None
    fullscreen_key = pygame.K_F11

class garden():#keyset
    def __init__(self, input_system):
        self.input_system = input_system
    
    def action(self):
        return self.input_system.keys[self.action_key] 

    input_system = None
    action_key = "mouse_0"

class spectator_mode():#keyset
    def __init__(self, input_system):
        self.input_system = input_system
    
    def w(self):
        return self.input_system.keys[self.w_key] 

    def a(self):
        return self.input_system.keys[self.a_key] 

    def s(self):
        return self.input_system.keys[self.s_key] 
        
    def d(self):
        return self.input_system.keys[self.d_key] 

    input_system = None
    w_key = pygame.K_w
    a_key = pygame.K_a
    s_key = pygame.K_s
    d_key = pygame.K_d

class Input_System():
    def __init__(self):
        self.spectator_mode = spectator_mode(self)
        self.garden = garden(self)
        self.utility = utility(self)

    def get_inputs(self):
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        mouse_presses = pygame.mouse.get_pressed()
        key = "mouse_0"
        if mouse_presses[0]:
            if self.keys[key] == 0 or self.keys[key] == 1:
                self.keys[key] = 2
            else:
                self.keys[key] = 3
        else:
            if self.keys[key] == 2 or self.keys[key] == 3:
                self.keys[key] = 1
            else:
                self.keys[key] = 0

        key = "mouse_2"
        if mouse_presses[2]:
            if self.keys[key] == 0 or self.keys[key] == 1:
                self.keys[key] = 2
            else:
                self.keys[key] = 3
        else:
            if self.keys[key] == 2 or self.keys[key] == 3:
                self.keys[key] = 1
            else:
                self.keys[key] = 0

        pressed_keys = pygame.key.get_pressed()
        
        for key_id in self.keys.keys():
            value = self.keys[key_id]
            if not (key_id == "mouse_0" or key_id == "mouse_2"):
                if pressed_keys[key_id]:
                    if value == 0 or value == 1:
                        self.keys[key_id] = 2
                    else:
                        self.keys[key_id] = 3
                else:
                    if value == 2 or value == 3:
                        self.keys[key_id] = 1
                    else:
                        self.keys[key_id] = 0

    #0 means not clicked 2 means just clicked 3 means held # 1 means released
    keys = {
        pygame.K_F11: 0, 
        pygame.K_w: 0, 
        pygame.K_a: 0, 
        pygame.K_s: 0, 
        pygame.K_d: 0, 
        "mouse_0":  0,
        "mouse_2":  0,        
    }
    
    mouse_pos_x = 0#position in pixels relative to window (0, 0) == top left corner
    mouse_pos_y = 0#position in pixels relative to window (0, 0) == top left corner

    spectator_mode = None
    garden = None
    utility = None