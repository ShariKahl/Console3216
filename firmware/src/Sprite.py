from Display import Display


class Color:
    """
    Repräsentiert eine RGB-Farbe.
    """
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b


class Sprite:
    def __init__(self, xPos: int, yPos: int, xExtend: int, yExtend: int):
        """
        Initialisiert das Sprite mit einer Position, einer Ausdehnung und einer Bitmap.
        :param xPos: X-Koordinate der oberen linken Ecke
        :param yPos: Y-Koordinate der oberen linken Ecke
        :param xExtend: Breite des Sprites
        :param yExtend: Höhe des Sprites
        """
        self._xPos = xPos
        self._yPos = yPos
        self._xExtend = xExtend
        self._yExtend = yExtend
        self._bitmap = [Color(0, 0, 0) for _ in range(xExtend * yExtend)]
        self._direction = 0
        self._active = False

    def setPosition(self, newXPos: int, newYPos: int):
        """
        Setzt die Position des Sprites.
        :param newXPos: Neue X-Koordinate
        :param newYPos: Neue Y-Koordinate
        """
        self._xPos = newXPos
        self._yPos = newYPos

    def move(self, xDelta: int, yDelta: int):
        """
        Bewegt das Sprite um eine relative Distanz.
        :param xDelta: Änderung der X-Koordinate
        :param yDelta: Änderung der Y-Koordinate
        """
        self._xPos += xDelta
        self._yPos += yDelta

    def getXPos(self) -> int:
        """
        Gibt die aktuelle X-Koordinate des Sprites zurück.
        """
        return self._xPos

    def getYPos(self) -> int:
        """
        Gibt die aktuelle Y-Koordinate des Sprites zurück.
        """
        return self._yPos

    def isActive(self) -> bool:
        """
        Gibt zurück, ob das Sprite aktiv ist.
        """
        return self._active

    def activate(self):
        """
        Aktiviert das Sprite.
        """
        self._active = True

    def deActivate(self):
        """
        Deaktiviert das Sprite.
        """
        self._active = False

    def draw(self):
        """
        Zeichnet das Sprite auf das Display.
        """
        if not self._active:
            return

        counter = 0
        for x in range(self._xExtend):
            for y in range(self._yExtend):
                color = self._bitmap[counter]
                Display.drawPixel(self._xPos + x, self._yPos + y, color)
                counter += 1
        print(f"Sprite drawn at ({self._xPos}, {self._yPos}) with size ({self._xExtend}, {self._yExtend})")

    def mirrorY(self):
        """
        Spiegelt das Sprite entlang der Y-Achse.
        """
        for y in range(self._yExtend):
            for x in range(self._xExtend // 2):
                leftIdx = y * self._xExtend + x
                rightIdx = y * self._xExtend + (self._xExtend - 1 - x)

                # Pixel austauschen
                self._bitmap[leftIdx], self._bitmap[rightIdx] = self._bitmap[rightIdx], self._bitmap[leftIdx]
        print("Sprite mirrored along Y-axis.")
