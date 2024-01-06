import pygame
from pygame.locals import *
from Get_Sprite import Get_Sprite, Get_Seed_Sprite, Get_Plant_Sprite
from Nine_Slice import Nine_Slice_Rect, nine_slice
from Game_Action_Wrapper import Game_Action_Wrapper
from Enums import Event_Types, Image_Type, UI_Object_Type
from Plant_Info import Plant_Type, Plant_Type_To_Display_Name, Get_Plant_Conditions, Get_Plant_Effect

class UI_Object():
    #stores and proceses info about this object
    drag_state = None #0 - not draged 1 - started draging 2 - being draged
    #There is no state for release because all the logic for it happens n the update

    events = None#Dictionary with functions and parameters to be executed at specific moments

    image = None #Holds the pygame surface object of the image to display

    rect = None #The entire area of the screen in viewport coordinates

    rects = None #A list with all the rects for a nine sliced image

    sorting_order = None#All objects of a single screen are sorted acording to this value
    #higher value means in front.

    image_type = None #See Enums

    object_type = None #See Enums

    def __init__(self, image, image_type, object_type, sorting_order, rects=None, rect=None):
        self.drag_state = 0
        self.sorting_order = sorting_order 
        self.image_type = image_type
        self.object_type = object_type
        self.image = image
        
        self.events = {
            Event_Types.on_click: [],
            Event_Types.on_begin_drag: [],
            Event_Types.on_end_drag: [],
        }

        if not rect is None:
            self.rect = rect
        elif not rects is None:
            self.rects = rects
            total_rect = pygame.Rect(self.rects[0][0].x,
                                     self.rects[0][0].y,
                                     self.rects[len(self.rects) - 1][0].x - self.rects[0][0].x + self.rects[
                                         len(self.rects) - 1][0].w,
                                     self.rects[len(self.rects) - 1][0].y - self.rects[0][0].y + self.rects[
                                         len(self.rects) - 1][0].h)
            self.rect = total_rect
        else:
            print("Failed to create ui object")
            return 1

    def Hovering_Over(self, mouse_x, mouse_y):
        # This funcion cares about the rect not the image 
        # so an image of a circle still has a square "hitbox"
        if self.rect.x <= mouse_x and self.rect.x + self.rect.w >= mouse_x and self.rect.y <= mouse_y and self.rect.y + self.rect.h >= mouse_y:
            return True
        return False

    def update(self, input_sys):
        # Deal with drag state changes and drag events
        if self.drag_state == 1:
            self.Execute_Events(Event_Types.on_begin_drag, input_sys)
            self.drag_state = 2
        if self.drag_state > 0:
            # the int(rect...) is an offset so the seed is centered on cursor
            self.Update_Position(input_sys.mouse_x - int(self.rect.w / 2), input_sys.mouse_y - int(self.rect.h / 2), True)
            if input_sys.garden.action() == 1:
                self.Execute_Events(Event_Types.on_end_drag, input_sys)
                self.Stop_Draging(input_sys)

        # Deal with clicks
        if self.object_type == UI_Object_Type.button:
            if input_sys.garden.action() == 2:
                if self.Hovering_Over(input_sys.mouse_x, input_sys.mouse_y):
                    self.Execute_Events(Event_Types.on_click, input_sys)

    def Start_Draging(self):
        self.drag_state = 1 #Seperate function so it can be called from an event

    def Stop_Draging(self, input_sys):
        self.drag_state = 0 #Seperate function so it can be called from an event

    def Add_Event(self, ev_type, ev, param):
        #ev is a function
        #param is a tuple with all necesary params
        self.events[ev_type].append((ev, param))
    
    def Execute_Events(self, event_type, input_sys):
        #Executes all events of event_type
        for i in range(len(self.events[event_type])):
            if self.events[event_type][i][1] == None:
                #Functions that do not take parameters arent expecting a None param
                # so it is ignored
                self.events[event_type][i][0]()
            else:
                self.events[event_type][i][0](self.events[event_type][i][1])

    def Update_Position(self, x, y, set_pos=False):
        if set_pos:
            if not self.rects is None:
                origin_x = self.rect.x
                origin_y = self.rect.y
                for rect in self.rect:
                    dif_x = rect.x - origin_x
                    dif_y = rect.y - origin_y
                    rect.x = x + dif_x
                    rect.y = y + dif_y
            if not self.rect is None:
                self.rect.x = x
                self.rect.y = y
        else:
            if not self.rects is None:
                for rect in self.rects:
                    self.rect.x += x
                    self.rect.y += y
            if not self.rect is None:
                self.rect.x += x
                self.rect.y += y

