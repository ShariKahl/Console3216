# #include "Arduino.h"
# #include "sprite.h"
import Sprite
import Display

class Guests(Sprite.Sprite):
    def __init__(self, xPos: int = 0, yPos: int = 0, width: int = 1, height: int = 1):
        super().__init__(xPos, yPos, width, height)

        self._vectorY: int = 1  # Bewegungsrichtung auf der Y-Achse (1 = nach unten, -1 = nach oben)
        self._movementPrescaler: int = 0  # Steuert die Geschwindigkeit der Bewegung
        self._active: bool = False

        # Beispiel-Bitmap für Gäste (Farben anpassen)
        self._bitmap = [Display.Display.getColorFrom333(0, 5, 7) for _ in range(width * height)]

    def move(self):
        if not self._active:
            return

        # Bewegung in Y-Richtung basierend auf _vectorY
        self._yPos += self._vectorY

        # Grenzenprüfung: Wenn die Gäste den Bildschirm verlassen, deaktivieren
        if self._yPos < 0 or self._yPos >= Display.Display.getHeight():
            self.deActivate()

    def draw(self):
        if self._active:
            super().draw()  # Verwendet die `draw`-Methode der `Sprite`-Klasse

    def activate(self):
        self._active = True

    def deActivate(self):
        self._active = False

    def setDirection(self, direction: bool):
        # Richtung setzen: True = nach unten, False = nach oben
        self._vectorY = 1 if direction else -1

    def isActive(self) -> bool:
        return self._active
