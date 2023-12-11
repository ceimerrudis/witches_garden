import pygame

# Each class holds the different possible inputs for that purpose
class utility():#keyset
    input_system = None
    fullscreen_key = None

    def __init__(self, input_system):
        self.input_system = input_system
        self.fullscreen_key = pygame.K_F11
    
    def fullscreen(self):
        return self.input_system.keys[self.fullscreen_key] 

class garden():#keyset
    input_system = None
    action_key = None
    cancel_key = None
    plant_key = None
    root_key = None
    end_turn_key = None
    
    one_key = None
    two_key = None
    three_key = None
    four_key = None
    five_key = None
    six_key = None
    seven_key = None
    eight_key = None
    nine_key = None
    zero_key = None

    def __init__(self, input_system):
        self.input_system = input_system
        self.action_key = "mouse_0"
        self.cancel_key= "mouse_2"# right click
        self.plant_key = pygame.K_p
        self.root_key = pygame.K_r
        self.end_turn_key = pygame.K_e
    
        self.one_key = [pygame.K_1, pygame.K_KP1]
        self.two_key = [pygame.K_2, pygame.K_KP2]
        self.three_key = [pygame.K_3, pygame.K_KP3]
        self.four_key = [pygame.K_4, pygame.K_KP4]
        self.five_key = [pygame.K_5, pygame.K_KP5]
        self.six_key = [pygame.K_6, pygame.K_KP6]
        self.seven_key = [pygame.K_7, pygame.K_KP7]
        self.eight_key = [pygame.K_8, pygame.K_KP8]
        self.nine_key = [pygame.K_9, pygame.K_KP9]
        self.zero_key = [pygame.K_0, pygame.K_KP0]
    
    def action(self):
        return self.input_system.keys[self.action_key]
    
    def cancel(self):
        return self.input_system.keys[self.cancel_key]

    def plant(self):
        return self.input_system.keys[self.plant_key]

    def root(self):
        return self.input_system.keys[self.root_key]

    def end_turn(self):
        return self.input_system.keys[self.end_turn_key]

    def one(self):
        return max(self.input_system.keys[self.one_key[0]], self.input_system.keys[self.one_key[1]])

    def two(self):
        return max(self.input_system.keys[self.two_key[0]], self.input_system.keys[self.two_key[1]])

    def three(self):
        return max(self.input_system.keys[self.three_key[0]], self.input_system.keys[self.three_key[1]])

    def four(self):
        return max(self.input_system.keys[self.four_key[0]], self.input_system.keys[self.four_key[1]])

    def five(self):
        return max(self.input_system.keys[self.five_key[0]], self.input_system.keys[self.five_key[1]])

    def six(self):
        return max(self.input_system.keys[self.six_key[0]], self.input_system.keys[self.six_key[1]])

    def seven(self):
        return max(self.input_system.keys[self.seven_key[0]], self.input_system.keys[self.seven_key[1]]) 

    def eight(self):
        return max(self.input_system.keys[self.eight_key[0]], self.input_system.keys[self.eight_key[1]])

    def nine(self):
        return max(self.input_system.keys[self.nine_key[0]], self.input_system.keys[self.nine_key[1]])

    def zero(self):
        return max(self.input_system.keys[self.zero_key[0]], self.input_system.keys[self.zero_key[1]])

class spectator_mode():#keyset
    input_system = None
    w_key = None
    a_key = None
    s_key = None
    d_key = None

    def __init__(self, input_system):
        self.input_system = input_system
        self.w_key = pygame.K_w
        self.a_key = pygame.K_a
        self.s_key = pygame.K_s
        self.d_key = pygame.K_d
    
    def w(self):
        return self.input_system.keys[self.w_key] 

    def a(self):
        return self.input_system.keys[self.a_key] 

    def s(self):
        return self.input_system.keys[self.s_key] 
        
    def d(self):
        return self.input_system.keys[self.d_key] 

class Input_System():
    #0 means not clicked 2 means just clicked 3 means held # 1 means released
    keys = None
    
    mouse_pos_x = None#position in pixels relative to window (0, 0) == top left corner
    mouse_pos_y = None#position in pixels relative to window (0, 0) == top left corner
    mouse_x = None#Mouse position in game viewport pixels
    mouse_y = None#Mouse position in game viewport pixels

    spectator_mode = None
    garden = None
    utility = None

    def __init__(self):
        self.spectator_mode = spectator_mode(self)
        self.garden = garden(self)
        self.utility = utility(self)

        self.keys = {
            pygame.K_F11: 0, 
            pygame.K_w: 0, 
            pygame.K_a: 0, 
            pygame.K_s: 0, 
            pygame.K_d: 0, 
            pygame.K_p: 0, 
            pygame.K_r: 0, 
            pygame.K_e: 0, 
            pygame.K_0: 0, 
            pygame.K_1: 0, 
            pygame.K_2: 0, 
            pygame.K_3: 0, 
            pygame.K_4: 0, 
            pygame.K_5: 0, 
            pygame.K_6: 0, 
            pygame.K_7: 0, 
            pygame.K_8: 0, 
            pygame.K_9: 0, 

            pygame.K_KP0: 0, 
            pygame.K_KP1: 0, 
            pygame.K_KP2: 0, 
            pygame.K_KP3: 0, 
            pygame.K_KP4: 0, 
            pygame.K_KP5: 0, 
            pygame.K_KP6: 0, 
            pygame.K_KP7: 0, 
            pygame.K_KP8: 0, 
            pygame.K_KP9: 0, 
            "mouse_0":  0,
            "mouse_2":  0,        
        }
    
        self.mouse_pos_x = 0
        self.mouse_pos_y = 0
        self.mouse_x = 0
        self.mouse_y = 0

    def get_inputs(self, mouse_to_viewportmouse):
        # pygme handles the mouse seperatley and so must I
        self.mouse_pos_x, self.mouse_pos_y = pygame.mouse.get_pos()
        self.mouse_x, self.mouse_y = mouse_to_viewportmouse(self.mouse_pos_x, self.mouse_pos_y)
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


        # This part deals with taking keyboard input
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