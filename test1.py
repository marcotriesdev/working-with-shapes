import raylibpy as rl

# Initialize the raylib window
rl.init_window(800, 600, "Font Example")

# Specify font size
font_size = 32

# Attempt to load the font using load_font_ex with None as codepoints and 0 as count
try:
    font = rl.load_font_ex("path/to/font.ttf", font_size, None, 0)
except TypeError as e:
    print("Error loading font:", e)
    rl.close_window()
    raise SystemExit("Failed to load font.")

# Game loop to render the font
while not rl.window_should_close():
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)

    rl.draw_text_ex(font, "Hello, Raylib!", (100, 100), font_size, 1, rl.BLACK)

    rl.end_drawing()

# Clean up
rl.unload_font(font)
rl.close_window()