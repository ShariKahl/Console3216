import Sprite
import Display
import Sound

EVENT_NO_BOUNCE = 0
EVENT_BOUNCE_MIDDLE = 1
EVENT_BOUNCE_LOW = 2
EVENT_BOUNCE_HIGH = 3
EVENT_BOUNCE_MIDDLE_BEND = 4

PADDLE_IDLE = 0
PADDLE_BEND = 1
PADDLE_HOLD = 2 


class Paddle(Sprite.Sprite):
    def __init__(self):
        super().__init__(0, 0, 2, 5)
        self._orientation = False
        self._status = PADDLE_IDLE
        self._bounceSoundEffect = 0

        self.unBend()
        self.activate()

    def setOrientation(self, paddleOrientation: bool):
        # Setze die Ausrichtung des Schlägers.
        self._orientation = paddleOrientation

    def setBounceSoundEffect(self, newBounceSoundEffect: int):
        # Setze den Soundeffekt für das Abprallen des Schlägers.
        self._bounceSoundEffect = newBounceSoundEffect

    def bend(self):
        # Biege den Schläger und ändere sein visuelles Erscheinungsbild.
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
            self.mirrorY()

        if self._status == PADDLE_IDLE:
            self._status = PADDLE_BEND

    def unBend(self):
        # Stellt den Schläger gerade und setzt sein visuelles Erscheinungsbild zurück.
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

    def isBend(self) -> bool:
        # Überprüfe, ob der Schläger gebogen ist.
        return self._status == PADDLE_BEND

    def move(self, direction: bool):
        # Bewege den Schläger nach oben oder unten basierend auf der Richtung.
        if direction and self._yPos > 0:
            super().move(0, -1)
        elif not direction and self._yPos < Display.DISPLAY_Y_EXTEND - self._yExtend:
            super().move(0, 1)

    def checkContact(self, xPos: int, yPos: int) -> int:
        # Überprüfe den Kontakt mit dem Ball und gib die Art des Abprallens zurück.
        if self._orientation:
            if self._xPos != xPos:
                return EVENT_NO_BOUNCE
        else:
            if self._xPos + 1 != xPos:
                return EVENT_NO_BOUNCE

        event = EVENT_NO_BOUNCE
        if self._yPos == yPos:
            event = EVENT_BOUNCE_HIGH
        elif self._yPos + self._yExtend - 1 == yPos:
            event = EVENT_BOUNCE_LOW
        elif self._yPos < yPos < self._yPos + self._yExtend:
            event = EVENT_BOUNCE_MIDDLE

        Sound.Sound.playSoundDura(self._bounceSoundEffect, 9, 100)

        return event
