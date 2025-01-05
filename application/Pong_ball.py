import random

# #include "Arduino.h"
# #include "sprite.h"
import Sprite

import Display

class Ball(Sprite.Sprite):
    def __init__(self):
        # TODO Super constructor call
        super().__init__(0, 0, 1, 1)

        self._bitmap[0] = Display.Display.getColorFrom333(7, 0, 0)
        self.activate()

        self._vectorX: int = 0
        self._vectorY: int = 0

        self._intPosX: int = 0
        self._intPosY: int = 0

        self._movementCounter: int = 0
        self._movementPrescaler: int = 0

        # TODO C++: uint8_t moved:1;
        self._moved: int = 0

    def setPosition(self, newXPos: int, newYPos: int):
        self._intPosX = newXPos << 4
        self._intPosY = newYPos << 4

        self._xPos = newXPos
        self._yPos = newYPos
        pass

    def increaseSpeed(self):
        if self._movementPrescaler > 0:
            self._movementPrescaler -= 1
        pass

    def decreaseSpeed(self):
        self._movementPrescaler += 1
        pass

    def setSpeed(self, newSpeed: int):
        self._movementPrescaler = newSpeed
        self._movementCounter = 0
        pass

    def move(self):
        if self._movementCounter >= self._movementPrescaler:
            self._intPosX += self._vectorX
            self._intPosY += self._vectorY

            # TODO
            self._xPos = self._intPosX >> 4
            self._yPos = self._intPosY >> 4

            self._movementCounter = 0
            self._moved = 1
        else:
            self._movementCounter += 1
            self._moved = 0
        pass

    def setVector(self, x: int, y: int):
        self._vectorX = x
        self._vectorY = y
        pass

    def bounce(self):
        self._vectorX = - self._vectorX
        self._vectorY = - self._vectorY

        # randomize
        self._vectorY = self._randomizeVector(self._vectorY)
        self._vectorX = self._randomizeVector(self._vectorX)

        self._correctVector()
        pass

    def bounceX(self):
        self._vectorX = - self._vectorX

        # randomize
        # vector darf das Vorzeichen nicht wechseln
        self._vectorY = self._randomizeVector(self._vectorY)
        self._vectorX = self._randomizeVector(self._vectorX)

        self._correctVector()
        pass

    def bounceY(self):
        self._vectorY = - self._vectorY

        # randomize
        self._vectorY = self._randomizeVector(self._vectorY)
        self._vectorX = self._randomizeVector(self._vectorX)

        self._correctVector()
        pass

    def hasMoved(self) -> bool:
        if self._moved == 1:
            return True
        
        return False

    def _correctVector(self):
        # Comments from C++ Source

        # if ( this->vectorX > 0x15)
        if self._vectorX > 15:
            # this->vectorX = 0x15;
            self._vectorX = -15
        elif self._vectorX < -15:
            self._vectorX = -15
        
        # if ( this->vectorY > 0x15)
        if self._vectorY > 15:
            # this->vectorY = 0x15;
            self._vectorY = -15
        elif self._vectorY < -15:
            # this->vectorY = -15;
            self._vectorY = 15
        pass

    def _randomizeVector(vector: int) -> int:
        newVector: int = vector

        # vector darf das Vorzeichen nicht wechseln
        newVector += random.randrange(2) - 1

        if ((vector < 0) and (newVector > 0)) or ((vector > 0) and (newVector < 0)):
            newVector = vector
        
        return newVector
