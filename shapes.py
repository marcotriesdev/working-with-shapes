from raylibpy import *
from classes import *

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 900
game_title = "EL COMEPUNTOS VOLADOR"
dimensions = Vector2(WINDOW_WIDTH,WINDOW_HEIGHT)

init_window(WINDOW_WIDTH,WINDOW_HEIGHT,"Raylib - Shapes")

set_trace_log_level(LOG_NONE)

set_target_fps(60)

#--------------------------------------------------------

estado_global = Estado_global.intro

state_machine = SimpleStateMachine(estado_global,dimensions.x,
                                   dimensions.y,game_title)

#--------------------------------------------------------

state_machine.update()
