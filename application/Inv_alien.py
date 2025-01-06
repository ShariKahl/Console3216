import Sprite
import Display

ALIEN_TYPE_NONE = 0
ALIEN_TYPE_SCOUT = ALIEN_TYPE_NONE + 1
ALIEN_TYPE_FIGHTER = ALIEN_TYPE_SCOUT + 1
ALIEN_TYPE_BOMBER = ALIEN_TYPE_FIGHTER + 1

ALIEN_POINTS_NONE = 0
ALIEN_POINTS_SCOUT = 5
ALIEN_POINTS_FIGHTER = 10
ALIEN_POINTS_BOMBER = 20

# Farben basierend auf Alien-Typen
ALIEN_COLOR_SCOUT = Display.Display.getColorFrom333(7, 3, 0)
ALIEN_COLOR_FIGHTER = Display.Display.getColorFrom333(7, 0, 7)
ALIEN_COLOR_BOMBER = Display.Display.getColorFrom333(3, 7, 7)


class Alien(Sprite.Sprite):
    def __init__(self):
        super().__init__(0, 0, 1, 1)
        
        self._type: int = ALIEN_TYPE_NONE
        self._movementCounter: int = 0
        self._movementPrescaler: int = 5  # Standard-Prescaler-Wert
        
        # Initialfarbe
        self._bitmap[0] = ALIEN_COLOR_SCOUT
        self.activate()

    def setType(self, newType: int):
        """
        Setzt den Typ des Aliens und aktualisiert die Farbe entsprechend.
        """
        if newType in [ALIEN_TYPE_NONE, ALIEN_TYPE_SCOUT, ALIEN_TYPE_FIGHTER, ALIEN_TYPE_BOMBER]:
            self._type = newType

            # Farbe entsprechend dem Typ setzen
            if newType == ALIEN_TYPE_SCOUT:
                self._bitmap[0] = ALIEN_COLOR_SCOUT
            elif newType == ALIEN_TYPE_FIGHTER:
                self._bitmap[0] = ALIEN_COLOR_FIGHTER
            elif newType == ALIEN_TYPE_BOMBER:
                self._bitmap[0] = ALIEN_COLOR_BOMBER
            else:
                self._bitmap[0] = Display.Display.getColorFrom333(0, 0, 0)  # Keine Farbe
        else:
            raise ValueError("Ungültiger Alien-Typ!")

    def getType(self) -> int:
        """
        Gibt den Typ des Aliens zurück.
        """
        return self._type

    def getPoints(self) -> int:
        """
        Gibt die Punkte basierend auf dem Typ des Aliens zurück.
        """
        if self._type == ALIEN_TYPE_SCOUT:
            return ALIEN_POINTS_SCOUT
        elif self._type == ALIEN_TYPE_FIGHTER:
            return ALIEN_POINTS_FIGHTER
        elif self._type == ALIEN_TYPE_BOMBER:
            return ALIEN_POINTS_BOMBER
        return ALIEN_POINTS_NONE

    def move(self, direction: bool):
        """
        Bewegt das Alien in die angegebene Richtung.
        """
        if self._movementCounter == 0:
            if direction:
                self._xPos += 1
            else:
                self._xPos -= 1

            # Bewegungscounter zurücksetzen
            self._movementCounter = self._movementPrescaler
        else:
            self._movementCounter -= 1

    def descent(self):
        """
        Lässt das Alien eine Reihe nach unten fallen.
        """
        self._yPos += 1
