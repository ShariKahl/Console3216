# #include "Arduino.h"
# #include "sprite.h"
import Sprite

import Display

class Projectile(Sprite.Sprite):
    def __init__(self):
        super().__init__(0, 0, 1, 1)
        self._vectorY: int = 0

        self._movementPrescaler: int = 0
        self._active: bool = False

        self._bitmap[0] = Display.Display.getColorFrom333(4, 7, 0)

    def move(self):
        if self._yPos > 0 and self._yPos < 16:
            self._yPos += self._vectorY
        else:
            self.deActivate()
        pass

    def setDirection(self, direction: bool):
        if direction:
            self._vectorY = 1
        else:
            self._vectorY = -1
        pass
