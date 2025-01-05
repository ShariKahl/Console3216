# #include "Arduino.h"
# #include "sprite.h"
import Sprite
# #include "Joystick.h"
import Joystick
# #include "sw_projectileManagement.h"
import SW_ProjectileManagement
# #include "sw_constants.h"
import SW_Constants
# #include "display.h"
import Display
# TODO #include "RgbLed.h"
# #include "sw_projectile.h"
import SW_Projectile

from RgbLed import graphics

class Ship(Sprite.Sprite):
    def __init__(self):
        # TODO Super constructor call
        super().__init__(0, 0, 4, 3)
        # Attribute
        self._shipLives: int = 3
        self._orientation: int = SW_Constants.SHIP_ORIENTATION_LEFT
        self._shipColor: graphics.Color = None
        self._timerTickMove: int = SW_Constants.SHIP_TICK_MOVE
        self._timerTickShot: int = SW_Constants.SHIP_TICK_SHOT
        self._hitBoxOne: int = 0
        self._hitBoxTwo: int = 0
        self._hitBoxThree: int = 0
        self._rightBorder: int = 0
        self._leftBorder: int = 0
        self._upperBorder: int = 0
        self._bottomBorder: int = 0
        self._xPos: int = 0
        self._yPos: int = 0

        # TODO C++: uint8_t shipBorderArray[4];
        self._shipBorderArray = [0 for _ in range(4)]

        # TODO pyserial
        # Serial.println("Constructor called")
        self.activate()

    """
     * Die Methode erzeugt ein spezifisches Projektil​ (siehe Modul ProjectileManagement - getProjectiles)​.
     * @param projectile
    """
    def _shot(self, projectileManagement: SW_ProjectileManagement.ProjectileManagement):
        if self._orientation == 0:
            projectileManagement.shoot(self.getXPos() + 3, self.getYPos() + 1, False)
        else:
            projectileManagement.shoot(self.getXPos() - 1, self.getYPos() + 1, True)
        pass

    """
     * Diese Methode wird bei der Instanziierung und nach jeder Bewegung des Raumschiffes aufgerufen.
     * Sie setzt die Hitboxen auf die abzufragenden Felder der Raumschiffe.
    """
    def _setHitBoxes(self):
        # TODO C++ Source body empty
        pass

    """
     * Diese Methode generiert die Form eines Raumschiffs. Die Form besteht aus einer Anordnung von Einträgen in eine
     * Bitmap. Jeder Eintrag bestimmt ein individuelles Element der Form. Vor dem Aufruf dieser Methode muss die
     * Methode setOrientation() für jede Schiffsinstanz aufgerufen werden.
    """
    def setBitMap(self):
        if self._orientation == 0:
            # TODO pyserial
            # Serial.println("Bitmap LeftShip called")
            self.setPosition(5, 5)
            self._bitmap[0] = self._shipColor
            self._bitmap[1] = Display.Display.getColorFrom565(0x0000)
            self._bitmap[2] = self._shipColor
            self._bitmap[3] = self._shipColor
            self._bitmap[4] = self._shipColor
            self._bitmap[5] = self._shipColor
            self._bitmap[6] = Display.Display.getColorFrom565(0x0000)
            self._bitmap[7] = self._shipColor
            self._bitmap[8] = Display.Display.getColorFrom565(0x0000)
            self._bitmap[9] = Display.Display.getColorFrom565(0x0000)
            self._bitmap[10] = Display.Display.getColorFrom565(0x0000)
            self._bitmap[11] = Display.Display.getColorFrom565(0x0000)
        else:
            # TODO pyserial
            # Serial.println("Bitmap RightShip called");
            self.setPosition(25, 5)
            self._bitmap[0] = Display.Display.getColorFrom565(0x0000)
            self._bitmap[1] = self._shipColor
            self._bitmap[2] = Display.Display.getColorFrom565(0x0000)
            self._bitmap[3] = self._shipColor
            self._bitmap[4] = self._shipColor
            self._bitmap[5] = self._shipColor
            self._bitmap[6] = self._shipColor
            self._bitmap[7] = Display.Display.getColorFrom565(0x0000)
            self._bitmap[8] = self._shipColor
            self._bitmap[9] = Display.Display.getColorFrom565(0x0000)
            self._bitmap[10] = Display.Display.getColorFrom565(0x0000)
            self._bitmap[11] = Display.Display.getColorFrom565(0x0000)
        pass

    """
     * Diese Methode prüft auf eingetretene Kollision mit Projektilen.
     * @param projectile
    """
    def checkHitWithProjectile(self, projectileManagement: SW_ProjectileManagement.ProjectileManagement):
        for i in range(SW_Constants.MAXPROJECTILE * 2):
            # TODO C++ Source used full lookup in every instance
            # Current Projectile
            cp = projectileManagement.getProjectiles(i)

            if cp.getValid():
                if cp.getDirection():
                    # TODO pyserial
                    # Serial.println("Ship Right")
                    # Serial.println(self.getYPos())
                    # Serial.println(self.getXPos())
                    # Serial.println(projectileManagement.getProjectiles(i).getXCoordinate())
                    if (
                        # Erste Zeile
                        ((self.getYPos() == cp.getYCoordinate()) and
                        ((self.getXPos() == cp.getXCoordinate()) or
                        (self.getXPos() + 1 == cp.getXCoordinate()))) or
                        # Zweite Zeile
                        ((self.getYPos() + 1 == cp.getYCoordinate()) and
                        (self.getXPos() == cp.getXCoordinate())) or
                        # Dritte Zeile
                        ((self.getYPos() + 2 == cp.getYCoordinate()) and
                        ((self.getXPos() == cp.getXCoordinate()) or
                        (self.getXPos() + 1 == cp.getXCoordinate())))):
                        # TODO pyserial
                        # Serial.println(self._shipLives)
                        if self.getShipLives() > 0:
                            self._shipLives -= 1
                        # Serial.println(self._shipLives)
                        # TODO Remove reference to current projectile
                        del cp
                        projectileManagement.deleteProjectile(i)
                else:
                    # TODO pyserial
                    # Serial.println("Ship Right")
                    # Serial.println(self.getYPos())
                    # Serial.println(self.getXPos())
                    # Serial.println(projectileManagement.getProjectiles(i).getXCoordinate())
                    if (
                        # Erste Zeile
                        ((self.getYPos() == cp.getYCoordinate()) and
                        ((self.getXPos() + 1 == cp.getXCoordinate()) or
                        (self.getXPos() + 2 == cp.getXCoordinate()))) or
                        # Zweite Zeile
                        ((self.getYPos() + 1 == cp.getYCoordinate()) and
                        (self.getXPos() == cp.getXCoordinate())) or
                        # Dritte Zeile
                        ((self.getYPos() + 2 == cp.getYCoordinate()) and
                        ((self.getXPos() + 1 == cp.getXCoordinate()) or
                        (self.getXPos() + 2 == cp.getXCoordinate())))):
                        if self.getShipLives() > 0:
                            self._shipLives -= 1
                        # TODO Remove reference to current projectile
                        del cp
                        projectileManagement.deleteProjectile(i)
        pass

    """
     * Diese Methode wird von der Spiellogik für jede Schiffsinstanz aufgerufen. Die Orientierung des Joystick`s muss
     * an die Orientierung der Schiffsinstanz angepasst werden. Die Methode benötigt für die Erzeugung einen Parameter
     * der die Funktionalität bietet die Projektil Listen aufzurufen (siehe Modul ProjectileManagement - getProjectiles).
     * @param joystick
     * @param projectile (optional)
     * @param projectileManagement (optional)

     TODO Method was marked as TODO in C++ Source
    """
    def moveShipAndShot(self, joystick: Joystick.Joystick, projectileManagement: SW_ProjectileManagement.ProjectileManagement):
        if (((self._orientation == 0) and joystick.isLeft() and (self.getXPos() > SW_Constants.SHIP_LEFT_LEFT_BORDER)) or
            ((self._orientation != 0) and joystick.isLeft() and (self.getXPos() > SW_Constants.SHIP_RIGHT_LEFT_BORDER))):
            if self._timerTickMove == 0:
                self.move(-1, 0)
                self._timerTickMove = SW_Constants.SHIP_TICK_MOVE + 1
                # Serial.println("Move left")
        elif (((self._orientation == 0) and joystick.isUp() and (self.getYPos() > SW_Constants.SHIP_LEFT_UPPER_BORDER)) or
            ((self._orientation != 0) and joystick.isUp() and (self.getYPos() > SW_Constants.SHIP_RIGHT_UPPER_BORDER))):
            if self._timerTickMove == 0:
                self.move(0, -1)
                self._timerTickMove = SW_Constants.SHIP_TICK_MOVE + 1
                # Serial.println("Move up")
        elif (((self._orientation == 0) and joystick.isRight() and (self.getXPos() < SW_Constants.SHIP_LEFT_RIGHT_BORDER - 2)) or
            ((self._orientation != 0) and joystick.isRight() and (self.getXPos() < SW_Constants.SHIP_RIGHT_RIGHT_BORDER - 2))):
            if self._timerTickMove == 0:
                self.move(1, 0)
                self._timerTickMove = SW_Constants.SHIP_TICK_MOVE + 1
                # Serial.println("Move right")
        elif (((self._orientation == 0) and joystick.isDown() and (self.getYPos() < SW_Constants.SHIP_LEFT_BOTTOM_BORDER - 2)) or
            ((self._orientation != 0) and joystick.isDown() and (self.getYPos() < SW_Constants.SHIP_RIGHT_BOTTOM_BORDER - 2))): # TODO C++ Source checked SHIP_LEFT_BOTTOM_BORDER, assuming Bug
            if self._timerTickMove == 0:
                self.move(0, 1)
                self._timerTickMove = SW_Constants.SHIP_TICK_MOVE + 1
                # Serial.println("Move down")
        
        if ((joystick.getControlStatus(Joystick.JOYSTICK_SWITCH_BUTTON_TOP) == Joystick.JOYSTICK_STATUS_PRESSED) or
            (joystick.getControlStatus(Joystick.JOYSTICK_SWITCH_BUTTON_BODY) == Joystick.JOYSTICK_STATUS_PRESSED)):
            if self._timerTickShot == 0:
                self._shot(projectileManagement)
                self._timerTickShot = SW_Constants.SHIP_TICK_SHOT + 1
        
        if self._timerTickMove > 0:
            self._timerTickMove -= 1
        if self._timerTickShot > 0:
            self._timerTickShot -= 1
        pass

    """
     * Die Methode reduziert die verbleibende Anzahl des Spielerlebens um Eins.
    """
    def decrementShipLives(self):
        self._shipLives -= 1
        pass

    """
     * Diese Methode setzt die Orientierung / Spielfeldseite eines Raumschiffes.
     * @param orientation
    """
    def setOrientation(self, orientation: int):
        self._orientation = orientation;
        if orientation == 0:
            self._shipBorderArray[0] = SW_Constants.SHIP_LEFT_RIGHT_BORDER
            self._shipBorderArray[1] = SW_Constants.SHIP_LEFT_LEFT_BORDER
            self._shipBorderArray[2] = SW_Constants.SHIP_LEFT_UPPER_BORDER
            self._shipBorderArray[3] = SW_Constants.SHIP_LEFT_BOTTOM_BORDER
            self._xPos = SW_Constants.SHIP_LEFT_LEFT_BORDER
            self._yPos = (SW_Constants.SHIP_LEFT_BOTTOM_BORDER + SW_Constants.SHIP_LEFT_UPPER_BORDER) / 2
        else:
            self._shipBorderArray[0] = SW_Constants.SHIP_RIGHT_RIGHT_BORDER
            self._shipBorderArray[1] = SW_Constants.SHIP_RIGHT_LEFT_BORDER
            self._shipBorderArray[2] = SW_Constants.SHIP_RIGHT_UPPER_BORDER
            self._shipBorderArray[3] = SW_Constants.SHIP_RIGHT_BOTTOM_BORDER
            self._xPos = SW_Constants.SHIP_RIGHT_RIGHT_BORDER
            self._yPos = (SW_Constants.SHIP_RIGHT_BOTTOM_BORDER + SW_Constants.SHIP_RIGHT_UPPER_BORDER) / 2
        pass

    """
     * Diese Methode gibt die Orientierung / Spielfeldseite eines Raumschiffes zurück.
     * @return uint8_t orientation
    """
    def getOrientation(self) -> int:
        return self._orientation

    """
     * Diese Methode ändert die Farbe aller Pixel eines Raumschiffes.
     * @param color
    """
    def setShipColor(self, color: graphics.Color):
        self._shipColor = color
        pass

    """
     * Mit dieser Methode kann jeder Pixel des Raumschiffs separat verändert werden. Durch einen Indexzugriff auf das
     * Feld des Pixels und ein Indexzugriff auf die Farbe kann auf einen Pixel zugegriffen werden.
     * @param pixel
     * @param color
    """
    # TODO C++: void setShipPixelColor(uint8_t *pixel, uint16_t *color);
    def setShipPixelColor(self, pixel: int, color: int):
        # TODO C++ Source body empty
        pass

    """
     * Mit dieser Methode kann der Default-Tickwert der Bewegung verändert werden.
     * @param tickValue
    """
    def setTickMoveDefault(self, tickValue: int):
        # TODO C++ Source provided no definition
        pass

    """
     * Diese Methode setzt die Anzahl der Leben eines Schiffes (Spielerleben).
     * @param livesValue
    """
    def setShipLives(self, livesValue: int):
        self._shipLives = livesValue
        pass

    """
     * Diese Methode liefert die derzeitige Anzahl der Leben eines Schiffs (Spielerleben) zurück.
     * @return uint8_t shipLives
    """
    def getShipLives(self) -> int:
        return self._shipLives

    """
     * Mit dieser Methode kann der Default-Tickwert der Schusshäufigkeit verändert werden.
     * @param tickValue
    """
    def setTickShotDefault(self, tickValue: int):
        # TODO C++ Source provided no definition
        pass

    """
     * Diese Methode gibt den Default-Tickwert der Bewegung des Raumschiffes zurück.
     * @return uint8_t TickMoveDefault
    """
    def getTickMoveDefault(self) -> int:
        # TODO C++ Source provided no definition
        pass

    """
     * Diese Methode liefert die Spielfeldgrenzen als Array zurück.
     * @return unit8_t 4 int-Werte für die Grenzen.
    """
    # TODO C++: uint8_t *getBorderRightLeftUpperBottom(void);
    def getBorderRightLeftUpperBottom(self) -> int:
        return self._shipBorderArray

    """
    /**
     * Diese Methode setzt anhand der Parameter die Spielfeldgrenzen eines Spielers. Diese Methode wird bei der
     * Initialisierung der Schiffsinstanzen aufgerufen und setzt die Grenzen auf die Größe der Konsole.
     * @param right
     * @param left
     * @param upper
     * @param bottom
     */
    """
    def setBorderRightLeftUpperBottom(self, right: int, left: int, upper: int, bottom: int):
        self._shipBorderArray[0] = right
        self._shipBorderArray[1] = left
        self._shipBorderArray[2] = upper
        self._shipBorderArray[3] = bottom
        pass
