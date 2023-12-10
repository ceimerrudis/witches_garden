from enum import Enum

class Event_Types(Enum):
	on_click = 1
	on_begin_drag = 2
	on_end_drag = 3

class UI_Object_Type(Enum):
	image = 0
	button = 1
	text = 2

class Image_Type(Enum):
	basic = 0
	nine_sliced = 1