class UI_Screen():
    # Base class for the diferent ui screens that are in the game (main menu, game screen, pause screen, etc)
    
    ui_objects = None # List of ui objects sorted by the objects sorting order
    #Must add objects through Add_Object function

    def __init__(self):
        self.ui_objects = []
    
    def Add_Object(self, obj_to_add):
        self.ui_objects.append(obj_to_add)
        self.ui_objects = sorted(self.ui_objects, key=lambda obj: obj.sorting_order)

    def update(self, input_sys):
        #let each object update it self
        for ui_obj in self.ui_objects:
            ui_obj.update(input_sys)

class Main_Menu_Screen(UI_Screen):
    level = None # currently unused acts a example on how systems can be developed in the future
    start_game_function = None # a function from Main class 

    def __init__(self, screen_width, screen_height, start_game_function):
        # Screen size in needed so the button can be placed in the center
        super().__init__()
    
        self.level = 1
        self.start_game_function = start_game_function
        
        img = Get_Sprite("start_btn")
        rect = pygame.Rect(int(screen_width / 2) - 30, int(screen_height / 2) - 10, 60, 20)
        obj = UI_Object(img, Image_Type.basic, UI_Object_Type.button, 1, rect = rect)
        obj.Add_Event(Event_Types.on_click, self.StartGame, None)
        self.Add_Object(obj)

    def StartGame(self):
        start_game_function_parameters = []
        start_game_function_parameters.append(self.level)# Unused
        self.start_game_function(start_game_function_parameters)

class Pause_Screen(UI_Screen):    
    def __init__(self, screen_width, screen_height, Disable_Pause_Function, To_Main_Menu_Function):
        super().__init__()

        img = Get_Sprite("back_btn")
        rect = pygame.Rect(screen_width / 2 - 30, screen_height / 2 - 22, 60, 20)
        obj = UI_Object(img, Image_Type.basic, UI_Object_Type.button, 2, rect = rect)
        self.Add_Object(obj)
        obj.Add_Event(Event_Types.on_click, Disable_Pause_Function, None)
        
        img = Get_Sprite("menu_btn")
        rect = pygame.Rect(screen_width / 2 - 30, screen_height / 2 + 2, 60, 20)
        obj = UI_Object(img, Image_Type.basic, UI_Object_Type.button, 2, rect = rect)
        self.Add_Object(obj)
        obj.Add_Event(Event_Types.on_click, To_Main_Menu_Function, None)

        img = Get_Sprite("gray")
        rect = pygame.Rect(-100, -100, 400, 400)
        self.Add_Object(UI_Object(img, Image_Type.basic, UI_Object_Type.image, 0, rect = rect))

