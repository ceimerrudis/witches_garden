import pygame
from Display_Objects import *

class UI_Logic_Controler():
    # Parent class that holds all data to do with user interface
    # this includes game object sprite data
    game_data = None
    active_screens = None
    scene = None
    game_action_wrapper = None
    surface = None
    input_sys = None
    stop_game_function = None
    
    def __init__(self, game_data, surface, start_game_function, stop_game_function):
        self.game_action_wrapper = Game_Action_Wrapper(game_data)
        self.game_data = game_data
        self.stop_game_function = stop_game_function
        self.surface = surface
        # Begin the user interface on the main menu page
        self.active_screens = [Main_Menu_Screen(surface.screen_width, surface.screen_height, start_game_function)]

    def Initialize_Game_Screen(self, surface, game_data):
        #Initialize the children which will each take care of their own data ()
        self.scene = Game_Scene(game_data)
        # overriding list to make sure no layer is is stuck
        self.active_screens = [Game_Screen(surface.screen_width, surface.screen_height, self.game_data, self)]

    def Initialize_Pause_Screen(self):
        self.active_screens.append(Pause_Screen(self.surface.screen_width, self.surface.screen_height, self.Disable_Pause, self.stop_game_function))

    def Disable_Pause(self):
        self.active_screens.pop(-1)

    def update(self, input_sys):
        #Update only the top most screen
        self.input_sys = input_sys
        self.active_screens[-1].update(input_sys)
        
    def Call_Plant(self, parameters):
        self.Process_Parameters(parameters)
        self.game_action_wrapper.Plant(parameters)

    def Call_Up_Root(self, parameters):
        self.Process_Parameters(parameters)
        self.game_action_wrapper.Up_Root(parameters)

    def Call_Undo(self):
        self.game_action_wrapper.Undo()

    def Process_Parameters(self, parameters):
        # Certain parameters are simply key strings instead of their actual values
        # this function sets the parameters to the correct values
        for i in range(len(parameters)):
            if parameters[i] == "MOUSE_X":
                x, y = self.surface.ScreenToWorldPos(self.input_sys.mouse_x, self.input_sys.mouse_y)
                parameters[i], dump = self.scene.plants.Get_Map_Pos_From_World_pos(x, y)
            if parameters[i] == "MOUSE_Y":
                x, y = self.surface.ScreenToWorldPos(self.input_sys.mouse_x, self.input_sys.mouse_y)
                dump, parameters[i] = self.scene.plants.Get_Map_Pos_From_World_pos(x, y)