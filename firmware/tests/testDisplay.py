from Display import Display

# Initialisieren
Display.init()

# Farben erstellen
red = Display.get_color(255, 0, 0)
green = Display.get_color(0, 255, 0)
blue = Display.get_color(0, 0, 255)

# Pixel und Formen zeichnen
Display.draw_pixel(10, 10, red)
Display.fill_rect(15, 15, 10, 10, green)
Display.draw_circle(32, 32, 10, blue)

# Text anzeigen
Display.draw_text("Hello, Pi!", 5, 20, red, font_index=0)

# Refresh (optional, falls nötig)
Display.refresh()

# pip install rgbmatrix