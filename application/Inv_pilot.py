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
        # Super-Konstruktor aufrufen und Sprite initialisieren
        super().__init__(0, 0, 1, 1)

        # Joystick-Instanz
        self._joystick: Joystick.Joystick = None

        # Bewegungssteuerung
        self._movementCounter: int = 0
        self._movementPrescaler: int = 0
        self._moved: int = 0

        # Sprite-Bitmap für den Piloten
        self._bitmap[0] = Display.Display.getColorFrom333(7, 0, 0)
        self.activate()

    # Initialisiert den Piloten mit dem zugehörigen Joystick
    def init(self, myJoystick: Joystick.Joystick):
        self._joystick = myJoystick

    # Überprüft die Eingaben des Joysticks und gibt Trigger zurück
    def checkActions(self) -> int:
        # Bewegung nach links
        if self._joystick.isLeft():
            self._xPos -= 1
            if self._xPos < 0:
                self._xPos = 0

        # Bewegung nach rechts
        elif self._joystick.isRight():
            self._xPos += 1
            if self._xPos > 31:  # Annahme: Spielfeldbreite = 32
                self._xPos = 31

        # Trigger überprüfen
        trigger: int = 0
        if self._joystick.isButtonTop():
            trigger |= PILOT_TRIGGER_UP
        if self._joystick.isButtonBody():
            trigger |= PILOT_TRIGGER_BODY

        return trigger

    # Zeichnet den Piloten auf das Display
    def draw(self):
        if self.isActive():
            super().draw()

    # Aktiviert den Piloten
    def activate(self):
        self._active = True

    # Deaktiviert den Piloten
    def deActivate(self):
        self._active = False

    # Überprüft, ob der Pilotenstatus aktiv ist
    def isActive(self) -> bool:
        return self._active
