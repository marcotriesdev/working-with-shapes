from raylibpy import *
from classes import *

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 1024
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
















def sacar():
        
    circle1 = Circle(Vector2(500,500),10,PINK,"fill",10,5)
    gamegui = Gui(WINDOW_WIDTH,WINDOW_HEIGHT, game_title,circle1)

    circle2 = Circle(Vector2(400,400),15,GREEN,"outline",1)
    circle3 = Circle(Vector2(460,400),15,GREEN,"outline",1)
    circle4 = Circle(Vector2(520,400),15,GREEN,"outline",1)

    enemy1 = Circle(Vector2(800,800),20,BLACK,"enemy",10,4,2)

    player_group = Group([circle1])
    circle_group = Group([circle2,circle3,circle4])
    circle_group.set_group_thickness(10)

    enemy_group = Group([enemy1])


    while not window_should_close():

        begin_drawing()

        clear_background(WHITE)

        player_group.update(dimensions)
        enemy_group.update(dimensions)
        circle_group.update(dimensions)

        circle1.collision(circle_group)
        circle1.collision(enemy_group)

        player_group.draw()
        circle_group.draw()
        enemy_group.draw()
        gamegui.draw_hud()

        end_drawing()
        
    close_window()



