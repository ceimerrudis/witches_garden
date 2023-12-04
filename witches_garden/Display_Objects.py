import pygame
from pygame.locals import *
from Get_Sprite import Get_Sprite, Get_Seed_Sprite, Get_Plant_Sprite
from Nine_Slice import Nine_Slice_Rect, nine_slice
from Game_Action_Wrapper import Game_Action_Wrapper
from Enums import Event_Types, Plant_Type

class UI_Object():
    curently_draged = None
    
    events = None

    image = None
    rect = None
    rects = None
    sorting_layer = None
    image_type = None
    # 0 for normal image 
    # 1 for nine sliced
    object_type = None
    # 0 for image
    # 1 for button
    # 2 for text
    # 3 for text input    

    def __init__(self, image, image_type, object_type, sorting_layer, rects=None, rect=None):
        self.curently_draged = False
        self.sorting_layer = 0
        self.image_type = 0
        self.object_type = 0

        self.events = {
            Event_Types.on_click: [], "on_click_params": [],
            Event_Types.on_begin_drag: [], "on_begin_drag_params": [],
            Event_Types.on_end_drag: [], "on_end_drag_params": [],
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
            return 1

        self.image = image
        self.image_type = image_type
        self.object_type = object_type
        self.sorting_layer = sorting_layer

    def Hovering_Over(self, mouse_x, mouse_y):
        if self.rect.x <= mouse_x and self.rect.x + self.rect.w >= mouse_x and self.rect.y <= mouse_y and self.rect.y + self.rect.h >= mouse_y:
            return True
        return False

    def update(self, input_sys):
        if self.curently_draged == 1:
            self.Execute_Events(Event_Types.on_begin_drag, input_sys)
            self.curently_draged = 2
        if self.curently_draged > 0:
            self.Update_Position(input_sys.mouse_x - int(self.rect.w / 2), input_sys.mouse_y - int(self.rect.h / 2))
            if input_sys.garden.action() == 1:
                self.Stop_Draging(input_sys)

        if input_sys.garden.action() == 2:
            if self.object_type == 1:
                if self.Hovering_Over(input_sys.mouse_x, input_sys.mouse_y):
                    self.Execute_Events(Event_Types.on_click, input_sys)

    def Start_Draging(self):
        self.curently_draged = 1

    def Stop_Draging(self, input_sys):
        self.curently_draged = 0
        self.Execute_Events(Event_Types.on_end_drag, input_sys)

    def Add_Event(self, ev_type, ev, param):
        self.events[ev_type].append(ev)
        self.events[ev_type.name + "_params"].append(param)
    
    def Execute_Events(self, event, input_sys):
        for i in range(len(self.events[event])):
            if self.events[event.name + "_params"][i] == None:
                self.events[event][i]()
            else:
                self.events[event][i](self.events[event.name + "_params"][i])

    def Update_Position(self, x, y, change_pos=False):
        if change_pos:
            if not self.rects is None:
                for rect in self.rects:
                    self.rect.x += x
                    self.rect.y += y
            if not self.rect is None:
                self.rect.x += x
                self.rect.y += y
        else:
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

class UI_Screen():
    ui_objects = None

    def __init__(self):
        self.ui_objects = []
    
    def Add_Object(self, obj_to_add):
        self.ui_objects.append(obj_to_add)
        self.ui_objects = sorted(self.ui_objects, key=lambda obj: obj.sorting_layer)

    def update(self, input_sys):
        for ui_obj in self.ui_objects:
            ui_obj.update(input_sys)

class Main_Menu_Screen(UI_Screen):
    level = None
    start_game_function = None

    def __init__(self, screen_width, screen_height, start_game_function):
        super().__init__()
    
        self.level = 1
        self.start_game_function = start_game_function
        
        img = Get_Sprite("start_btn")
        rect = pygame.Rect(int(screen_width / 2) - 30, int(screen_height / 2) - 10, 60, 20)
        obj = UI_Object(img, 0, 1, 1, rect = rect)
        obj.Add_Event(Event_Types.on_click, self.StartGame, None)
        self.Add_Object(obj)

    def StartGame(self):
        start_game_function_parameters = []
        start_game_function_parameters.append(self.level)
        self.start_game_function(start_game_function_parameters)

class Game_Screen(UI_Screen):
    seed_list = None
    seed_obj_list = None
    selected_seed_id = None
    slots = None
    game_data_seeds = None
    ui_logic_controler = None
    uprooting = None
    fonts = None

    text_pannel = None
    text_pannel_text_objs = None
    game_data = None
    score_obj = None

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
        self.fonts["default"] = pygame.font.SysFont(None, 24)
        self.fonts["seed_count"] = pygame.font.SysFont(None, 40)
        self.fonts["info"] = pygame.font.SysFont(None, 30)
        self.fonts["score"] = pygame.font.SysFont(None, 40)

        #slice_values
        l, t, r, b = 26, 26, 26, 26
        #btm_pnl_sliced_images, center_width, center_height
        img, c_w, c_h = nine_slice(Get_Sprite("bottom"), l, t, r, b)
        #btm_pnl_target_rect_on_viewport
        rect = pygame.Rect(0, screen_height - 64, screen_width, 64)
        #btm_pnl_sliced_rect
        sliced_rect = Nine_Slice_Rect(rect, l, t, r, b, c_w, c_h)
        
        bottom_panel_object = UI_Object(img, 1, 0, 0, rects = sliced_rect)
        self.Add_Object(bottom_panel_object)

        img = Get_Sprite("arrowLeft")
        rect = pygame.Rect(8, screen_height - 50, 18, 36)
        obj = UI_Object(img, 0, 1, 2, rect = rect)
        self.Add_Object(obj)
        obj.Add_Event(Event_Types.on_click, self.Shift_Seeds_Left, None)
        
        img = Get_Sprite("arrowRight")
        rect = pygame.Rect(screen_width - 8 - 18, screen_height - 50, 18, 36)
        obj = UI_Object(img, 0, 1, 2, rect = rect)
        self.Add_Object(obj)
        obj.Add_Event(Event_Types.on_click, self.Shift_Seeds_Right, None)

        img = Get_Sprite("top")
        rect = pygame.Rect(screen_width - 48, 0, 48, 128)
        self.text_pannel = UI_Object(img, 0, 0, 0, rect = rect)
        self.Add_Object(self.text_pannel)

        self.score_obj = self.Create_Text_Object("score", "score: 0", self.text_pannel.rect.x + 4, self.text_pannel.rect.y + 73)
        self.score_obj.score = 0

        img = Get_Sprite("hourglass")
        child_rect = pygame.Rect(rect.x + 6, rect.y + rect.h - 4 - 16, 16, 16)
        obj = UI_Object(img, 0, 1, 1, rect = child_rect)
        self.Add_Object(obj)
        obj.Add_Event(Event_Types.on_click, game_data.End_Turn, None)

        img = Get_Sprite("shovel")
        child_rect = pygame.Rect(rect.x + 6 + 16 + 4, rect.y + rect.h - 4 - 16, 16, 16)
        obj = UI_Object(img, 0, 1, 1, rect = child_rect)
        self.Add_Object(obj)
        obj.Add_Event(Event_Types.on_click, self.Start_uprooting, None)

        img = Get_Sprite("pause")
        child_rect = pygame.Rect(rect.x + 6, rect.y + rect.h - 5 - 32 -2, 16, 16)
        obj = UI_Object(img, 0, 1, 1, rect = child_rect)
        self.Add_Object(obj)
        #obj.Add_Event(Event_Types.on_click, game_data.End_Turn, None)#TODO

        img = Get_Sprite("undo")
        child_rect = pygame.Rect(rect.x + 6 + 16 + 4, rect.y + rect.h - 5 - 32 - 2, 16, 16)
        obj = UI_Object(img, 0, 1, 1, rect = child_rect)
        self.Add_Object(obj)
        obj.Add_Event(Event_Types.on_click, self.ui_logic_controler.Call_Undo, None)

        for i in range(4):
            img = Get_Sprite("slot")
            rect = pygame.Rect(29 + (i * 42), screen_height - 52, 40, 40)
            obj = UI_Object(img, 0, 0, 2, rect = rect)
            self.Add_Object(obj)
            self.slots.append(obj)

        self.Update_Seed_List()

    def update(self, input_sys):
        if self.uprooting:
            if input_sys.garden.action() == 2:
                self.End_uprooting()

        super().update(input_sys)

        #displaying info about the plant under cursor
        plant_map = self.ui_logic_controler.scene.plants 
        x, y = self.ui_logic_controler.surface.ScreenToWorldPos(input_sys.mouse_x, input_sys.mouse_y)
        x, y = plant_map.Get_Map_Pos_From_World_pos(x, y)
        plant = self.game_data.Get_Plant(x, y)
        self.Display_Plant_Info(plant)

        #displaying the correct score
        if not self.score_obj.score == self.game_data.score:
            self.score_obj.score = self.game_data.score
            score_txt = "score: " + str(self.score_obj.score)
            sz = self.fonts["score"].size(score_txt)
            self.score_obj.rect.w = sz[0]
            self.score_obj.rect.h = sz[1]
            
            self.score_obj.image = self.fonts["score"].render(score_txt, False, (255,255,255))

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
        info = "test"    
        for i in range(5):
            if i == 0:
                info = plant.plant_type.name
            if i == 1:
                info = str(plant.age)
            if i == 2:
                info = str(plant.age)
            if i == 3:
                info = str(plant.age)
            if i == 4:
                info = str(plant.age)
            obj = self.Create_Text_Object("info", info, self.text_pannel.rect.x + 6, self.text_pannel.rect.y + 5 + (12 * i))
            self.text_pannel_text_objs.append(obj)


    def Create_Text_Object(self, font_name, text, position_x = 0, position_y = 0, color = (255, 255, 255), layer = 5):
        if not font_name in self.fonts.keys():
            return

        sz = self.fonts[font_name].size(text)
        rect = pygame.Rect(position_x, position_y, sz[0], sz[1])
                                                #antialiass
        img = self.fonts[font_name].render(text, False, color)
        obj = UI_Object(img, 0, 2, layer, rect = rect)
        self.Add_Object(obj)
        return obj

    def Start_uprooting(self):
        self.uprooting = True

    def End_uprooting(self):
        self.uprooting = False
        self.ui_logic_controler.Call_Up_Root(["MOUSE_X", "MOUSE_Y"])

    def Shift_Seeds_Left(self):
        if not self.selected_seed_id == 0:
            self.selected_seed_id -= 1
            self.Update_Seed_List(True)

    def Shift_Seeds_Right(self):
        if self.selected_seed_id + 1 < len(self.game_data_seeds):
            self.selected_seed_id += 1
            self.Update_Seed_List(True)

    def Update_Seed_List(self, force_update = False):
        ls = []
        for key in self.game_data_seeds.keys():
            ls.append((key.value, self.game_data_seeds[key]))
        ls = sorted(ls)

        if ls == self.seed_list and not force_update:
            return

        self.seed_list = ls
        for seed in self.seed_obj_list:
            self.ui_objects.remove(seed)
        self.seed_obj_list.clear()

        if len(self.seed_list) > self.selected_seed_id:
            for i in range(self.selected_seed_id, self.selected_seed_id + 4):
                if i + 1 <= len(self.seed_list):#this entry exists
                    inner_rect = pygame.Rect(self.slots[i - self.selected_seed_id].rect.x + 4, self.slots[i - self.selected_seed_id].rect.y + 4, 32, 32)
                    seed_obj = UI_Object(Get_Seed_Sprite(Plant_Type(self.seed_list[i][0])), 0, 1, 3, rect = inner_rect)
                    
                    seed_obj.Add_Event(Event_Types.on_click, seed_obj.Start_Draging, None)
                    seed_obj.Add_Event(Event_Types.on_end_drag, self.ui_logic_controler.Call_Plant, ["MOUSE_X", "MOUSE_Y", Plant_Type(self.seed_list[i][0])])
                    seed_obj.Add_Event(Event_Types.on_end_drag, self.Update_Seed_List, True)
                    
                    self.seed_obj_list.append(seed_obj)
                    self.seed_obj_list.append(self.Create_Text_Object("seed_count", str(self.seed_list[i][1]), inner_rect.x + 20, inner_rect.y + 20))
                    self.Add_Object(seed_obj)

class Game_Scene():
    background = None
    plants = None

    def __init__(self, game_data):
        self.background = Tilemap(game_data.field_size_x, game_data.field_size_y)
        self.plants = Tilemap(game_data.field_size_x, game_data.field_size_y)

class Tilemap():
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

        for i in range(self.map_height):  # Corrected range
            self.tiles.append([])
            for j in range(self.map_width):  # Corrected range
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
        #print(self.p_type)
        self.age = age
