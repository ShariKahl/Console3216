# #include "Arduino.h"
# #include "sprite.h"
import Sprite
# #include "Joystick.h"
import Joystick

import Display

PILOT_TRIGGER_UP = 1
PILOT_TRIGGER_BODY = 2


class Pilot(Sprite.Sprite):
    def __init__(self):
        # TODO Super constructor call
        super().__init__(0, 0, 1, 1)

        # TODO C++: Joystick *joystick;
        self._joystick: Joystick.Joystick = None

        self._movementCounter: int = 0
        self._movementPrescaler: int = 0

        self._moved: int = 0

        # TODO Sprite Class
        self._bitmap[0] = Display.Display.getColorFrom333(7, 0, 0)
        self.activate()

    # TODO C++: void init(Joystick & myJoystick);
    def init(self, myJoystick: Joystick.Joystick):
        self._joystick = myJoystick
        pass

    def checkActions(self):
        if self._joystick.isLeft():
            self._xPos -= 1
            if (self._xPos < 0):
                self._xPos = 0
        elif self._joystick.isRight():
            self._xPos += 1
            if (self._xPos > 31):
                self._xPos = 31
        
        trigger: int = 0

        if self._joystick.isButtonTop():
            # TODO C++ Source used |= assignment
            trigger = PILOT_TRIGGER_UP
        if self._joystick.isButtonBody():
            trigger = PILOT_TRIGGER_BODY
        
        return trigger
