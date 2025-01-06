import random

# #include "Arduino.h"
# #include "sprite.h"
import Sprite
# #include "Joystick.h"
import Joystick
# #include "inv_alien.h"
import Inv_alien

ALIENS_SQUAD_MAX_SIZE: int = 24

# **Definition von SquadMember_t**
class SquadMember_t:
    def __init__(self, alien_type: int, x_delta: int, y_delta: int):
        self.type: int = alien_type
        self.xDelta: int = x_delta
        self.yDelta: int = y_delta

# **Definition der vorgefertigten Alien-Squads**
alienSquads = [
    [
        SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, x * 3, y)
        for y in [1, 3, 5]
        for x in range(8)
    ],
    [
        SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 4, 3),
        SquadMember_t(Inv_alien.ALIEN_TYPE_BOMBER, 7, 6),
    ]
]

class Squad:
    def __init__(self):
        self._type: int = 0
        self._movementCounter: int = 0
        self._movementPrescaler: int = 0
        self._aliens = [Inv_alien.Alien() for _ in range(ALIENS_SQUAD_MAX_SIZE)]
        self._movePrescaler: int = 0

    def prepareSquad(self):
        """
        Initialisiert die Aliens in der Squad mit einem Typ und einer Position
        basierend auf den vorgefertigten Squads.
        """
        for i in range(ALIENS_SQUAD_MAX_SIZE):
            alien = self._aliens[i]
            if i < len(alienSquads[self._type]):
                member = alienSquads[self._type][i]
                alien.setType(member.type)
                alien.setPosition(member.xDelta, member.yDelta)
                alien.activate()
            else:
                alien.deActivate()

    def draw(self):
        """
        Zeichnet alle aktiven Aliens auf dem Display.
        """
        for alien in self._aliens:
            if alien.isActive():
                alien.draw()

    def move(self):
        """
        Bewegt die Aliens in der Squad basierend auf zufälligen Bewegungsmustern.
        """
        self._movePrescaler += 1
        if self._movePrescaler < 4:
            return

        self._movePrescaler = 0
        alienMaxXPos: int = 0
        alienMinXPos: int = 31

        # Berechnet die Positionen der Aliens
        for alien in self._aliens:
            if alien.isActive():
                alienMaxXPos = max(alienMaxXPos, alien.getXPos())
                alienMinXPos = min(alienMinXPos, alien.getXPos())

        randomNr = random.randrange(3)
        direction: bool = False

        if randomNr == 0 and alienMaxXPos < 31:
            direction = True
        elif randomNr == 2 and alienMinXPos > 0:
            direction = False

        # Bewegt die Aliens in der berechneten Richtung
        for alien in self._aliens:
            if alien.isActive():
                alien.move(direction)

    def descent(self):
        """
        Bewegt die Aliens nach unten.
        """
        for alien in self._aliens:
            if alien.isActive():
                alien.descent()

    def checkCollision(self, xPos: int, yPos: int) -> int:
        """
        Überprüft, ob ein Projektil ein Alien trifft, und gibt die Punkte zurück.
        """
        points: int = 0

        for alien in self._aliens:
            if alien.isActive() and alien.getXPos() == xPos and alien.getYPos() == yPos:
                alien.deActivate()
                points = alien.getPoints()

        return points
