#! ../witches_garden_env/Scripts/python

import pygame
from pygame.locals import *
import thorpy
import numpy
from random import randint
from Screen import Screen
from Input_System import Input_System
from UI_Renderer import UI_Renderer
from Object_Renderer import Object_Renderer

black = (0, 0, 0)
green = (0, 60, 0)

screen = Screen()
screen.fill(black)
delta_time = 0
FPS_LIMIT = 60
clock = pygame.time.Clock()
inputs = Input_System()
obj_renderer = Object_Renderer()
ui_renderer = UI_Renderer()

background_rect = pygame.Rect(-1000, -1000, 2000, 2000)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    
            break
        if event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            screen.resize(width, height)
          
    if not running:
        break
    screen.fill(black)
    screen.draw(green, background_rect)
    delta_time = clock.tick(FPS_LIMIT)
    
    #get inputs
    inputs.get_inputs()
    
    #process inputs unrelated to game (fullsreen toggle and any others)
    if(inputs.f_11 == 1):
        screen.toggle_fullscreen()

    #process the inputs
    #only deals with game logic
    #game.update(input)
    if(inputs.w == 1 or inputs.w == 2):
        screen.move_camera( 0, -1)
    if(inputs.s == 1 or inputs.s == 2):
        screen.move_camera( 0,  1)
    if(inputs.a == 1 or inputs.a == 2):
        screen.move_camera(-1,  0)
    if(inputs.d == 1 or inputs.d == 2):
        screen.move_camera( 1,  0)

    #render the game
    #spritepath = "witches_garden/sprites/"
    #plot = pygame.image.load(spritepath + "plot.png")
    #plot = pygame.transform.scale(plot, (64, 64))
    #screen.surface.blit(plot, pygame.Rect((100, 100), (64, 64)), pygame.Rect((6, 6), (64, 64)))

    #render the ui
    ui_renderer.render(screen)
    obj_renderer.render(screen)

    pygame.display.update()

pygame.quit()






































































"""
def Render_Text(window, what, color, font):
    text = font.render(what.txt, 1, pygame.Color(color))
    window.blit(text, (what.position.x, what.position.y))

class position:
    def __init__(self, xpos = 0, ypos = 0, yPrcntpos = 0, xPrcntpos = 0, anchor = 0):
        self.x = xpos
        self.y = ypos
        self.xPrcntpos = xPrcntpos
        self.yPrcntpos = yPrcntpos
        self.anchor = anchor
    x = 0
    y = 0
    xPrcnt = 0
    yPrcnt = 0
    anchor = 0

class uiObj:
    def __init__(self, pos, sprite = None, width = 0, height = 0, txt = None):
        self.position = pos
        if not width == 0:
            self.width = width
        if not height == 0: 
            self.height = height
        self.txt = txt
        self.sprite = sprite
    position = None
    width = 0
    height = 0
    sprite = None
    txt = None

class plant:
    def __init__(self, plantType, plantSprite):
        self.plantType = plantType
        self.plantSprite = plantSprite
    plantType = "grass"
    plantSprite = None

# MAIN _________________________________________________________________________________________
def main():
    pygame.init()

    FPS = 60
    clock = pygame.time.Clock()

    GREEN = (0, 70, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    screenW = 900
    screenH = 600
    screen = pygame.display.set_mode((screenW,screenH))
    screen.fill(GREEN)

    font = pygame.font.Font('witches_garden/fonts/kongtext.ttf', 30)
    pygame.display.set_caption("Witches garden")
    deltatime = 0

    spritepath = "witches_garden/sprites/"
    fireSprite = pygame.image.load(spritepath + "fire.png")
    fireplant = pygame.image.load(spritepath + "fireplant.png")
    grass = [pygame.image.load(spritepath + "grass1.png"), pygame.image.load(spritepath + "grass2.png"), pygame.image.load(spritepath + "grass3.png"), pygame.image.load(spritepath + "grass4.png")]
    iceplant = pygame.image.load(spritepath + "iceplant.png")
    plot = pygame.image.load(spritepath + "plot.png")
    water = pygame.image.load(spritepath + "water.png")
    
    arrowLeft = pygame.image.load(spritepath + "arrowLeft.png")
    arrowRight = pygame.image.load(spritepath + "arrowRight.png")
    seedSlot = pygame.image.load(spritepath + "seedSlot.png")
    topPannel = pygame.image.load(spritepath + "topPannel.png")
    bottomPannel = pygame.image.load(spritepath + "bottomPannel.png")

    rows, cols = 11, 11
    field = [[plant("grass", grass[randint(0, len(grass)-1)])] for i in range(cols)] for i in range(cols)
    staticuiObjects = [ uiObj(bottomPannel, position(anchor = 8), 0, 64),
                        #uiObj(arrowLeft, position(), 0, 64), 
                        #uiObj(arrowRight, position(anchor = 8), 0, 64),
                        uiObj(topPannel, position(anchor = 3), 48, 64)]
    fpsMeter = uiObj(txt = "0", pos = position(xpos = 0, ypos = 0, anchor = 1), width = 0, height = 0)#TODO

    print(field[0][1].plantType)
    field[0][0].plantType = "dif"
    print(field[0][0].plantType)
    print(field[0][1].plantType)
    
    #TODO set up field

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False    
                continue
        screen.fill(GREEN)
        deltatime = clock.tick(60)
    
    
        #code	
        #pressed_keys = pygame.key.get_pressed()
        #if pressed_keys[K_UP]:
            #self.rect.move_ip(0, -5)
    
        #renderUI
        #TODO render field

        object2 = pygame.Rect((10, 10), (100, 100))
        #pygame.draw.rect(screen, BLACK, object2)

        fpsMeter.txt = str(int(clock.get_fps()))
        Render_Text(screen, fpsMeter, BLACK, font)
        pygame.display.update()
    pygame.quit()
main()
"""