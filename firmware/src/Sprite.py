
from Display import *


# TODO Die Farben werden jetzt mit 3 ints (RGB) angegeben
# Die Liste _bitmap ist in C++ ein Array aus ints, die
# auf jeder Position einen Farbcode beinhalten.
# In Dieser Implementierung wird ein neues Color Objekt
# an jeder Position angelegt
class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


class Sprite:
    def __init__(self, xPos: int, yPos: int, xExtend: int, yExtend: int) -> None:
        self._xPos: int = xPos
        self._yPos: int = yPos
        self._xExtend: int = xExtend
        self._yExtend: int = yExtend
        # C++ Quellcode:
        # this->bitmap = new uint16_t [yExtend * xExtend];
        # TODO Convert to new Color method
        self._bitmap = [Color for _ in range(xExtend * yExtend)]
        self._direction: int = 0
        self._active: bool = False

    def setPosition(self, newXPos: int, newYPos: int):
        self._xPos = newXPos
        self._yPos = newYPos
        pass

    def move(self, xDelta: int, yDelta: int):
        self._xPos += xDelta
        self._yPos += yDelta
        pass

    def getXPos(self) -> int:
        return self._xPos

    def getYPos(self) -> int:
        return self._yPos

    def isActive(self) -> bool:
        return self._active

    def activate(self):
        self._active = True
        pass

    def deActivate(self):
        self._active = False
        pass

    # TODO Farbe wird nicht mehr mit nur einem int angegeben
    def draw(self):
        if self._active:
            counter = 0

            for x in range(self._xPos, self._xExtend + self._xPos):
                for y in range(self._yPos, self._yExtend + self._yPos):
                    Display.drawPixel(x, y, self._bitmap[counter])
                    counter += 1
        pass

    def mirrorY(self):
        for y in range(0, int(self._xExtend / 2)):
            for x in range(0, self._yExtend):
                leftPixel = self._bitmap[y * self._yExtend + x]
                rightPixel = self._bitmap[(self._xExtend - 1) * self._yExtend + x]

                self._bitmap[y * self._yExtend + x] = rightPixel
                self._bitmap[(self._xExtend - 1) * self._yExtend + x] = leftPixel
        pass
