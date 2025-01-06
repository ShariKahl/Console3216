from enum import Enum
import random

# #include "Arduino.h"
# #include "game.h"
import Game
# #include "inc/TetrisTetrom.h"
import TetrisTetrom

import Display
import NumericDisplay


class TetrisPlayerStatus(Enum):
    PLAYING = 0
    LOST = 1


class TetrisPlayer:
    def __init__(self, offsetX: int, offsetY: int):
        self.temporaryCounter: int = 0

        self.status: TetrisPlayerStatus = None
        # TODO C++: TetrisTetrom* currentTetrom;
        self.currentTetrom: TetrisTetrom.TetrisTetrom = None
        # TODO C++: TetrisTetrom* nextTetrom;
        self.nextTetrom: TetrisTetrom.TetrisTetrom = None
        self.deltaSum: int = 0
        self.updateDelay: int = 0
        self.mapColor: int = 0
        self.mapOffsetX: int = offsetX
        self.mapOffsetY: int = offsetY
        self.softDropDelay: int = 50
        self.normalDelay: int = 200

        # TODO C++: uint8_t map[16][10] = {...};
        self.map = [[0 for _ in range(10)] for _ in range(16)]

        self.playerpoints: int = 0

        self.init()

    def canMoveTetrom(self, tetrom: TetrisTetrom.TetrisTetrom, xOffset: int, yOffset: int) -> bool:
        tetrom.moveRelative(xOffset, yOffset)
        collides: bool = self.hasCollisions(tetrom)
        tetrom.moveRelative(-xOffset, -yOffset)
        return not collides

    def canRotateTetrom(self, tetrom: TetrisTetrom.TetrisTetrom, clockwise: bool) -> bool:
        if clockwise:
            tetrom.rotateRight()
        else:
            tetrom.rotateLeft()

        collides: bool = self.hasCollisions(tetrom)

        if clockwise:
            tetrom.rotateLeft()
        else:
            tetrom.rotateRight()

        return not collides

    def initializeTetroms(self):
        self.currentTetrom = self.generateTetrom()
        self.nextTetrom = self.generateTetrom()

    def assignNextTetroms(self):
        self.currentTetrom = self.nextTetrom
        self.nextTetrom = self.generateTetrom()

    def generateTetrom(self) -> TetrisTetrom.TetrisTetrom:
        tetrom = TetrisTetrom.TetrisTetrom(self.mapOffsetX, self.mapOffsetY)
        tetrom.setType(random.randrange(0, 7))  # Random type
        tetrom.setPosition(5, -5)  # Top center?
        rColor: int = Display.Display.getColorFrom333(random.randrange(0, 3), random.randrange(0, 3), random.randrange(0, 3))
        # TODO C++ Source overrides previous line
        rColor = Display.Display.getColorFrom333(2, 2, 3)
        tetrom.setColor(rColor)
        return tetrom

    def logicalUpdate(self, delta: int):
        tetrom = self.getCurrentTetrom()

        posY: int = tetrom.getY()
        posX: int = tetrom.getX()

        if not self.canMoveTetrom(tetrom, 0, 1):  # +Y direction!!! change <- TODO Comment from C++ Source
            # Will collide -> place it now. Generate new.
            if posY < 0:
                self.status = TetrisPlayerStatus.LOST
            else:
                self.placeOnMap(tetrom)
                for locY in range(16):
                    if self.checkLine(locY):
                        self.removeLine(locY)
                        self.playerpoints += 10

                self.assignNextTetroms()
        else:
            posY += 1
            tetrom.setPosition(posX, posY)

    def hasCollisions(self, tetrom: TetrisTetrom.TetrisTetrom) -> bool:
        for x in range(4):
            for y in range(4):
                canCollide: bool = tetrom.getCollision(x, y)
                if canCollide:
                    if not self.mapEmpty(tetrom.getX() + x, tetrom.getY() + y):
                        return True
        return False

    def mapEmpty(self, x: int, y: int) -> bool:
        if ((x > 9) or (x < 0)):
            return False

        if y > 15:
            return False

        if y < 0:
            return True

        return self.map[y][x] == 0

    def placeOnMap(self, tetrom: TetrisTetrom.TetrisTetrom):
        posX: int = tetrom.getX()
        posY: int = tetrom.getY()
        for x in range(4):
            for y in range(4):
                if tetrom.getCollision(x, y):
                    self.changeMap(x + posX, y + posY, 1)

    def changeMap(self, x: int, y: int, value: int):
        if (y >= 0) and (x >= 0) and (y < 16) and (x < 10):
            self.map[y][x] = value

    def moveIfPossible(self, tetrom: TetrisTetrom.TetrisTetrom, xOffset: int, yOffset: int):
        if self.canMoveTetrom(tetrom, xOffset, yOffset):
            tetrom.moveRelative(xOffset, yOffset)

    def rotateIfPossible(self, tetrom: TetrisTetrom.TetrisTetrom, clockwise: bool):
        if self.canRotateTetrom(tetrom, clockwise):
            if clockwise:
                tetrom.rotateRight()
            else:
                tetrom.rotateLeft()

    def returnPlayerPoints(self) -> int:
        return self.playerpoints

    def displayPlayerPoints(self, b: bool):
        if b:
            NumericDisplay.NumericDisplay.displayValue(NumericDisplay.DISPLAY_LEFT, self.playerpoints)
        else:
            NumericDisplay.NumericDisplay.displayValue(NumericDisplay.DISPLAY_RIGHT, self.playerpoints)

    def init(self):
        self.playerpoints = 0
        self.status = TetrisPlayerStatus.PLAYING
        self.mapColor = Display.Display.getColorFrom333(2, 0, 2)
        self.temporaryCounter = 0
        self.deltaSum = 0
        self.updateDelay = self.normalDelay

        self.initializeTetroms()

    def reset(self):
        self.init()
        for x in range(10):
            for y in range(16):
                self.changeMap(x, y, 0)

    def getStatus(self) -> TetrisPlayerStatus:
        return self.status

    def draw(self):
        color: int = self.mapColor
        for x in range(10):
            for y in range(16):
                if self.map[y][x] != 0:
                    Display.Display.drawPixel(x + self.mapOffsetX, y + self.mapOffsetY, color)

        tetrom: TetrisTetrom.TetrisTetrom = self.getCurrentTetrom()
        tetrom.draw()

    def drawNextTetroms(self, offsetX: int, offsetY: int):
        color: int = Display.Display.getColorFrom333(0, 0, 2)

        for x in range(4):
            for y in range(4):
                if self.nextTetrom.getPixel(x, y):
                    Display.Display.drawPixel(x + offsetX, y + offsetY, color)

    def update(self, delta: int):
        self.deltaSum += delta
        if self.deltaSum >= self.updateDelay:
            self.logicalUpdate(delta)
            self.deltaSum = 0

    def getCurrentTetrom(self) -> TetrisTetrom.TetrisTetrom:
        return self.currentTetrom

    def getNextTetrom(self) -> TetrisTetrom.TetrisTetrom:
        return self.nextTetrom

    def softDropOn(self):
        self.updateDelay = self.softDropDelay

    def softDropOff(self):
        self.updateDelay = self.normalDelay

    def inputRotateClockwise(self):
        self.rotateIfPossible(self.getCurrentTetrom(), True)

    def inputRotateCounterClockwise(self):
        self.rotateIfPossible(self.getCurrentTetrom(), False)

    def inputMoveLeft(self):
        self.moveIfPossible(self.getCurrentTetrom(), -1, 0)

    def inputMoveRight(self):
        self.moveIfPossible(self.getCurrentTetrom(), 1, 0)

    def checkLine(self, y: int) -> bool:
        for x in range(10):
            if self.map[y][x] == 0:
                return False
        return True

    def removeLine(self, y: int):
        for x in range(10):
            for yLoc in range(y, 0, -1):
                self.changeMap(x, yLoc, self.map[yLoc - 1][x])
        for x in range(10):
            self.changeMap(x, 0, 0)
