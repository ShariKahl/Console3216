import random

# #include "Arduino.h"
# #include "sprite.h"
import Sprite
# #include "Joystick.h"
import Joystick
# #include "inv_alien.h"
import Inv_alien

# TODO Schreibfehler behoben: ALLIENS_SQUAD_MAX_SIZE -> ALIENS_SQUAD_MAX_SIZE
ALIENS_SQUAD_MAX_SIZE: int = 24


# TODO typedef struct {...} SquadMember_t
class SquadMember_t:
    def __init__(self):
        self.type: int = 0
        self.xDelta: int = 0
        self.yDelta: int = 0

# TODO C++ Source:
# const SquadMember_t alienSquads [2] [ALLIENS_SQUAD_MAX_SIZE] = {...}
alienSquads = [SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 0, 1), SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 3, 1), SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 6, 1),
      SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 9, 1), SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 12, 1), SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 15, 1),
      SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 18, 1), SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 21, 1), SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 0, 3),
      SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 3, 3), SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 6, 3), SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 9, 3),
      SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 12, 3), SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 15, 3), SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 18, 3),
      SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 21, 3), SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 0, 5), SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 3, 5),
      SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 6, 5), SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 9, 5), SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 12, 5),
      SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 15, 5), SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 18, 5), SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 21, 5)], [
          SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 4, 3), SquadMember_t(Inv_alien.ALIEN_TYPE_BOMBER, 7, 6)]

# TODO C++ does not allow multi-size arrays, Python does, so this array will not be a[2][24], but a[0][24] and a[1][2] instead of a[1][24] with empty slots
# TODO Not sure if the empty spots will be required by the code or not.
# TODO The following code produces a correctly sized array with the same values, but calculated instead of hardcoded:
# alienSquads = [[None for _ in range(ALIENS_SQUAD_MAX_SIZE)] for _ in range(2)]
# yDelta = 1

# for i in range(ALIENS_SQUAD_MAX_SIZE):
#     alienSquads[0][i] = SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, i * 3 % 24, yDelta)
#     if i > 0 and i % 8 == 0:
#         yDelta += 2

# alienSquads[1][0] = SquadMember_t(Inv_alien.ALIEN_TYPE_SCOUT, 4, 3)
# alienSquads[1][1] = SquadMember_t(Inv_alien.ALIEN_TYPE_BOMBER, 7, 6)

class Squad:
    def __init__(self):
        self._type: int = 0
        self._movementCounter: int = 0
        self._movementPrescaler: int = 0
        # TODO C++: Alien aliens[ALLIENS_SQUAD_MAX_SIZE];
        self._aliens = [None for _ in range(ALIENS_SQUAD_MAX_SIZE)]
        # TODO Schreibfehler behoben: _moviePrescaller -> _movePrescaler
        self._movePrescaler: int = 0

    def prepareSquad(self):
        pass

    def draw(self):
        for alienIndex in range(ALIENS_SQUAD_MAX_SIZE):
            self._aliens[alienIndex].draw()
        pass

    def move(self):
        alienMaxXPos: int = 0
        alienMinXPos: int = 31

        self._movePrescaler += 1
        if self._movePrescaler < 4:
            return

        self._movePrescaler = 0
        for squadCounter in ALIENS_SQUAD_MAX_SIZE:
            if alienMaxXPos < self._aliens[squadCounter].getXPos():
                alienMaxXPos = self._aliens[squadCounter].getXPos()
            
            if alienMinXPos > self._aliens[squadCounter].getXPos():
                alienMinXPos = self._aliens[squadCounter].getXPos()
            
        direction: bool = False

        randomNr = random.randrange(3)
        # TODO Source C++ code was Switch/Case
        if randomNr == 0:
            if alienMaxXPos < 31:
                direction = True

                for squadCounter in range(ALIENS_SQUAD_MAX_SIZE):
                    self._aliens[squadCounter].move(direction)
        elif randomNr == 2:
            if alienMinXPos > 0:
                direction = False

                for squadCounter in range(ALIENS_SQUAD_MAX_SIZE):
                    self._aliens[squadCounter].move(direction)
        pass

    # TODO No definition in C++ source
    def descent(self):
        pass

    # TODO C++ Source had a typo: checkColision
    def checkCollision(self, xPos: int, yPos: int) -> int:
        # TODO Unused in C++ source
        # alienXPos: int
        # alienYPos: int
        points: int = 0

        for squadCounter in range(ALIENS_SQUAD_MAX_SIZE):
            if self._aliens[squadCounter].isActive():
                if self._aliens[squadCounter].getXPos() == xPos:
                    if self._aliens[squadCounter].getYPos() == yPos:
                        self._aliens[squadCounter].deActivate()
                        points = self._aliens[squadCounter].getPoints()
        
        return points
