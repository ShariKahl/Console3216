from math import pi, cos, sin

# TODO C++ includes:
# Adafruit_GFX.h
# gfxfront.h
# RGBMatrixPanel.h

import os
# TODO Unbenutzter Import
# import Microcontroller
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

from Sprite import *

DISPLAY_X_EXTEND = 32
DISPLAY_Y_EXTEND = 16

# Matrix Options
DISPLAY_X = 32
DISPLAY_Y = 16
DISPLAY_SCALE_FACTOR = 64
DISPLAY_CHAIN = 1
HARDWARE_MAPPING = "adafruit-hat"

# TODO C++ Defines
#define CLK 11  
#define LAT A3
#define OE  9
#define A   A0
#define B   A1
#define C   A2

# TODO Schriftarten
# In der C++ Implementierung konnte ein Skalierungsfaktor angegeben werden,
# das simulieren wir indem wir einfach mehrere Schriftarten verwenden
# TODO Liste nicht fertig
FONT_LIST = ["4x6.bdf", "6x9.bdf"]

# Farbumrechnungstabelle von 3-Bit auf 8-Bt
# Berechnung: acht_bit = (drei_bit << 5) | (drei_bit << 2) | (drei_bit >> 1)
COLORTABLE = [0, 36, 73, 109, 146, 182, 219, 255]