class Game_Screen(UI_Screen):
    seed_list = None # A copy of game data seed list if copies are not eaqul the list is remade
    seed_obj_list = None # Contains tuples that hold references to 
    #               (seed sprite objects, seed count obj, seed name obj, plant_type)
    
    effect_texts = None # Holds references to action text objects (on screen text that indicates which action just happened)
    #as well as time of creation so they can be properly destroyed
    time_of_last_effect_text = None #time when last spawned effect text
    effect_text_time_interval = None #amount of time that can pass between effect texts
    time_to_delete_effect_text = None #time that text stays on screen

    selected_seed_id = None
    slots = None #list of references to slots
    game_data_seeds = None # The actual game data seed list
    ui_logic_controler = None
    uprooting = None
    fonts = None #dictionary of fonts

    text_pannel = None # reference needed to place info text in the correct place
    text_pannel_text_objs = None # List of info text object
    game_data = None
    score_obj = None # Text displaying score

    def __init__(self, screen_width, screen_height, game_data, logic_controler):
        super().__init__()

        self.uprooting = False
        self.ui_logic_controler = logic_controler
        self.seed_list = []
        self.seed_obj_list = []
        self.selected_seed_id = 0
        self.slots = []
        self.game_data_seeds = game_data.seeds
        self.game_data = game_data

        self.fonts = {}
        pygame.font.init()
        fontPath = None#"witches_garden/fonts/pixelifysans/static/PixelifySans-Regular.ttf"
        self.fonts["default"] = pygame.font.Font(fontPath, 24)
        self.fonts["seed_count"] = pygame.font.Font(fontPath, 40)
        self.fonts["info"] = pygame.font.Font(fontPath, 30)
        self.fonts["score"] = pygame.font.Font(fontPath, 36)
        self.fonts["effecttext"] = pygame.font.Font(fontPath, 30)
        self.time_of_last_effect_text = pygame.time.get_ticks()
        self.effect_text_time_interval = 350 
        self.time_to_delete_effect_text = 1400
        self.effect_texts = []

        # Adding ui objects

        #slice_values
        l, t, r, b = 26, 26, 26, 26
        img, c_w, c_h = nine_slice(Get_Sprite("bottom"), l, t, r, b)
        rect = pygame.Rect(0, screen_height - 64, screen_width, 64)
        sliced_rect = Nine_Slice_Rect(rect, l, t, r, b, c_w, c_h)
        bottom_panel_object = UI_Object(img, Image_Type.nine_sliced, UI_Object_Type.image, 0, rects = sliced_rect)
        self.Add_Object(bottom_panel_object)

        img = Get_Sprite("arrowLeft")
        rect = pygame.Rect(8, screen_height - 50, 18, 36)
        obj = UI_Object(img, Image_Type.basic, UI_Object_Type.button, 2, rect = rect)
        self.Add_Object(obj)
        obj.Add_Event(Event_Types.on_click, self.Shift_Seeds_Left, None)
        
        img = Get_Sprite("arrowRight")
        rect = pygame.Rect(screen_width - 8 - 18, screen_height - 50, 18, 36)
        obj = UI_Object(img, Image_Type.basic, UI_Object_Type.button, 2, rect = rect)
        self.Add_Object(obj)
        obj.Add_Event(Event_Types.on_click, self.Shift_Seeds_Right, None)

        img = Get_Sprite("top")
        rect = pygame.Rect(screen_width - 48, 0, 48, 128)
        self.text_pannel = UI_Object(img, Image_Type.basic, UI_Object_Type.image, 0, rect = rect)
        self.Add_Object(self.text_pannel)

        self.score_obj = self.Create_Text_Object("score", "score: 0 / 1", self.text_pannel.rect.x + 4, self.text_pannel.rect.y + 73)
        self.score_obj.score = 0
        self.score_obj.turn = 0

        img = Get_Sprite("hourglass")
        child_rect = pygame.Rect(rect.x + 6, rect.y + rect.h - 4 - 16, 16, 16)
        obj = UI_Object(img, Image_Type.basic, UI_Object_Type.button, 1, rect = child_rect)
        self.Add_Object(obj)
        obj.Add_Event(Event_Types.on_click, game_data.End_Turn, None)

        img = Get_Sprite("shovel")
        child_rect = pygame.Rect(rect.x + 6 + 16 + 4, rect.y + rect.h - 4 - 16, 16, 16)
        obj = UI_Object(img, Image_Type.basic, UI_Object_Type.button, 1, rect = child_rect)
        self.Add_Object(obj)
        obj.Add_Event(Event_Types.on_click, self.Start_uprooting, None)

        img = Get_Sprite("pause")
        child_rect = pygame.Rect(rect.x + 6, rect.y + rect.h - 5 - 32 -2, 16, 16)
        obj = UI_Object(img, Image_Type.basic, UI_Object_Type.button, 1, rect = child_rect)
        self.Add_Object(obj)
        obj.Add_Event(Event_Types.on_click, self.ui_logic_controler.Initialize_Pause_Screen, None)

        img = Get_Sprite("undo")
        child_rect = pygame.Rect(rect.x + 6 + 16 + 4, rect.y + rect.h - 5 - 32 - 2, 16, 16)
        obj = UI_Object(img, Image_Type.basic, UI_Object_Type.button, 1, rect = child_rect)
        self.Add_Object(obj)
        obj.Add_Event(Event_Types.on_click, self.ui_logic_controler.Call_Undo, None)

        for i in range(4):
            img = Get_Sprite("slot")
            rect = pygame.Rect(29 + (i * 42), screen_height - 52, 40, 40)
            obj = UI_Object(img, Image_Type.basic, UI_Object_Type.image, 2, rect = rect)
            self.Add_Object(obj)
            self.slots.append(obj)

        self.Update_Seed_List()

    def update(self, input_sys):
        if self.uprooting:# must be called before super update because buttons call start uproot and the uproot could end on the same frame
            if input_sys.garden.action() == 2:
                self.End_uprooting()
            if input_sys.garden.cancel() == 2:
                self.End_uprooting()

        super().update(input_sys)

        #displaying info about the plant under cursor
        plant_map = self.ui_logic_controler.scene.plants 
        x, y = self.ui_logic_controler.surface.ViewportToWorldPos(input_sys.mouse_x, input_sys.mouse_y)
        x, y = plant_map.Get_Map_Pos_From_World_pos(x, y)
        
        # BUG seed info dissapears when holding seed over grass (or field in general)
        plant = self.game_data.Get_Plant(x, y)
        if plant == None:
            plant_found = False
            for item in self.seed_obj_list:
                if item[0].Hovering_Over(input_sys.mouse_x, input_sys.mouse_y):
                    plant_found = True
                    self.Display_Seed_Info(item[3])
            if not plant_found: 
                self.Display_Plant_Info(None)
        else:
            self.Display_Plant_Info(plant)
                    

        #displaying the correct score
        if not (self.score_obj.score == self.game_data.score and self.score_obj.turn == self.game_data.turn):
            self.score_obj.score = self.game_data.score
            self.score_obj.turn = self.game_data.turn
            score_txt = "score: " + str(self.score_obj.score) + " / " + str(self.score_obj.turn + 1)
            sz = self.fonts["score"].size(score_txt)
            self.score_obj.rect.w = sz[0]
            self.score_obj.rect.h = sz[1]
            
            self.score_obj.image = self.fonts["score"].render(score_txt, False, (255,255,255))

        #move effect texts upward
        for textobj in self.effect_texts:
            textobj[0].Update_Position(0, -1)
            if textobj[1] + self.time_to_delete_effect_text < pygame.time.get_ticks():
                self.ui_objects.remove(textobj[0])
                self.effect_texts.remove(textobj)

        #Add any effect texts and remove them from the game data
        if len(self.game_data.effect_texts) > 0 and self.time_of_last_effect_text + self.effect_text_time_interval < pygame.time.get_ticks():
            self.Create_Effect_Text(self.game_data.effect_texts[0])
            self.game_data.effect_texts.pop(0)
            self.time_of_last_effect_text = pygame.time.get_ticks()

        self.Update_Seed_List()

    def Display_Plant_Info(self, plant):
        if self.text_pannel == None:
            print("error")
            return
        if self.text_pannel_text_objs == None:
            self.text_pannel_text_objs = []
        else:
            for item in self.text_pannel_text_objs:
                self.ui_objects.remove(item)
            self.text_pannel_text_objs.clear()
        if plant == None:
            return
        if plant.plant_type == Plant_Type.plot or plant.plant_type == Plant_Type.grass1 or plant.plant_type == Plant_Type.grass2 or plant.plant_type == Plant_Type.grass3 or plant.plant_type == Plant_Type.grass4:
            return
        info = "test"    
        for i in range(8):
            if i == 0:
                info = "plant: " + Plant_Type_To_Display_Name(plant.plant_type)
            if i == 1:
                info = "age: " + str(plant.age)
            if i == 2:
                info = "light: " + str(plant.light)
            if i == 3:
                info = "heat: " + str(plant.temperature)
            if i == 4:
                info = "water: " + str(plant.water)
            if i == 5:
                info = "charge: " + str(plant.charge)
            if i == 6:
                info = "bugs: " + str(plant.bugs)
            if i == 7:
                info = "poison: " + str(plant.poison)
            if i == 8:
                info = "flags: " + str(plant.flags)
            
            x, y = self.text_pannel.rect.x + 3, self.text_pannel.rect.y + 5 + (8 * i)
            obj = self.Create_Text_Object("info", info, x, y)
            self.text_pannel_text_objs.append(obj)

    def Display_Seed_Info(self, plant_type):
        if self.text_pannel == None:
            print("error")
            return
        if self.text_pannel_text_objs == None:
            self.text_pannel_text_objs = []
        else:
            for item in self.text_pannel_text_objs:
                self.ui_objects.remove(item)
            self.text_pannel_text_objs.clear()
        if plant_type == Plant_Type.plot or plant_type == Plant_Type.grass1 or plant_type == Plant_Type.grass2 or plant_type == Plant_Type.grass3 or plant_type == Plant_Type.grass4:
            return
        info = "test"    

        conditions = Get_Plant_Conditions(plant_type)
        effects = Get_Plant_Effect(plant_type, 20)# 20 is the assumed age
        j = 0
        for i in range(8):
            if i == 0:
                info = "plant: " + Plant_Type_To_Display_Name(plant_type)
            if i == 1:
                info = "cond / effects"
            if i == 2:
                info = "light: " + str(conditions["light"]) + " / " + str(effects["light"])
            if i == 3:
                info = "heat: " + str(conditions["temperature"]) + " / " + str(effects["temperature"])
            if i == 4:
                info = "water: " + str(conditions["water"]) + " / " + str(effects["water"])
            if i == 5:
                info = "charge: " + str(conditions["charge"]) + " / " + str(effects["charge"])
            if i == 6:
                info = "bugs: " + str(conditions["bugs"]) + " / " + str(effects["bugs"])
            if i == 7:
                info = "poison: " + str(conditions["poison"]) + " / " + str(effects["poison"])
            
            x, y = self.text_pannel.rect.x + 3, self.text_pannel.rect.y + 5 + (8 * i)
            obj = self.Create_Text_Object("info", info, x, y)
            self.text_pannel_text_objs.append(obj)

    def Create_Text_Object(self, font_name, text, position_x = 0, position_y = 0, color = (255, 255, 255), layer = 5):
        if not font_name in self.fonts.keys():
            return

        sz = self.fonts[font_name].size(text)
        rect = pygame.Rect(position_x, position_y, sz[0], sz[1])

                                                #antialiass
        img = self.fonts[font_name].render(text, False, color)
        obj = UI_Object(img, Image_Type.basic, UI_Object_Type.text, layer, rect = rect)
        self.Add_Object(obj)
        return obj

    def Create_Effect_Text(self, text):
        obj = self.Create_Text_Object("effecttext", text, 10, 150)
        self.effect_texts.append((obj, pygame.time.get_ticks()))

    def Start_uprooting(self):
        self.uprooting = True

    def End_uprooting(self):
        self.uprooting = False
        self.ui_logic_controler.Call_Up_Root(["MOUSE_X", "MOUSE_Y"])

    def Shift_Seeds_Left(self):
        if not self.selected_seed_id == 0:
            self.selected_seed_id -= 1
            self.Update_Seed_List(True)
            # Force update even if local seed list is same as game_data

    def Shift_Seeds_Right(self):
        if self.selected_seed_id + 1 < len(self.game_data_seeds):
            self.selected_seed_id += 1
            self.Update_Seed_List(True)
            # Force update even if local seed list is same as game_data

    def Update_Seed_List(self, force_update = False):
        ls = []
        for key in self.game_data_seeds.keys():# Reform game data seed list
            ls.append((key.value, self.game_data_seeds[key]))
        ls = sorted(ls)

        # Only update if lists aren't the same or if forced
        if ls == self.seed_list and not force_update:
            return

        # destroy all seed objects
        self.seed_list = ls
        for seed in self.seed_obj_list:
            self.ui_objects.remove(seed[0])
            self.ui_objects.remove(seed[1])
            self.ui_objects.remove(seed[2])
        self.seed_obj_list.clear()

        # create all objects
        if len(self.seed_list) > self.selected_seed_id:
            for i in range(self.selected_seed_id, self.selected_seed_id + 4):
                if i + 1 <= len(self.seed_list):#this entry exists
                    inner_rect = pygame.Rect(self.slots[i - self.selected_seed_id].rect.x + 4, self.slots[i - self.selected_seed_id].rect.y + 4, 32, 32)
                    seed_obj = UI_Object(Get_Seed_Sprite(Plant_Type(self.seed_list[i][0])), Image_Type.basic, UI_Object_Type.button, 3, rect = inner_rect)
                    
                    seed_obj.Add_Event(Event_Types.on_click, seed_obj.Start_Draging, None)
                    seed_obj.Add_Event(Event_Types.on_end_drag, self.ui_logic_controler.Call_Plant, ["MOUSE_X", "MOUSE_Y", Plant_Type(self.seed_list[i][0])])
                    seed_obj.Add_Event(Event_Types.on_end_drag, self.Update_Seed_List, True)
                    
                    count = (self.Create_Text_Object("seed_count", str(self.seed_list[i][1]), inner_rect.x + 20, inner_rect.y + 20))
                    name = (self.Create_Text_Object("info", Plant_Type_To_Display_Name(Plant_Type(self.seed_list[i][0])), inner_rect.x, inner_rect.y + 28))
                    
                    self.seed_obj_list.append((seed_obj, name, count, Plant_Type(self.seed_list[i][0])))                   
                    self.Add_Object(seed_obj)

