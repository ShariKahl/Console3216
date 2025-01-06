from enum import Enum
import random

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
        self.mapOffsetX: int = offsetX
        self.mapOffsetY: int = offsetY
        self.positionX: int = 0
        self.positionY: int = 0
        self.rotationIndex: int = 0
        self.tetromIndex: int = 0
        self.color: int = Display.Display.getColorFrom333(2, 0, 2)

    def getX(self) -> int:
        return self.positionX

    def getY(self) -> int:
        return self.positionY

    def moveRelative(self, x: int, y: int):
        self.positionX += x
        self.positionY += y

    def setPosition(self, x: int, y: int):
        self.positionX = x
        self.positionY = y

    def rotateLeft(self):
        self.rotationIndex -= 1
        self.rotationIndex %= 4

    def rotateRight(self):
        self.rotationIndex += 1
        self.rotationIndex %= 4

    def setRotation(self, rotation: int):
        self.rotationIndex = rotation

    def getRotation(self) -> int:
        return self.rotationIndex

    def setType(self, type: int):
        self.tetromIndex = type

    def getType(self) -> int:
        return self.tetromIndex

    """
    * Always 4x4 [y][x]
    """
    def getPixel(self, x: int, y: int) -> int:
        return tetromRotations[self.tetromIndex][self.rotationIndex][x][y]

    def getCollision(self, x: int, y: int) -> bool:
        return self.getPixel(x, y) != 0

    def setColor(self, color: int):
        self.color = color

    def draw(self):
        for x in range(4):
            for y in range(4):
                if self.getPixel(x, y) != 0:
                    calcX: int = x + self.mapOffsetX + self.positionX
                    calcY: int = y + self.mapOffsetY + self.positionY
                    Display.Display.drawPixel(calcX, calcY, self.color)
