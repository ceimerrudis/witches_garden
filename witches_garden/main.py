#! ../witches_garden_env/Scripts/python
import pygame
from pygame.locals import *
from random import randint
from Screen import Screen
from Input_System import Input_System
from UI_Renderer import UI_Renderer
from Object_Renderer import Object_Renderer
from Game_Data import Game_Data
from UI_Logic_Controler import UI_Logic_Controler

class main():
    # Main loop dressed up as a class 
    # so that functions can acces the data without the need to make global variables
    
    TICKS_PER_SECOND = None # Number of "physics" updates  
    #the game tries to perform per second
    SKIP_TIME = None # miliseconds that each tick should take up
    
    # How many times a frame renderring can be skipped in order to try and 
    # catch up to the targeted amount of ticks per second
    MAX_FRAMESKIP = None
    # value used by pygame to limit the amount of frames renderred 
    # used to decrease ressource ussage and increase power efficiency
    FPS_LIMIT = None

    # Time between the seccond to last and last frame
    delta_time = None

    # simple colors used to diferentiete the outside and inside of the game viewport
    black = None
    green = None

    # A wrapper and more class for a pygame window surface
    screen = None

    # pygame clock
    clock = None
    # time when the next tick should be started
    next_game_tick = None

    # input system
    inputs = None

    # class dealing with actual game data and its manipulation
    game_data = None
    # stores ui objects
    ui_logic_ctrl = None
    
    obj_renderer = None
    ui_renderer = None

    # Simple rect existing in the world acting as a backdrop
    background_rect = None

    # bool
    running = None

    def __init__(self):
        self.TICKS_PER_SECOND = 30
        self.SKIP_TIME = 1000 / self.TICKS_PER_SECOND
        self.MAX_FRAMESKIP = 10
        self.FPS_LIMIT = 60

        self.delta_time = 0

        self.black = (0, 0, 0)
        self.green = (0, 60, 0)

        self.screen = Screen()
        self.screen.fill(self.black)

        self.clock = pygame.time.Clock()
        self.next_game_tick = pygame.time.get_ticks()

        self.inputs = Input_System()

        self.game_data = Game_Data()
        self.obj_renderer = Object_Renderer(self.screen)

        self.ui_logic_ctrl = UI_Logic_Controler(self.game_data, self.screen, self.Start_Game, self.Stop_Game)
        self.ui_renderer = UI_Renderer(self.screen, self.ui_logic_ctrl)

        self.background_rect = pygame.Rect(-1000, -1000, 2000, 2000)

        self.running = True

    def update(self):
        while self.running:# While the programm runs
            for event in pygame.event.get():
                # pygame events like window close window resize, inputs, etc
                if event.type == pygame.QUIT:
                    self.running = False    
                    break
                elif event.type == pygame.VIDEORESIZE:
                    width, height = event.w, event.h
                    self.screen.resize(width, height)
            
            if not self.running:
                break # if we just got news to shut the game down dont process update

            self.screen.fill(self.black) # clearing the screen
            # drawing the backdrop in worldspace
            self.screen.draw(self.green, self.background_rect) 
            self.delta_time = self.clock.tick(self.FPS_LIMIT)
    
            self.loops = 0;
            # This loop tries to execute "physics" updates if the time "asks" for it
            while (pygame.time.get_ticks() > self.next_game_tick and self.loops < self.MAX_FRAMESKIP):
                #get inputs
                self.inputs.get_inputs(self.screen.Calc_Mouse_Viewport_Position)
        
                #process the inputs
                self.ui_logic_ctrl.update(self.inputs)
                if self.game_data.initialized == True:
                    self.game_data.update(self.inputs)
        
                self.next_game_tick += self.SKIP_TIME;
                self.loops += 1

                #process inputs unrelated to game (fullsreen toggle and any others)
                if(self.inputs.utility.fullscreen() == 2):
                    self.screen.toggle_fullscreen()

            
            if self.game_data.initialized == True:
                self.screen.set_camera_pos(self.game_data.camera_pos)
            else:
                self.screen.set_camera_pos((0, 0))
    

            # Render the game
            #render the game world
            self.obj_renderer.render(self.game_data, self.ui_logic_ctrl.scene)
            #render all the ui elements in ui_logic_ctrl
            self.ui_renderer.render()
     
            pygame.display.update()

        #loop is broken
        pygame.quit()

    def Start_Game(self, parameters):
        #create game
        self.game_data.Initialize()
        self.ui_logic_ctrl.Initialize_Game_Screen(self.screen, self.game_data)

    def Stop_Game(self):
        self.game_data = Game_Data()
        self.obj_renderer = Object_Renderer(self.screen)
        self.ui_logic_ctrl = UI_Logic_Controler(self.game_data, self.screen, self.Start_Game, self.Stop_Game)
        self.ui_renderer = UI_Renderer(self.screen, self.ui_logic_ctrl)


main = main()# calls the actual main function
main.update()