class Display:
    matrix: RGBMatrix = None
    fonts: list = list()

    # def __rescale_to_local(self, coordinate: int):
    #     return coordinate / DISPLAY_SCALE_FACTOR

    # TODO Konstruktor in C++ vorhanden
    def __init__(self):
        # TODO Aus C++ übernommen, wird aber anscheinend nirgendwo verwendet
        self.__prevBallX: int = 0
        self.__prevBallY: int = 0
        self.__prevP1: int = 0
        self.__prevP2: int = 0

    @classmethod
    def init(cls):
        # TODO Alter Matrix Init Code
        # pinMode(PIN_DISPLAY_CLK, OUTPUT); // CLK input ?
        # pinMode(PIN_DISPLAY_OE, OUTPUT); // OE  input ?
        # pinMode(PIN_DISPLAY_B2, OUTPUT);
        # pinMode(PIN_DISPLAY_G2, OUTPUT);
        # pinMode(PIN_DISPLAY_R2, OUTPUT);
        # pinMode(PIN_DISPLAY_B1, OUTPUT);
        # pinMode(PIN_DISPLAY_G1, OUTPUT);
        # pinMode(PIN_DISPLAY_R1, OUTPUT);
        # pinMode(PIN_DISPLAY_LAT, OUTPUT);
        # pinMode(PIN_DISPLAY_C, OUTPUT);
        # pinMode(PIN_DISPLAY_B, OUTPUT);
        # pinMode(PIN_DISPLAY_A, OUTPUT);
        
        # Wurde in C++ mit "new" angelegt, weil matrix ein Pointer ist
        # Display.matrix = RGBMatrixPanel(A, B, C, CLK, LAT, OE, True)
        # Display.matrix.begin()
        # Display.matrix.fillScreen(self.matrix.Color333(0, 0, 7)) # BLUE
        # Display.matrix.fillScreen(self.matrix.Color333(0, 0, 0)) # CLEAR

        # Neuer Matrix Init Code
        matrix_options = RGBMatrixOptions()
        matrix_options.rows = DISPLAY_X
        matrix_options.cols = DISPLAY_Y
        matrix_options.chain_length = DISPLAY_CHAIN
        matrix_options.hardware_mapping = HARDWARE_MAPPING

        # Schriftarten laden
        cls.import_fonts()

        cls.matrix = RGBMatrix(options=matrix_options)
        cls.matrix.Clear()

    @classmethod
    def import_fonts(cls):
        """_summary_
        Importiert die Schriftarten für die Textausgabe
        """
        font_path = os.path.join(os.path.curdir, "fonts")

        # TODO 2 mögliche Methoden zum importieren von Schriftarten

        method: int = 2

        if method == 1:
            # Methode 1:
            # Schriftarten werden manuell in ein Array eingetragen
            # Vorteil: Reihenfolge kann direkt festgelegt werden
            # Nachteil: Hardcoded und muss im Code angepasst werden,
            # wenn nötig.
            for font in FONT_LIST:
                cls.fonts.append(graphics.Font())
                cls.fonts[-1].LoadFont(os.path.join(font_path, font))
        elif method == 2:
            # Methode 2:
            # Alle Schriftarten, die sich im Ordner befinden, werden geladen
            # Vorteil: Code muss nicht angepasst werden, wenn die Schriftarten
            # sich ändern.
            # Nachteil: Reihenfolge muss im Dateinamen festgemacht werden,
            # Tests nötig, ob die Dateien in der gewünschten Reihenfolge
            # behandelt werden
            for filename in os.listdir(font_path):
                if filename.endswith(".bdf"):
                    file_path = os.path.join(os.path.curdir, filename)
                    cls.fonts.append(graphics.Font())
                    cls.fonts[-1].LoadFont(file_path)

    @classmethod
    def refresh(cls):
        cls.matrix.SwapOnVSync()

    @classmethod
    def drawPixel(cls, x: int, y: int, color: graphics.Color):
        if ((x < DISPLAY_X_EXTEND) and (y < DISPLAY_Y_EXTEND)):
            # TODO color
            cls.matrix.SetPixel(x, y, color.r, color.g, color.b)

    # TODO Auskommentierte Zeile
    # C++: static void drawRect(int16_t x, int16_t y,
    #                           int16_t w, int16_t h, uint16_t color);
    # @classmethod
    # def drawRect(self, x: int, y: int, w: int, h: int, color: int)

    @classmethod
    def clearDisplay(cls):
        cls.matrix.Clear()

    # TODO Rewrite for new Color method
    #@classmethod
    #def drawText(cls, text: str, x: int, y: int, r, g, b, scaleFactor: int):
    @classmethod
    def drawText(cls, text: str, x: int, y: int, color: graphics.Color, scaleFactor: int):
        # cls.matrix.setCursor(x, y)
        # cls.matrix.setTextColor(color)
        # cls.matrix.setTextSize(scaleFactor)
        # cls.matrix.print(text)
        # color = graphics.Color(r, g, b)
        # TODO Skalierungsfaktor mit mehreren Schriftarten simulieren
        # TODO Erster Parameter gibt Canvas an
        # Eventuell muss neuer Hintergrund Canvas erzeugt werden
        graphics.DrawText(cls.matrix,
                          cls.fonts[scaleFactor],
                          x, y,
                          color,
                          text)

    # @classmethod
    # def getColor(self, red: int, green: int, blue: int) -> int:
    #    return Display.matrix.Color333(red, green, blue)

    # Nimmt 3-Bit Werte an und gibt 8-Bit Werte zurück
    @classmethod
    def getColorFrom333(cls, red: int, green: int, blue: int) -> graphics.Color:
        return graphics.Color(COLORTABLE[red], COLORTABLE[green], [COLORTABLE[blue]])
    
    # RGB565 zu RGB888 Umrechner
    @classmethod
    def getColorFrom565(cls, value: int) -> graphics.Color:
        red = value >> 13
        green = value >> 8 & 7
        blue = value >> 2 & 7
        return graphics.Color(COLORTABLE[red], COLORTABLE[green], [COLORTABLE[blue]])
    
    # RGB888
    @classmethod
    def getColor888(cls, red: int, green: int, blue: int) -> graphics.Color:
        return graphics.Color(red, green, blue)

    @classmethod
    def getColor(cls, red: int, green: int = -1, blue: int = -1, rgb888: bool = False) -> graphics.Color:
        # Fall: 565
        if green == -1 and blue == -1:
            return cls.getColorFrom565(red)
        # Fall: 888
        elif rgb888:
            return cls.getColor888(red, green, blue)
        # Fall: 333
        else:
            return cls.getColorFrom333(red, green, blue)

    # TODO Kein Python Äquivalent, dafür können jetzt Bilddateien angezeigt werden
    # Wird aber eventuell nicht benötigt
    # @classmethod
    # def drawBitmap(cls, x: int, y: int, bitmap: int, width: int, height: int, color: int):
    #     self.matrix.drawBitmap(self.__rescaleToLocal(x), self.__rescaleToLocal(y), bitmap, width, height, color)
    
    # TODO Temporary replacement functions, needs testing if native functions are available
    @classmethod
    def drawLine(cls, x1: int, y1: int, x2: int, y2: int, color: graphics.Color):
        graphics.DrawLine(cls.matrix, x1, y1, x2, y2, color)
        pass
    
    @classmethod
    def drawRect(cls, x: int, y: int, w: int, h: int, color: graphics.Color):
        # Horizontal
        for i in range(w):
            cls.matrix.SetPixel(x + i, y, color.r, color.g, color.b)
            cls.matrix.SetPixel(x + i, y + h - 1, color.r, color.g, color.b)
        # Vertical
        for y in range(1, h - 1):
            cls.matrix.SetPixel(x, y + i, color.r, color.g, color.b)
            cls.matrix.SetPixel(x + w - 1, y + i, color.r, color.g, color.b)
        pass
    
    @classmethod
    def drawRectAlt(cls, x: int, y: int, w: int, h: int, color: graphics.Color):
        # Horizontal
        cls.drawLine(x, y, x + w - 1, y)
        cls.drawLine(x, y + h - 1, x + w - 1, y + h - 1)
        # Vertical
        cls.drawLine(x, y + 1, x, y + h - 2)
        cls.drawLine(x + w - 1, y + 1, x + w - 1, y + h - 2)
        pass
    
    @classmethod
    def fillRectAlt(cls, x: int, y: int, w: int, h: int, color: graphics.Color):
        for i in range(w):
            cls.drawLine(x + i, y, x + i, y + h - 1)
        pass
    
    @classmethod
    def fillRect(cls, x: int, y: int, w: int, h: int, color: graphics.Color):
        for i in range(h):
            for j in range(w):
                cls.matrix.SetPixel(x + j, y + i, color.r, color.g, color.b)
        pass
    
    """
    Zeichnet den Umriss eines Kreises in die Matrix.
    
    Die Methode benötigt 4 Pflichtparameter:
    * x     =   X-Coordinate des Mittelpunkts
    * y     =   Y-Coordinate des Mittelpunkts
    * r     =   Radius
    * color =   Farbe
    
    Und es kann ein optionaler Parameter verwendet werden:
    * dots  =   Aus wie vielen Punkten der Kreis bestehen soll. Je kleiner der Kreis, desto kleiner die Anzahl der möglichen Punkte.
                So kann man ein klein wenig optimieren, wie viele Berechnungen pro Kreis durchgeführt werden.
                    
                Wird kein Wert angegeben, wird die minimale Anzahl der äußeren Punkte berechnet, um einen geschlossenen Kreis zu erzeugen.
                -> Default = -1
    """
    @classmethod
    def drawCircle(cls, x: int, y: int, r: int, color: graphics.Color, dots: int = -1):
        if dots == -1:
            dots = (3 * r - 1) // 2 * 4
        hc = pi / (dots / 2)
        for i in range(0, dots):
            x2 = round(r * sin(i * hc))
            y2 = round(r * cos(i * hc))
            cls.matrix.SetPixel(x + x2, y + y2, color.r, color.g, color.b)
        pass

    """
    Zeichnet einen ausgefüllten Kreis in die Matrix.
    
    Es wird zunächst ein Umriss mit der drawCircle Funktion gezeichnet, der optionale Parameter dots ist ausschließlich für diesen Schritt gedacht,
    die Berechnung des Kreisinneren wird unabhängig von diesem Wert durchgeführt.
    """
    @classmethod
    def fillCircle(cls, x: int, y: int, r: int, color: graphics.Color, dots: int = -1):
        cls.drawCircle(x, y, r, dots)
        for i in range(y - r, y + r + 1):
            for j in range(x - r, x + r + 1):
                if pow(i - y, 2) + pow(j - x, 2) <= pow(r, 2):
                    cls.matrix.SetPixel(j, i, color.r, color.g, color.b)
        pass
    
    """
    Alternative Methode, einen Kreis zu zeichnen. Kann nur den Umriss zeichnen oder den Kreis ausfüllen.
    Zeichnet einen Umriss für r, danach den Umriss für r-1 usw. bis r = 0 ist.
    
    Bis auf die While Schleife und die Manipulation von r gibt es keinen Unterschied zu den Berechnungen der drawCircle Methode.
    
    Optionaler Parameter:
    * filled    =   Ob der Kreis ausgefüllt werden soll.
    """
    @classmethod
    def drawCircleAlt(cls, x: int, y: int, r: int, color: graphics.Color, dots: int = -1, filled: bool = False):
        if dots == -1:
            dots = (3 * r - 1) // 2 * 4
        hc = pi / (dots / 2)
        
        while r > 0:
            for i in range(0, dots):
                x2 = round(r * sin(i * hc))
                y2 = round(r * cos(i * hc))
                cls.matrix.SetPixel(x + x2, y + y2, color.r, color.g, color.b)
            if filled:
                r -= 1
            else:
                r = 0
        if filled:
            cls.matrix.SetPixel(x, y, color.r, color.g, color.b)
        pass
