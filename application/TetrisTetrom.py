# #include "Arduino.h"
# #include "game.h"
import Game

import Display

# TODO C++: static const uint8_t tetromRotations[7][4][4][4] = {...}
tetromRotations = [
    # J 0
    [[[0, 1, 0, 0],
      [0, 1, 0, 0],
      [1, 1, 0, 0],
      [0, 0, 0, 0]],
     [[1, 0, 0, 0],
      [1, 1, 1, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0]],
     [[0, 1, 1, 0],
      [0, 1, 0, 0],
      [0, 1, 0, 0],
      [0, 0, 0, 0]],
     [[0, 0, 0, 0],
      [1, 1, 1, 0],
      [0, 0, 1, 0],
      [0, 0, 0, 0]]],
    # L 1
    [[[0, 1, 0, 0],
      [0, 1, 0, 0],
      [0, 1, 1, 0],
      [0, 0, 0, 0]],
     [[0, 0, 0, 0],
      [1, 1, 1, 0],
      [1, 0, 0, 0],
      [0, 0, 0, 0]],
     [[1, 1, 0, 0],
      [0, 1, 0, 0],
      [0, 1, 0, 0],
      [0, 0, 0, 0]],
     [[0, 0, 1, 0],
      [1, 1, 1, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0]]],
    # O 2
    [[[1, 1, 0, 0],
      [1, 1, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0]],
     [[1, 1, 0, 0],
      [1, 1, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0]],
     [[1, 1, 0, 0],
      [1, 1, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0]],
     [[1, 1, 0, 0],
      [1, 1, 0, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0]]],
    # S 3
    [[[0, 0, 0, 0],
      [0, 1, 1, 0],
      [1, 1, 0, 0],
      [0, 0, 0, 0]],
     [[0, 1, 0, 0],
      [0, 1, 1, 0],
      [0, 0, 1, 0],
      [0, 0, 0, 0]],
     [[0, 0, 0, 0],
      [0, 1, 1, 0],
      [1, 1, 0, 0],
      [0, 0, 0, 0]],
     [[0, 1, 0, 0],
      [0, 1, 1, 0],
      [0, 0, 1, 0],
      [0, 0, 0, 0]]],
    # Z 4
    [[[0, 0, 0, 0],
      [1, 1, 0, 0],
      [0, 1, 1, 0],
      [0, 0, 0, 0]],
     [[0, 0, 1, 0],
      [0, 1, 1, 0],
      [0, 1, 0, 0],
      [0, 0, 0, 0]],
     [[0, 0, 0, 0],
      [1, 1, 0, 0],
      [0, 1, 1, 0],
      [0, 0, 0, 0]],
     [[0, 0, 1, 0],
      [0, 1, 1, 0],
      [0, 1, 0, 0],
      [0, 0, 0, 0]]],
    # T 5
    [[[0, 0, 0, 0],
      [1, 1, 1, 0],
      [0, 1, 0, 0],
      [0, 0, 0, 0]],
     [[0, 1, 0, 0],
      [1, 1, 0, 0],
      [0, 1, 0, 0],
      [0, 0, 0, 0]],
     [[0, 1, 0, 0],
      [1, 1, 1, 0],
      [0, 0, 0, 0],
      [0, 0, 0, 0]],
     [[0, 1, 0, 0],
      [0, 1, 1, 0],
      [0, 1, 0, 0],
      [0, 0, 0, 0]]],
    # I 6
    [[[0, 0, 1, 0],
      [0, 0, 1, 0],
      [0, 0, 1, 0],
      [0, 0, 1, 0]],
     [[0, 0, 0, 0],
      [0, 0, 0, 0],
      [1, 1, 1, 1],
      [0, 0, 0, 0]],
     [[0, 0, 1, 0],
      [0, 0, 1, 0],
      [0, 0, 1, 0],
      [0, 0, 1, 0]],
     [[0, 0, 0, 0],
      [0, 0, 0, 0],
      [1, 1, 1, 1],
      [0, 0, 0, 0]]]]


class TetrisTetrom:
    def __init__(self, offsetX: int, offsetY: int):
        self.__mapOffsetX: int = offsetX
        self.__mapOffsetY: int = offsetY
        self.__positionX: int = 0
        self.__positionY: int = 0
        self.__rotationIndex: int = 0
        self.__tetromIndex: int = 0
        self.__color: int = Display.Display.getColorFrom333(2, 0, 2)
        pass

    def getX(self) -> int:
        return self.__positionX

    def getY(self) -> int:
        return self.__positionY

    def moveRelative(self, x: int, y: int):
        self.__positionX += x
        self.__positionY += y
        pass

    def setPosition(self, x: int, y: int):
        self.__positionX = x
        self.__positionY = y
        pass

    def rotateLeft(self):
        self.__rotationIndex -= 1
        self.__rotationIndex %= 4
        pass

    def rotateRight(self):
        self.__rotationIndex += 1
        self.__rotationIndex %= 4
        pass

    def setRotation(self, rotation: int):
        self.__rotationIndex = rotation
        pass

    def getRotation(self) -> int:
        return self.__rotationIndex

    def setType(self, type: int):
        self.__tetromIndex = type
        pass

    def getType(self) -> int:
        return self.__tetromIndex

    """
    * Always 4x4 [y][x]
    """
    def getPixel(self, x: int, y: int) -> int:
        return tetromRotations[self.__tetromIndex][self.__rotationIndex][x][y]

    def getCollision(self, x: int, y: int) -> bool:
        return self.getPixel(x, y) != 0

    def setColor(self, color: int):
        self.__color = color
        pass

    def draw(self):
        for x in range(4):
            for y in range(4):
                if self.getPixel(x, y) != 0:
                    calcX: int = x + self.__mapOffsetX + self.__positionX
                    calcY: int = y + self.__mapOffsetY + self.__positionY
                    Display.Display.drawPixel(calcX, calcY, self.__color)
        pass
