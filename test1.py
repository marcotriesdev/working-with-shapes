from pyray import *

init_window(800, 450, "Hello Pyray")
set_target_fps(60)

camera = Camera3D([18.0, 16.0, 18.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], 45.0, 0)

while not window_should_close():
    update_camera(camera, 1)
    begin_drawing()
    clear_background(RAYWHITE)
    begin_mode_3d(camera)
    draw_grid(20, 1.0)
    end_mode_3d()
    draw_text("Hello world", 190, 200, 20, VIOLET)
    end_drawing()

close_window()