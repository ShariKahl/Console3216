# #include "Arduino.h"
# #include "sprite.h"
import Sprite

import Display

import Sound

EVENT_NO_BOUNCE: int = 0
EVENT_BOUNCE_MIDDLE: int = 1
EVENT_BOUNCE_LOW: int = 2
EVENT_BOUNCE_HIGH: int = 3
EVENT_BOUNCE_MIDDLE_BEND: int = 4

PADDLE_IDLE: int = 0
PADDLE_BEND: int = 1
PADDLE_HOLD: int = 2


class Paddle(Sprite.Sprite):
    def __init__(self):
        # TODO Super constructor call
        super().__init__(0, 0, 2, 5)
        self._orientation: bool = False
        self._status: int = 0
        self._bounceSoundEffect: int = 0

        self.unBend()
        self.activate()

    def setOrientation(self, paddleOrientation: bool):
        self._orientation = paddleOrientation
        pass

    def setBounceSoundEffect(self, newBounceSoundEffect: int):
        # TODO Siehe inline Funktion weiter unten für C++ Code
        self._bounceSoundEffect = newBounceSoundEffect

    def bend(self):
        self._bitmap[0] = Display.Display.getColorFrom565(0xff00)
        self._bitmap[1] = Display.Display.getColorFrom565(0x0000)
        self._bitmap[2] = Display.Display.getColorFrom565(0x0000)
        self._bitmap[3] = Display.Display.getColorFrom565(0x0000)
        self._bitmap[4] = Display.Display.getColorFrom565(0xff00)
        
        self._bitmap[5] = Display.Display.getColorFrom565(0x0000)
        self._bitmap[6] = Display.Display.getColorFrom565(0x0ff0)
        self._bitmap[7] = Display.Display.getColorFrom565(0x0ff0)
        self._bitmap[8] = Display.Display.getColorFrom565(0x0ff0)
        self._bitmap[9] = Display.Display.getColorFrom565(0x0000)

        if self._orientation:
            # TODO pyserial
            # Serial.println("mirror!")
            self.mirrorY()
        else:
            # Serial.println("no mirror!")
            pass
        
        if self._status == PADDLE_IDLE:
            self._status = PADDLE_BEND
        else:
            # TODO commented out in C++ source
            # this->status = PADDLE_HOLD
            pass
        pass

    def unBend(self):
        self._bitmap[0] = Display.Display.getColorFrom565(0xff00)
        self._bitmap[1] = Display.Display.getColorFrom565(0x00ff)
        self._bitmap[2] = Display.Display.getColorFrom565(0x00ff)
        self._bitmap[3] = Display.Display.getColorFrom565(0x00ff)
        self._bitmap[4] = Display.Display.getColorFrom565(0xff00)
        
        self._bitmap[5] = Display.Display.getColorFrom565(0x0000)
        self._bitmap[6] = Display.Display.getColorFrom565(0x0000)
        self._bitmap[7] = Display.Display.getColorFrom565(0x0000)
        self._bitmap[8] = Display.Display.getColorFrom565(0x0000)
        self._bitmap[9] = Display.Display.getColorFrom565(0x0000)

        if self._orientation:
            self.mirrorY()
        
        self._status = PADDLE_IDLE
        pass

    # TODO C++ Source body empty
    def isBend(self) -> bool:
        pass

    def move(self, direction: bool):
        if direction:
            if self._yPos > 0:
                # TODO C++ Source:
                # Sprite::move(0,-1);
                super().move(0, -1)
        else:
            if self._yPos < Display.DISPLAY_Y_EXTEND - self._yExtend:
                # TODO C++ Source:
                # Sprite::move(0,1);
                super().move(0, 1)
        pass

    def checkContact(self, xPos: int, yPos: int):
        event: int = EVENT_NO_BOUNCE
        # TODO Unused variable
        # bend: bool = self.isBend()

        if self._orientation:
            if not (self._xPos == xPos):
                return EVENT_NO_BOUNCE
        else:
            if not (self._xPos + 1 == xPos):
                return EVENT_NO_BOUNCE
        
        if self._yPos == yPos:
            event = EVENT_BOUNCE_HIGH
        elif self._yPos + self._yExtend - 1 == yPos:
            event = EVENT_BOUNCE_LOW
        elif (yPos > self._yPos) and (yPos < self._yPos + self._yExtend):
            event = EVENT_BOUNCE_MIDDLE
        
        # TODO pyserial
        # Serial.print("event :");
        # Serial.println(event);
        # Serial.print("****sound :");
        # Sound::playSound(this->bounceSoundEffect, 9, 100);
        
        Sound.Sound.playSoundDura(self._bounceSoundEffect, 9, 100)

        return event

# inline void Paddle::setBounceSoundEffect(uint8_t newBounceSoundEffect)
# {
# 	this->bounceSoundEffect = newBounceSoundEffect;
# }
