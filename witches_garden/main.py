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

def Start_Game(parameters):
    #create game
    game_data.Initialize()
    obj_renderer.Initialize()
    ui_logic_ctrl.Initialize_Game_Screen(screen, game_data)

TICKS_PER_SECOND = 30
SKIP_TIME = 1000 / TICKS_PER_SECOND
MAX_FRAMESKIP = 10
FPS_LIMIT = 60

delta_time = 0

black = (0, 0, 0)
green = (0, 60, 0)

screen = Screen()
screen.fill(black)

clock = pygame.time.Clock()
next_game_tick = pygame.time.get_ticks()

inputs = Input_System()

game_data = Game_Data()
obj_renderer = Object_Renderer(screen)

ui_logic_ctrl = UI_Logic_Controler(game_data, screen, Start_Game)
ui_renderer = UI_Renderer(screen, ui_logic_ctrl)

background_rect = pygame.Rect(-1000, -1000, 2000, 2000)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    
            break
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            screen.resize(width, height)
            
          
    if not running:
        break
    screen.fill(black)
    screen.draw(green, background_rect)
    delta_time = clock.tick(FPS_LIMIT)
    
    loops = 0;
    while (pygame.time.get_ticks() > next_game_tick and loops < MAX_FRAMESKIP):
        #get inputs
        inputs.get_inputs(screen.Calc_Mouse_Viewport_Position)
        
        #process the inputs
        ui_logic_ctrl.update(inputs)
        if game_data.initialized == True:
            game_data.update(inputs)
        
        next_game_tick += SKIP_TIME;
        loops += 1

    #process inputs unrelated to game (fullsreen toggle and any others)
    if(inputs.utility.fullscreen() == 2):
        screen.toggle_fullscreen()

    if game_data.initialized == True:
        screen.set_camera_pos(game_data.camera_pos)
    else:
        screen.set_camera_pos((0, 0))
    
    #render the game
    #render the game world
    if obj_renderer.initialized == True:
        obj_renderer.render(game_data, ui_logic_ctrl.scene)
    
    #render all the elements in ui_logic_ctrl
    ui_renderer.render()
     
    pygame.display.update()

pygame.quit()