class GameEndedScreen(UI_Screen):
    fonts = None

    def __init__(self, screen_width, screen_height, score, MainMenu):
        # Screen size in needed so the button can be placed in the center
        super().__init__()
        
        self.fonts = {}
        pygame.font.init()
        self.fonts["default"] = pygame.font.Font(None, 60)
        self.Create_Text_Object("default", "The game has ended", int(screen_width / 2) - 50, 60)
        self.Create_Text_Object("default", "your score was " + str(score), int(screen_width / 2) - 50, 80)
        
        img = Get_Sprite("menu_btn")
        rect = pygame.Rect(int(screen_width / 2) - 30, int(screen_height / 2) - 10, 60, 20)
        obj = UI_Object(img, Image_Type.basic, UI_Object_Type.button, 1, rect = rect)
        obj.Add_Event(Event_Types.on_click, MainMenu, None)
        self.Add_Object(obj)

    def Create_Text_Object(self, font_name, text, position_x = 0, position_y = 0, color = (255, 255, 255), layer = 5):
        if not font_name in self.fonts.keys():
            return

        sz = self.fonts[font_name].size(text)
        rect = pygame.Rect(position_x, position_y, sz[0], sz[1])

                                                #antialiass
        img = self.fonts[font_name].render(text, False, color)
        obj = UI_Object(img, Image_Type.basic, UI_Object_Type.text, layer, rect = rect)
        self.Add_Object(obj)
        return obj



