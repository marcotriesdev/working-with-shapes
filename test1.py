import raylibpy as rl

# Configuración de la ventana
rl.init_window(800, 600, "Texto sin pixelado en raylibpy")
rl.set_target_fps(60)

# Ruta y tamaño de la fuente
font_size = 150

# Cargar la fuente
font = rl.load_font("path/to/font.ttf")  # Usa load_font para cargar la fuente

# Creación de una textura de renderizado para el texto
text_texture = rl.load_render_texture(500, 200)

# Dibujamos el texto en la textura
rl.begin_texture_mode(text_texture)
rl.clear_background(rl.BLANK)
rl.draw_text_ex(font, "Texto grande", (0, 0), font_size, 1, rl.RAYWHITE)
rl.end_texture_mode()

# Bucle de la ventana principal
while not rl.window_should_close():
    rl.begin_drawing()
    rl.clear_background(rl.DARKGRAY)
    
    # Renderizado de la textura del texto
    rl.draw_texture_pro(
        text_texture.texture,
        rl.Rectangle(0, 0, text_texture.texture.width, -text_texture.texture.height),
        rl.Rectangle(150, 200, text_texture.texture.width, text_texture.texture.height),
        rl.Vector2(0, 0), 
        0.0, 
        rl.RAYWHITE
    )
    
    rl.end_drawing()

# Limpieza de recursos
rl.unload_font(font)
rl.unload_render_texture(text_texture)
rl.close_window()
