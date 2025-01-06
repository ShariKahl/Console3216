import random
import Sprite
import Display


class Ball(Sprite.Sprite):
    def __init__(self):
        super().__init__(0, 0, 1, 1)
        self._bitmap[0] = Display.Display.getColorFrom333(7, 0, 0)
        self.activate()

        self._vectorX: int = 0
        self._vectorY: int = 0

        self._intPosX: int = 0
        self._intPosY: int = 0

        self._movementCounter: int = 0
        self._movementPrescaler: int = 0

        self._moved: int = 0

    def setPosition(self, newXPos: int, newYPos: int):
        self._intPosX = newXPos << 4
        self._intPosY = newYPos << 4
        self._xPos = newXPos
        self._yPos = newYPos

    def increaseSpeed(self):
        if self._movementPrescaler > 0:
            self._movementPrescaler -= 1

    def decreaseSpeed(self):
        self._movementPrescaler += 1

    def setSpeed(self, newSpeed: int):
        self._movementPrescaler = newSpeed
        self._movementCounter = 0

    def move(self):
        if self._movementCounter >= self._movementPrescaler:
            self._intPosX += self._vectorX
            self._intPosY += self._vectorY

            self._xPos = self._intPosX >> 4
            self._yPos = self._intPosY >> 4

            self._movementCounter = 0
            self._moved = 1
        else:
            self._movementCounter += 1
            self._moved = 0

    def setVector(self, x: int, y: int):
        self._vectorX = x
        self._vectorY = y

    def bounce(self):
        self._vectorX = -self._vectorX
        self._vectorY = -self._vectorY

        self._vectorY = self._randomizeVector(self._vectorY)
        self._vectorX = self._randomizeVector(self._vectorX)

        self._correctVector()

    def bounceX(self):
        self._vectorX = -self._vectorX

        self._vectorY = self._randomizeVector(self._vectorY)
        self._vectorX = self._randomizeVector(self._vectorX)

        self._correctVector()

    def bounceY(self):
        self._vectorY = -self._vectorY

        self._vectorY = self._randomizeVector(self._vectorY)
        self._vectorX = self._randomizeVector(self._vectorX)

        self._correctVector()

    def hasMoved(self) -> bool:
        return self._moved == 1

    def _correctVector(self):
        # Begrenzung des Vektors, um unkontrollierte Bewegung zu vermeiden
        self._vectorX = max(min(self._vectorX, 15), -15)
        self._vectorY = max(min(self._vectorY, 15), -15)

    def _randomizeVector(self, vector: int) -> int:
        newVector: int = vector + random.randrange(-1, 2)
        if ((vector < 0 and newVector > 0) or (vector > 0 and newVector < 0)):
            newVector = vector  # Vorzeichenwechsel verhindern
        return newVector