class Game_Scene():
    # Holds all data about the "game object" visuals
    background = None # tilemap
    plants = None # tilemap

    def __init__(self, game_data):
        self.background = Tilemap(game_data.field_size_x, game_data.field_size_y)
        self.plants = Tilemap(game_data.field_size_x, game_data.field_size_y)

class Tilemap():
    #Holds info about tiles and performs calculations when needed
    tiles = None
    tile_width = None
    tile_height = None
    map_width = None
    map_height = None
    pos_x = None
    pos_y = None

    def __init__(self, map_width, map_height, tile_width=16, tile_height=16):
        self.tiles = []
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.map_width = map_width
        self.map_height = map_height

        self.pos_x = 0
        self.pos_y = 16

        for i in range(self.map_height):
            self.tiles.append([])
            for j in range(self.map_width):
                xpos = j * self.tile_width
                ypos = (self.map_height * self.tile_height) - ((self.map_width - i - 1) * self.tile_height)
                tile = Tile_Obj(None, pygame.Rect(xpos, ypos, self.tile_width, self.tile_height))
                self.tiles[i].append(tile)

    def Get_Map_Pos_From_World_pos(self, x, y):
        return ((x-self.pos_x) // self.tile_width), ((y-self.pos_y) // self.tile_height)

    def Get_Tile(self, x, y):
        return self.tiles[x][y]

    def Set_Tile(self, x, y, tile):
        self.tiles[x][y] = tile

class Tile_Obj():
    p_type = None
    age = 0
    rect = None
    image = None

    def __init__(self, img, rect, p_type = None, age = 0):
        self.image = img
        self.rect = rect
        self.p_type = p_type
        self.age = age
