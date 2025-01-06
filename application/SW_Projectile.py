class SW_Projectile:
    def __init__(self):
        # x-Koordinate
        self.__xCoordinate: int = 0

        # y-Koordinate
        self.__yCoordinate: int = 0

        # Richtungsflag: True = links, False = rechts
        self.__directionLeft: bool = False

        # Validitätsflag: Zeigt an, ob das Projektil aktiv ist
        self.__valid: bool = False

    def getDirection(self) -> bool:
        """
        Gibt die Flugrichtung des Projektils zurück.
        True = links, False = rechts.
        """
        return self.__directionLeft

    def setDirection(self, directionLeft: bool):
        """
        Setzt die Flugrichtung des Projektils.
        True = links, False = rechts.
        """
        self.__directionLeft = directionLeft

    def getValid(self) -> bool:
        """
        Gibt zurück, ob das Projektil aktiv ist.
        """
        return self.__valid

    def setValid(self, valid: bool):
        """
        Setzt das Validitätsflag für das Projektil.
        True = aktiv, False = inaktiv.
        """
        self.__valid = valid

    def getXCoordinate(self) -> int:
        """
        Gibt die x-Koordinate des Projektils zurück.
        """
        return self.__xCoordinate

    def setXCoordinate(self, xCoordinate: int):
        """
        Setzt die x-Koordinate des Projektils.
        """
        self.__xCoordinate = xCoordinate

    def getYCoordinate(self) -> int:
        """
        Gibt die y-Koordinate des Projektils zurück.
        """
        return self.__yCoordinate

    def setYCoordinate(self, yCoordinate: int):
        """
        Setzt die y-Koordinate des Projektils.
        """
        self.__yCoordinate = yCoordinate

    def move(self):
        """
        Bewegt das Projektil um ein Pixel nach links oder rechts,
        abhängig von der gesetzten Flugrichtung.
        """
        if self.getDirection():  # Richtung links
            self.setXCoordinate(self.getXCoordinate() - 1)
        else:  # Richtung rechts
            self.setXCoordinate(self.getXCoordinate() + 1)
