# #include "sw_constants.h"
import SW_Constants
# #include "sw_projectile.h"
import SW_Projectile
# #include <display.h>
import Display


class ProjectileManagement:
    def __init__(self):
        # Array of projectiles
        # TODO C++: SW_Projectile projectile[2*MAXPROJECTILE];
        self.__projectile = [None for _ in range(SW_Constants.MAXPROJECTILE * 2)]

        self.__tickMoveProjectiles: int = 0

        for i in range(2 * SW_Constants.MAXPROJECTILE):
            self.__projectile[i] = SW_Projectile.SW_Projectile()

    """
     * Diese Methode liefert eine Liste mit allen auf dem Spielfeld aktiven Projektilen.
    """
    def getProjectiles(self, index: int) -> SW_Projectile.SW_Projectile:
        return self.__projectile[index]

    """
     * Diese Methode wird von der Spiellogik aufgerufen, um die Rahmenbedingung der Projektile
     * zu prüfen. Die Projektile werden nacheinander mit Hilfe von Projectile::move() bewegt.
     * Zwischen jeder Bewegung eines Projektils wird mittels checkCollision() geprüft ob eine
     * Kollision aufgetreten ist. Sollte eine Kollision aufgetreten sein wird, mit Hilfe der
     * deleteProjectile() Methode, jedes kollidierte Projektil gelöscht.
    """
    def manageProjectiles(self):
        # TODO C++ Source:
        # for(uint8_t i = 0; i < (2 * MAXPROJECTILE) && this->tickMoveProjectiles == 0; i++) {...}
        for i in range(2 * SW_Constants.MAXPROJECTILE):
            if self.__tickMoveProjectiles != 0:
                break
            self.__projectile[i].move()
        
        if self.__tickMoveProjectiles > 0:
            self.__tickMoveProjectiles -= 1
        else:
            self.__tickMoveProjectiles = SW_Constants.TICK_MOVE_PROJECTILES_DEFAULT
        pass

    """
     * Diese Methode wird von den Raumschiffen aufgerufen, wenn diese ein Projektil abfeuern.
     * Diese Methode erzeugt ein Projektil und fügt es in die Liste der Projektile ein. Sie benötigt
     * als Übergabeparameter die Richtung und die X / Y Koordinaten des Projektils.
     * Die Koordinaten referenzieren die Abschussposition des Projektils auf dem Spielfeld. Das
     * Richtungsflag gibt an, ob sich das Projektil nach links (directionLeft = true) oder rechts
     * (directionLeft = false) bewegt.
     * @param x
     * @param y
     * @param directionLeft
    """
    def shoot(self, x: int, y: int, directionLeft: bool):
        max: int = SW_Constants.MAXPROJECTILE
        i: int = 0

        if directionLeft:
            i = SW_Constants.MAXPROJECTILE
            max = 2 * SW_Constants.MAXPROJECTILE
        
        for j in range(i, max):
            if not self.__projectile[j].getValid():
                self.__projectile[j].setDirection(directionLeft)
                self.__projectile[j].setXCoordinate(x)
                self.__projectile[j].setYCoordinate(y)
                self.__projectile[j].setValid(True)
                break
        pass

    """
     * Diese Methode löscht ein Projektil.
     * Diese Methode wird einerseits von den Raumschiffen aufgerufen, wenn sie von einem
     * Projektil getroffen wurden, als auch von ProjectileManagement, wenn zwei Projektile
     * kollidieren.
     * @param projectileID
    """
    def deleteProjectile(self, projectileID: int):
        self.__projectile[projectileID].setValid(False)
        pass

    """
     *  Diese Methode prüft auf Kollisionen zwischen Projektilen.
    """
    def checkCollision(self):
        # Kollision mit Projektil
        for i in range(SW_Constants.MAXPROJECTILE):
            if self.__projectile[i].getValid():
                for j in range(SW_Constants.MAXPROJECTILE, SW_Constants.MAXPROJECTILE * 2):
                    if self.__projectile[j].getYCoordinate() == self.__projectile[j].getYCoordinate():
                        if (self.__projectile[i].getXCoordinate() + 1 == self.__projectile[j].getXCoordinate()) or (self.__projectile[i].getXCoordinate() == self.__projectile[j].getXCoordinate()):
                            self.deleteProjectile(i)
                            self.deleteProjectile(j)
        pass

    """
     *  Diese Methode prüft auf Kollisionen mit der Wand.
    """
    def checkBoundaries(self):
        # Kollision mit der Wand
        for i in range(SW_Constants.MAXPROJECTILE):
            if self.__projectile[i].getValid():
                if self.__projectile[i].getXCoordinate() >= SW_Constants.FIELD_RIGHT_BORDER:
                    self.deleteProjectile(i)
        
        for i in range(SW_Constants.MAXPROJECTILE, SW_Constants.MAXPROJECTILE * 2):
            if self.__projectile[i].getValid():
                if self.__projectile[i].getXCoordinate() == SW_Constants.FIELD_LEFT_BORDER:
                    self.deleteProjectile(i)
        pass

    def draw(self):
        for i in range(SW_Constants.MAXPROJECTILE * 2):
            if self.__projectile[i].getValid():
                if self.__projectile[i].getDirection():
                    Display.Display.drawPixel(self.__projectile[i].getXCoordinate(), self.__projectile[i].getYCoordinate(), Display.Display.getColorFrom333(0, 7, 0))
                else:
                    Display.Display.drawPixel(self.__projectile[i].getXCoordinate(), self.__projectile[i].getYCoordinate(), Display.Display.getColorFrom333(7, 0, 0))
        
        if self.__tickMoveProjectiles == SW_Constants.TICK_MOVE_PROJECTILES_DEFAULT:
            self.checkCollision()
            self.checkBoundaries()
        pass
