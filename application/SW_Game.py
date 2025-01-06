# #include "game.h"
import Game
# #include "Joystick.h"
import Joystick
# #include "sw_constants.h"
import SW_Constants
# #include <display.h>
import Display
# #include <sine.h>
import Sine
# #include "sw_ship.h"
import SW_Ship
# #include "sw_projectileManagement.h"
import SW_ProjectileManagement
# #include "SpaceSounds.h"
import SpaceSounds

import NumericDisplay

from rgbmatrix import graphics


class Space_Wars(Game.Game):
    def __init__(self, leftJoystick: Joystick.Joystick, rightJoystick: Joystick.Joystick):
        super().__init__(leftJoystick, rightJoystick, "SWAR")

        # Farben und Spielstatus initialisieren
        self._textColor: graphics.Color = Display.Display.getColorFrom333(0, 2, 5)
        self._middleBorderColor: graphics.Color = Display.Display.getColorFrom565(0xFFFF)
        self._currentState: int = SW_Constants.STATE_DEMO
        self._gameFinish: bool = False

        # Sounds und Projektile initialisieren
        self._sounds: SpaceSounds.SpaceSounds = SpaceSounds.SpaceSounds()
        self._projectileManagement: SW_ProjectileManagement.ProjectileManagement = SW_ProjectileManagement.ProjectileManagement()

        # Schiffe initialisieren
        self._shipLeft: SW_Ship.Ship = SW_Ship.Ship()
        self._shipRight: SW_Ship.Ship = SW_Ship.Ship()

        # Neustart und Setup
        self._restart()

        NumericDisplay.NumericDisplay.test()
        self._timeStart()

        # Schiffe konfigurieren
        self._shipLeft.setShipColor(Display.Display.getColorFrom565(0xFFFF))
        self._shipLeft.setOrientation(SW_Constants.SHIP_LEFT)
        self._shipLeft.setBitMap()

        self._shipRight.setShipColor(Display.Display.getColorFrom565(0xFFFF))
        self._shipRight.setOrientation(SW_Constants.SHIP_RIGHT)
        self._shipRight.setBitMap()

    def play(self) -> None:
        """Die Hauptspiel-Logik."""
        self._shipLeft.moveShipAndShot(self._joystickLeft, self._projectileManagement)
        self._shipRight.moveShipAndShot(self._joystickRight, self._projectileManagement)
        self._projectileManagement.manageProjectiles()
        self._shipLeft.checkHitWithProjectile(self._projectileManagement)
        self._shipRight.checkHitWithProjectile(self._projectileManagement)

    def draw(self, state: int) -> None:
        """Zeichnet den aktuellen Spielzustand."""
        Display.Display.clearDisplay()

        if state == SW_Constants.STATE_DEMO:
            Display.Display.drawText(self._name, 4, 4, self._textColor, 1)
        elif state == SW_Constants.STATE_PLAY:
            self._shipLeft.draw()
            self._shipRight.draw()
            self._projectileManagement.draw()
            self._drawMiddleBorder()
        elif state == SW_Constants.STATE_SHOW_WINNER:
            if self._shipLeft.getShipLives() == 0:
                Display.Display.drawText("P2", 4, 0, self._textColor, 1)
                Display.Display.drawText("WIN", 4, 8, self._textColor, 1)
            if self._shipRight.getShipLives() == 0:
                Display.Display.drawText("P1", 4, 0, self._textColor, 1)
                Display.Display.drawText("WIN", 4, 8, self._textColor, 1)
            self._gameFinish = True

        NumericDisplay.NumericDisplay.displayTime(NumericDisplay.DISPLAY_MIDDLE, self._time / 1000)
        Display.Display.refresh()

    def prepareDemo(self) -> None:
        """Vorbereitung der Demo."""
        self._shipLeft.setShipLives(3)
        self._shipRight.setShipLives(3)
        self._currentState = SW_Constants.STATE_PLAY
        self._player1Type = Game.PLAYER_TYPE_HUMAN
        self._player2Type = Game.PLAYER_TYPE_HUMAN
        self._gameFinish = False

    def playDemo(self) -> None:
        """Spielt die Demo ab."""
        self.prepareDemo()
        self.demo()
        self.draw(SW_Constants.STATE_DEMO)
        self._currentState = SW_Constants.STATE_PLAY

    def playGame(self) -> None:
        """Spielt das eigentliche Spiel."""
        self.play()
        self.draw(self._currentState)

    def process(self) -> None:
        """Verarbeitet den aktuellen Zustand des Spiels."""
        super().process()
        NumericDisplay.NumericDisplay.displayValue(NumericDisplay.DISPLAY_LEFT, self._shipLeft.getShipLives())
        NumericDisplay.NumericDisplay.displayValue(NumericDisplay.DISPLAY_RIGHT, self._shipRight.getShipLives())

        if (self._shipLeft.getShipLives() == 0) or (self._shipRight.getShipLives() == 0):
            self._currentState = SW_Constants.STATE_SHOW_WINNER

        if self._gameFinish and (self._joystickLeft.isButtonTop() or
                                 self._joystickLeft.isButtonBody() or
                                 self._joystickRight.isButtonTop() or
                                 self._joystickRight.isButtonBody()):
            self._state = Game.GAME_STATE_END

    def demo(self) -> None:
        """Zeigt eine Demo des Spiels (noch leer)."""
        pass

    def playSound(self, soundType: str) -> None:
        """Spielt Sounds basierend auf dem Typ ab."""
        if soundType == "shot":
            self._sounds.playSoundShipShot()
        elif soundType == "collision":
            self._sounds.playSoundProjectileCollision()
        elif soundType == "hit":
            self._sounds.playSoundShipHasBeenHit()

    def _drawMiddleBorder(self) -> None:
        """Zeichnet die Grenze in der Mitte des Spielfelds."""
        for i in range(16):
            if i % 2 == 0:
                Display.Display.drawPixel(SW_Constants.SHIP_LEFT_RIGHT_BORDER + 1, i, self._middleBorderColor)
            else:
                Display.Display.drawPixel(SW_Constants.SHIP_RIGHT_LEFT_BORDER - 1, i, self._middleBorderColor)

    def _restart(self) -> None:
        """Setzt das Spiel zurück."""
        self._shipLeft.setShipLives(3)
        self._shipRight.setShipLives(3)
        self._timeStart()

    def _callTestMethod(self) -> None:
        """Testmethode für interne Funktionalitäten."""
        checkCollision: bool = False
        xLeft: int = 0
        yLeft: int = 0
        xRight: int = 30
        yRight: int = 0

        self._projectileManagement.shoot(xLeft, yLeft, False)
        self._projectileManagement.shoot(xRight, yRight, True)
        self._projectileManagement.manageProjectiles()

        if yLeft == SW_Constants.BORDER_BOTTOM:
            self.playSound("shot")
            yLeft = 0
        else:
            yLeft += 1

        if yRight == SW_Constants.BORDER_BOTTOM:
            yRight = 0
            checkCollision = not checkCollision
        else:
            yRight += 1
