import Sprite
import Joystick
import SW_ProjectileManagement
import SW_Constants
import Display
from RgbLed import graphics

class Ship(Sprite.Sprite):
    def __init__(self):
        super().__init__(0, 0, 4, 3)
        # Initialisierung der Attribute
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

        # Initialisierung des ShipBorders
        self._shipBorderArray = [0 for _ in range(4)]

        self.activate()

    def _shot(self, projectileManagement: SW_ProjectileManagement.ProjectileManagement):
        """Erzeugt ein Projektil basierend auf der Orientierung des Schiffs."""
        if self._orientation == 0:
            projectileManagement.shoot(self.getXPos() + 3, self.getYPos() + 1, False)
        else:
            projectileManagement.shoot(self.getXPos() - 1, self.getYPos() + 1, True)

    def _setHitBoxes(self):
        """Setzt die Hitboxen des Schiffs (falls erforderlich)."""
        pass

    def setBitMap(self):
        """Setzt die Bitmap des Schiffs basierend auf der Orientierung."""
        if self._orientation == 0:
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

    def checkHitWithProjectile(self, projectileManagement: SW_ProjectileManagement.ProjectileManagement):
        """Prüft, ob das Schiff von einem Projektil getroffen wurde."""
        for i in range(SW_Constants.MAXPROJECTILE * 2):
            cp = projectileManagement.getProjectiles(i)

            if cp.getValid():
                if cp.getDirection():
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
                        if self.getShipLives() > 0:
                            self._shipLives -= 1
                        # Lösche das Projektil nach dem Treffer
                        del cp
                        projectileManagement.deleteProjectile(i)
                else:
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
                        # Lösche das Projektil nach dem Treffer
                        del cp
                        projectileManagement.deleteProjectile(i)

    def moveShipAndShot(self, joystick: Joystick.Joystick, projectileManagement: SW_ProjectileManagement.ProjectileManagement):
        """Bewegt das Schiff und feuert ein Projektil ab, wenn der Joystick entsprechend betätigt wird."""
        if (((self._orientation == 0) and joystick.isLeft() and (self.getXPos() > SW_Constants.SHIP_LEFT_LEFT_BORDER)) or
            ((self._orientation != 0) and joystick.isLeft() and (self.getXPos() > SW_Constants.SHIP_RIGHT_LEFT_BORDER))):
            if self._timerTickMove == 0:
                self.move(-1, 0)
                self._timerTickMove = SW_Constants.SHIP_TICK_MOVE + 1
        elif (((self._orientation == 0) and joystick.isUp() and (self.getYPos() > SW_Constants.SHIP_LEFT_UPPER_BORDER)) or
            ((self._orientation != 0) and joystick.isUp() and (self.getYPos() > SW_Constants.SHIP_RIGHT_UPPER_BORDER))):
            if self._timerTickMove == 0:
                self.move(0, -1)
                self._timerTickMove = SW_Constants.SHIP_TICK_MOVE + 1
        elif (((self._orientation == 0) and joystick.isRight() and (self.getXPos() < SW_Constants.SHIP_LEFT_RIGHT_BORDER - 2)) or
            ((self._orientation != 0) and joystick.isRight() and (self.getXPos() < SW_Constants.SHIP_RIGHT_RIGHT_BORDER - 2))):
            if self._timerTickMove == 0:
                self.move(1, 0)
                self._timerTickMove = SW_Constants.SHIP_TICK_MOVE + 1
        elif (((self._orientation == 0) and joystick.isDown() and (self.getYPos() < SW_Constants.SHIP_LEFT_BOTTOM_BORDER - 2)) or
            ((self._orientation != 0) and joystick.isDown() and (self.getYPos() < SW_Constants.SHIP_RIGHT_BOTTOM_BORDER - 2))):
            if self._timerTickMove == 0:
                self.move(0, 1)
                self._timerTickMove = SW_Constants.SHIP_TICK_MOVE + 1
        
        if ((joystick.getControlStatus(Joystick.JOYSTICK_SWITCH_BUTTON_TOP) == Joystick.JOYSTICK_STATUS_PRESSED) or
            (joystick.getControlStatus(Joystick.JOYSTICK_SWITCH_BUTTON_BODY) == Joystick.JOYSTICK_STATUS_PRESSED)):
            if self._timerTickShot == 0:
                self._shot(projectileManagement)
                self._timerTickShot = SW_Constants.SHIP_TICK_SHOT + 1
        
        if self._timerTickMove > 0:
            self._timerTickMove -= 1
        if self._timerTickShot > 0:
            self._timerTickShot -= 1

    def decrementShipLives(self):
        """Verringert die Leben des Schiffs um 1."""
        self._shipLives -= 1

    def setOrientation(self, orientation: int):
        """Setzt die Orientierung des Schiffs (links oder rechts)."""
        self._orientation = orientation
        if orientation == 0:
            self._shipBorderArray[0] = SW_Constants.SHIP_LEFT_RIGHT_BORDER
            self._shipBorderArray[1] = SW_Constants.SHIP_LEFT_LEFT_BORDER
            self._shipBorderArray[2] = SW_Constants.SHIP_LEFT_UPPER_BORDER
            self._shipBorderArray[3] = SW_Constants.SHIP_LEFT_BOTTOM_BORDER
            self._xPos = SW_Constants.SHIP_LEFT_LEFT_BORDER
            self._yPos = (SW_Constants.SHIP_LEFT_BOTTOM_BORDER + SW_Constants.SHIP_LEFT_UPPER_BORDER) // 2
        else:
            self._shipBorderArray[0] = SW_Constants.SHIP_RIGHT_RIGHT_BORDER
            self._shipBorderArray[1] = SW_Constants.SHIP_RIGHT_LEFT_BORDER
            self._shipBorderArray[2] = SW_Constants.SHIP_RIGHT_UPPER_BORDER
            self._shipBorderArray[3] = SW_Constants.SHIP_RIGHT_BOTTOM_BORDER
            self._xPos = SW_Constants.SHIP_RIGHT_RIGHT_BORDER
            self._yPos = (SW_Constants.SHIP_RIGHT_BOTTOM_BORDER + SW_Constants.SHIP_RIGHT_UPPER_BORDER) // 2

    def getOrientation(self) -> int:
        """Gibt die Orientierung des Schiffs zurück."""
        return self._orientation

    def setShipColor(self, color: graphics.Color):
        """Setzt die Farbe des Schiffs."""
        self._shipColor = color

    def getShipLives(self) -> int:
        """Gibt die verbleibenden Leben des Schiffs zurück."""
        return self._shipLives
