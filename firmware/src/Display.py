from math import pi, cos, sin
import os
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# Matrix-Konfiguration
DISPLAY_ROWS = 64
DISPLAY_COLS = 64
DISPLAY_CHAIN = 1
HARDWARE_MAPPING = "adafruit-hat"

FONT_DIR = "fonts"  # Verzeichnis mit BDF-Schriftarten
COLORTABLE = [0, 36, 73, 109, 146, 182, 219, 255]  # 3-Bit auf 8-Bit Farbwerte

class Display:
    matrix = None
    fonts = []

    @classmethod
    def init(cls):
        """Initialisiert die LED-Matrix."""
        options = RGBMatrixOptions()
        options.rows = DISPLAY_ROWS
        options.cols = DISPLAY_COLS
        options.chain_length = DISPLAY_CHAIN
        options.hardware_mapping = HARDWARE_MAPPING
        cls.matrix = RGBMatrix(options=options)
        cls.matrix.Clear()
        cls.import_fonts()

    @classmethod
    def import_fonts(cls):
        """Lädt Schriftarten aus dem FONT_DIR-Verzeichnis."""
        font_path = os.path.join(os.curdir, FONT_DIR)
        if not os.path.exists(font_path):
            print(f"Font directory '{FONT_DIR}' not found.")
            return
        for filename in os.listdir(font_path):
            if filename.endswith(".bdf"):
                font = graphics.Font()
                font.LoadFont(os.path.join(font_path, filename))
                cls.fonts.append(font)
        if not cls.fonts:
            print("No fonts loaded. Ensure BDF files are in the fonts directory.")

    @classmethod
    def clear(cls):
        """Löscht die Matrix."""
        cls.matrix.Clear()

    @classmethod
    def draw_pixel(cls, x, y, color):
        """Zeichnet ein einzelnes Pixel."""
        cls.matrix.SetPixel(x, y, color.red, color.green, color.blue)

    @classmethod
    def draw_text(cls, text, x, y, color, font_index=0):
        """Zeichnet einen Text."""
        if font_index < len(cls.fonts):
            graphics.DrawText(cls.matrix, cls.fonts[font_index], x, y, color, text)
        else:
            print(f"Font index {font_index} out of range. Loaded fonts: {len(cls.fonts)}")

    @classmethod
    def draw_circle(cls, x, y, r, color):
        """Zeichnet einen Kreis."""
        for angle in range(0, 360, 5):  # Punkte in 5-Grad-Schritten
            x2 = int(x + r * cos(angle * pi / 180))
            y2 = int(y + r * sin(angle * pi / 180))
            cls.draw_pixel(x2, y2, color)

    @classmethod
    def fill_rect(cls, x, y, w, h, color):
        """Füllt ein Rechteck."""
        for i in range(w):
            for j in range(h):
                cls.draw_pixel(x + i, y + j, color)

    @classmethod
    def get_color(cls, red, green, blue):
        """Erstellt eine Farbe."""
        return graphics.Color(red, green, blue)

    @classmethod
    def refresh(cls):
        """Aktualisiert die Matrix."""
        cls.matrix.SwapOnVSync()
