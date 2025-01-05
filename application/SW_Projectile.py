# #include "Arduino.h"
# #include "Joystick.h"
import Joystick


class SW_Projectile:
    def __init__(self):
        # x-Koordinate
        self.__xCoordinate: int = 0

        # y-Koordinate
        self.__yCoordinate: int = 0

        # Richtungsflag
        self.__directionLeft: bool = False

        # Valid flag
        self.__valid: bool = False

    """
     * Diese Methode gibt das Richtungsflag eines Projektils zurück.
     * Bei true ist die Flugrichtung eines Projektils links und bei
     * falls ist sie rechts.
     * @return bool directionLeft
    """
    def getDirection(self) -> bool:
        return self.__directionLeft

    def getValid(self) -> bool:
        return self.__valid

    def setValid(self, valid: bool):
        self.__valid = valid
        pass

    """
    * Diese Methode setzt das Richtungsflag eines Projektils.
    * Bei true ist die Flugrichtung eines Projektils links und bei
    * falls ist sie rechts.
    """
    def setDirection(self, directionLeft: bool):
        self.__directionLeft = directionLeft
        pass

    """
     * Diese Methode gibt die x-Koordinate eines Projektils zurück.
     * @return int xCoordinate
    """
    def getXCoordinate(self) -> int:
        return self.__xCoordinate

    """
     * Diese Methode gibt die y-Koordinate eines Projektils zurück.
     * @return int yCoordinate
    """
    def getYCoordinate(self) -> int:
        return self.__yCoordinate

    """
     * Diese Methode setzt die x-Koordinate eines Projektils auf die
     * übergebene x-Koordinate
     * @param int xCoordinate
    """
    def setXCoordinate(self, xCoordinate: int):
        self.__xCoordinate = xCoordinate
        pass

    """
     * Diese Methode setzt die y-Koordinate eines Projektils auf die
     * übergebene y-Koordinate
     * @param int yCoordinate
    """
    def setYCoordinate(self, yCoordinate: int):
        self.__yCoordinate = yCoordinate
        pass

    """
     * Diese Methode wird aufgerufen, um ein Projektil um ein Pixel
     * nach links oder rechts zu bewegen.
    """
    def move(self):
        if self.getDirection():
            self.setXCoordinate(self.getXCoordinate() - 1)
        else:
            self.setXCoordinate(self.getXCoordinate() + 1)
        pass
