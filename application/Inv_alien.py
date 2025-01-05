# #include "Arduino.h"
# #include "sprite.h"
import Sprite
# #include "Joystick.h"
import Joystick

import Display

ALIEN_TYPE_NONE = 0
ALIEN_TYPE_SCOUT = ALIEN_TYPE_NONE + 1
ALIEN_TYPE_FIGHTER = ALIEN_TYPE_SCOUT + 1
ALIEN_TYPE_BOMBER = ALIEN_TYPE_FIGHTER + 1

ALIEN_POINTS_NONE = 0
ALIEN_POINTS_SCOUT = 5
ALIEN_POINTS_FIGHTER = 10
ALIEN_POINTS_BOMBER = 20


class Alien(Sprite.Sprite):
    def __init__(self):
        super().__init__(0, 0, 1, 1)
        
        self._type: int = ALIEN_TYPE_NONE
        self._movementCounter: int = 0
        self._movementPrescaler: int = 0
        
        # bitmap is part of Sprite.py
        self._bitmap[0] = Display.Display.getColorFrom333(7, 3, 0)
        self.activate()

    def setType(self, newType: int):
        self._type = newType
        pass

    def getType(self) -> int:
        return self._type

    def getPoints(self) -> int:
        returnPoints = ALIEN_POINTS_NONE

        # C++ Source was switch/case and had multiple return statements
        if self._type == ALIEN_TYPE_SCOUT:
            returnPoints = ALIEN_POINTS_SCOUT
        elif self._type == ALIEN_TYPE_FIGHTER:
            returnPoints = ALIEN_POINTS_FIGHTER
        elif self._type == ALIEN_TYPE_BOMBER:
            returnPoints = ALIEN_POINTS_BOMBER
        
        return returnPoints

    def move(self, direction: bool):
        if direction:
            self._xPos += 1
        else:
            self._xPos -= 1
        pass

    # TODO C++ source does not have a definition
    def descent(self):
        pass
