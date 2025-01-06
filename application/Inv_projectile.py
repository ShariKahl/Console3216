# #include "Arduino.h"
# #include "sprite.h"
import Sprite
import Display

class Projectile(Sprite.Sprite):
    def __init__(self):
        # Super-Konstruktor aufrufen und Sprite initialisieren
        super().__init__(0, 0, 1, 1)
        
        # Bewegungsrichtung und Status des Projektils
        self._vectorY: int = 0
        self._movementPrescaler: int = 0
        self._active: bool = False

        # Farbe des Projektils definieren
        self._bitmap[0] = Display.Display.getColorFrom333(4, 7, 0)

    # Bewegt das Projektil in die aktuelle Richtung
    def move(self):
        if self._active:
            # Überprüfen, ob das Projektil innerhalb des Spielfeldes bleibt
            if 0 <= self._yPos + self._vectorY < 16:  # Annahme: Spielfeldhöhe = 16
                self._yPos += self._vectorY
            else:
                # Deaktivieren, wenn es das Spielfeld verlässt
                self.deActivate()

    # Setzt die Bewegungsrichtung des Projektils
    def setDirection(self, direction: bool):
        # Richtung nach oben oder unten
        self._vectorY = 1 if direction else -1

    # Aktiviert das Projektil
    def activate(self):
        self._active = True

    # Deaktiviert das Projektil
    def deActivate(self):
        self._active = False

    # Überprüft, ob das Projektil aktiv ist
    def isActive(self) -> bool:
        return self._active

    # Zeichnet das Projektil auf dem Display
    def draw(self):
        if self.isActive():
            super().draw()
