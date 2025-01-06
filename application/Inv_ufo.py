# #include "Arduino.h"
# #include "sprite.h"
import Sprite
# #include "Joystick.h"
import Joystick

import Display


class Ufo(Sprite.Sprite):
    def __init__(self):
        """
        Initialisiert das UFO mit der Standardposition und -farbe.
        """
        super().__init__(0, 0, 1, 1)  # UFO hat eine Größe von 1x1 Pixel
        self._movementPrescaler: int = 0
        self._bitmap[0] = Display.Display.getColorFrom333(7, 7, 7)  # Weiß als Standardfarbe
        self.activate()
        self._yPos = 0

    def move(self):
        """
        Bewegt das UFO nach rechts. Deaktiviert das UFO, wenn es den Bildschirmrand erreicht.
        """
        self._xPos += 1
        if self._xPos > 31:  # Spielfeldbreite ist 32
            self.deActivate()

    def checkCollision(self, xPos: int) -> bool:
        """
        Überprüft, ob ein Projektil das UFO getroffen hat.
        :param xPos: Die x-Position des Projektils.
        :return: True, wenn das Projektil das UFO getroffen hat, sonst False.
        """
        # Debugging-Ausgabe (in Python durch print ersetzbar, wenn benötigt):
        # print(f"Projektil: {xPos}, UFO: {self._xPos}")

        if self.isActive() and self._xPos == xPos:
            return True
        return False

    def explode(self):
        """
        Simuliert die Explosion des UFOs. Diese Methode könnte erweitert werden, um eine Animation oder Soundeffekte hinzuzufügen.
        """
        # Mögliche Implementierung:
        # - Anzeige einer Animation
        # - Abspielen eines Soundeffekts
        # - Temporäres Ändern der Farbe des UFOs
        pass
