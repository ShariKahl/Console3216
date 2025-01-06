import SW_Constants
import SW_Projectile
import Display

class ProjectileManagement:
    def __init__(self):
        # Liste der Projektile (maximal 2 * MAXPROJECTILE)
        self.__projectile = [SW_Projectile.SW_Projectile() for _ in range(SW_Constants.MAXPROJECTILE * 2)]

        # Tick-Variable für das Bewegen der Projektile
        self.__tickMoveProjectiles: int = 0

    def getProjectiles(self, index: int) -> SW_Projectile.SW_Projectile:
        """
        Gibt das Projektil am angegebenen Index zurück.
        """
        return self.__projectile[index]

    def manageProjectiles(self):
        """
        Bewegt die Projektile und prüft nach jeder Bewegung, ob Kollisionen aufgetreten sind.
        """
        # Wenn der Tick nicht Null ist, beende die Bewegung
        if self.__tickMoveProjectiles != 0:
            return
        
        # Bewege alle Projektile
        for i in range(2 * SW_Constants.MAXPROJECTILE):
            self.__projectile[i].move()

        # Kollision und Grenzen prüfen
        self.checkCollision()
        self.checkBoundaries()

        # Tick-Management für Projektile
        if self.__tickMoveProjectiles > 0:
            self.__tickMoveProjectiles -= 1
        else:
            self.__tickMoveProjectiles = SW_Constants.TICK_MOVE_PROJECTILES_DEFAULT

    def shoot(self, x: int, y: int, directionLeft: bool):
        """
        Erzeugt ein neues Projektil und fügt es der Liste hinzu.
        """
        # Bestimmen, welches Projektil frei ist und in die Liste einfügen
        max_index = SW_Constants.MAXPROJECTILE * 2 if directionLeft else SW_Constants.MAXPROJECTILE
        for i in range(max_index):
            if not self.__projectile[i].getValid():
                self.__projectile[i].setDirection(directionLeft)
                self.__projectile[i].setXCoordinate(x)
                self.__projectile[i].setYCoordinate(y)
                self.__projectile[i].setValid(True)
                break

    def deleteProjectile(self, projectileID: int):
        """
        Löscht das Projektil an der gegebenen ID.
        """
        self.__projectile[projectileID].setValid(False)

    def checkCollision(self):
        """
        Prüft auf Kollisionen zwischen den Projektilen.
        """
        for i in range(SW_Constants.MAXPROJECTILE):
            if self.__projectile[i].getValid():
                for j in range(SW_Constants.MAXPROJECTILE, 2 * SW_Constants.MAXPROJECTILE):
                    # Prüft, ob X und Y-Koordinaten übereinstimmen
                    if self.__projectile[i].getXCoordinate() == self.__projectile[j].getXCoordinate() and \
                            self.__projectile[i].getYCoordinate() == self.__projectile[j].getYCoordinate():
                        self.deleteProjectile(i)
                        self.deleteProjectile(j)

    def checkBoundaries(self):
        """
        Prüft, ob die Projektile die Spielfeldgrenzen überschreiten.
        """
        for i in range(SW_Constants.MAXPROJECTILE):
            if self.__projectile[i].getValid():
                if self.__projectile[i].getXCoordinate() >= SW_Constants.FIELD_RIGHT_BORDER:
                    self.deleteProjectile(i)

        for i in range(SW_Constants.MAXPROJECTILE, 2 * SW_Constants.MAXPROJECTILE):
            if self.__projectile[i].getValid():
                if self.__projectile[i].getXCoordinate() <= SW_Constants.FIELD_LEFT_BORDER:
                    self.deleteProjectile(i)

    def draw(self):
        """
        Zeichnet alle aktiven Projektile auf dem Display.
        """
        for i in range(SW_Constants.MAXPROJECTILE * 2):
            if self.__projectile[i].getValid():
                if self.__projectile[i].getDirection():
                    # Projektil nach links
                    Display.Display.drawPixel(self.__projectile[i].getXCoordinate(), self.__projectile[i].getYCoordinate(), Display.Display.getColorFrom333(0, 7, 0))
                else:
                    # Projektil nach rechts
                    Display.Display.drawPixel(self.__projectile[i].getXCoordinate(), self.__projectile[i].getYCoordinate(), Display.Display.getColorFrom333(7, 0, 0))

        # Nachdem die Projektile bewegt wurden, Kollision und Grenzen prüfen
        if self.__tickMoveProjectiles == SW_Constants.TICK_MOVE_PROJECTILES_DEFAULT:
            self.checkCollision()
            self.checkBoundaries()
