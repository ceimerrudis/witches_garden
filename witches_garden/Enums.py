from enum import Enum

class Plant_Type(Enum):
	plot = 1
	grass1 = 2
	grass2 = 3
	grass3 = 4
	grass4 = 5
	drelay = 6
	brelay = 7
	hrelay = 8
	fireplant = 9
	iceplant = 10
	seedplant = 11
	lightplant = 12
	darknessplant = 13

class Event_Types(Enum):
	on_click = 1
	on_begin_drag = 2
	on_end_drag = 3
