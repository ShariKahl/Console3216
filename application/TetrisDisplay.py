import Display

class TetrisDisplay:
    def __init__(self):
        # Initialisierung der Spielfeldanzeige
        self.__map = [[0 for _ in range(32)] for _ in range(16)]  # 16 Zeilen, 32 Spalten (für das Display)

    def clear(self):
        # Löscht die Anzeige
        Display.Display.clearDisplay()
        Display.Display.refresh()

    def update(self):
        # Aktualisiert das Spielfeld auf dem Display
        for x in range(32):  # 32 Spalten
            for y in range(16):  # 16 Zeilen
                if self.__map[y][x] == 1:
                    # Zeichnet ein Pixel, wenn es Teil des Spielfeldes ist
                    Display.Display.drawPixel(x, y, Display.Display.getColorFrom333(2, 0, 0))  # Farbe wählen
        Display.Display.refresh()

    def draw_block(self, x, y):
        # Zeichnet einen Block auf dem Spielfeld an der Position (x, y)
        if 0 <= x < 32 and 0 <= y < 16:
            self.__map[y][x] = 1  # Setzt das entsprechende Feld auf 1, um es zu aktivieren
            Display.Display.drawPixel(x, y, Display.Display.getColorFrom333(2, 0, 0))  # Farbe des Blocks
            Display.Display.refresh()

    def erase_block(self, x, y):
        # Löscht einen Block an der Position (x, y)
        if 0 <= x < 32 and 0 <= y < 16:
            self.__map[y][x] = 0  # Setzt das entsprechende Feld auf 0, um es zu deaktivieren
            Display.Display.drawPixel(x, y, Display.Display.getColorFrom333(0, 0, 0))  # Farbe der Hintergrund
            Display.Display.refresh()

    def reset(self):
        # Setzt das Spielfeld zurück
        self.__map = [[0 for _ in range(32)] for _ in range(16)]  # Spielfeld zurücksetzen
        self.clear()  # Bildschirm löschen
        self.update()  # Bildschirm mit leerem Spielfeld anzeigen
