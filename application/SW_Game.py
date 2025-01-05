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
        # TODO Super constructor call
        super().__init__(leftJoystick, rightJoystick, "SWAR")
        # TODO
        self._textColor: graphics.Color = Display.Display.getColorFrom333(0, 2, 5)
        self._middleBorderColor: graphics.Color = Display.Display.getColorFrom565(0xFFFF)

        self._currentState: int = SW_Constants.STATE_DEMO

        self._gameFinish: bool = False

        self._sounds: SpaceSounds.SpaceSounds = None

        self._projectileManagement: SW_ProjectileManagement.ProjectileManagement = None

        self._shipLeft: SW_Ship.Ship = None
        self._shipRight: SW_Ship.Ship = None

        self._restart()

        NumericDisplay.NumericDisplay.test()

        self._timeStart()

        # Comment from C++ source:
        # Here you have to initialize important variables for your ships
        self._shipLeft.setShipColor(Display.Display.getColorFrom565(0xFFFF))
        self._shipLeft.setOrientation(SW_Constants.SHIP_LEFT)
        self._shipLeft.setBitMap()

        self._shipRight.setShipColor(Display.Display.getColorFrom565(0xFFFF))
        self._shipRight.setOrientation(SW_Constants.SHIP_RIGHT)
        self._shipRight.setBitMap()

    def play(self):
        # /* The Game-Logic will be placed here. */
        self._shipLeft.moveShipAndShot(self._joystickLeft, self._projectileManagement)
        self._shipRight.moveShipAndShot(self._joystickRight, self._projectileManagement)
        self._projectileManagement.manageProjectiles()
        self._shipLeft.checkHitWithProjectile(self._projectileManagement)
        self._shipRight.checkHitWithProjectile(self._projectileManagement)
        pass

    def draw(self, state: int):
        Display.Display.clearDisplay()

        if state == SW_Constants.STATE_DEMO:
            Display.Display.drawText(self._name, 4, 4, self._textColor, 1)
        elif state == SW_Constants.STATE_PLAY:
            # /* Something you want to draw in game mode only */
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

        # /* We will call the draw methods from ships and proteciles here */

        Display.Display.refresh()
        pass

    def prepareDemo(self):
        self._shipLeft.setShipLives(3)
        self._shipRight.setShipLives(3)
        self._currentState = SW_Constants.STATE_PLAY

        self._player1Type = Game.PLAYER_TYPE_HUMAN
        self._player2Type = Game.PLAYER_TYPE_HUMAN

        self._gameFinish = False
        pass

    def playDemo(self):
        self._shipLeft.setShipLives(3)
        self._shipRight.setShipLives(3)
        self._currentState = SW_Constants.STATE_PLAY
        self._gameFinish = False

        self.demo()

        self.draw(SW_Constants.STATE_DEMO)
        self._currentState = SW_Constants.STATE_PLAY
        pass

    def playGame(self):
        self.play()
        self.draw(self._currentState)
        pass

    def process(self):
        super().process()
        NumericDisplay.NumericDisplay.displayValue(NumericDisplay.DISPLAY_LEFT, self._shipLeft.getShipLives())
        NumericDisplay.NumericDisplay.displayValue(NumericDisplay.DISPLAY_RIGHT, self._shipRight.getShipLives())
        # Abfrage auf Spielende
        if (self._shipLeft.getShipLives() == 0) or (self._shipRight.getShipLives() == 0):
            self._currentState = SW_Constants.STATE_SHOW_WINNER
        
        if self._gameFinish and (self._joystickLeft.isButtonTop() or
                                 self._joystickLeft.isButtonBody() or
                                 self._joystickRight.isButtonTop() or
                                 self._joystickRight.isButtonBody()):
            self._state = SW_Constants.GAME_STATE_END
        pass

    def demo(self):
        # /* Here we want to show a little clip that shows how the game will be played */
        pass

    def playSoundShot(self):
        self._sounds.SpaceSounds.playSoundShipShot()
        pass

    def playSoundCollision(self):
        self._sounds.SpaceSounds.playSoundProjectileCollision()
        pass

    # TODO No function definition in C++ Source
    def _drawField(self):
        pass

    def _drawMiddleBorder(self):
        for i in range(16):
            if i % 2 == 0:
                Display.Display.drawPixel(SW_Constants.SHIP_LEFT_RIGHT_BORDER + 1, i, self._middleBorderColor)
            else:
                Display.Display.drawPixel(SW_Constants.SHIP_RIGHT_LEFT_BORDER - 1, i, self._middleBorderColor)
        pass

    def _restart(self):
        self._shipLeft.setShipLives(3)
        self._shipRight.setShipLives(3)
        self._timeStart()
        pass

    def _callTestMethod(self):
        # /* place your test-code here */
        # /* this->shipLeft.moveShipAndShot(this->joystickLeft);
        # this->shipRight.moveShipAndShot(this->joystickRight);*/

        # TODO C++ Source had static variables:
        # static bool checkCollision = false;

        # static uint8_t xLeft = 0;
        # static uint8_t yLeft = 0;

        # static uint8_t xRight = 30;
        # static uint8_t yRight = 0;
        checkCollision: bool = False

        xLeft: int = 0
        yLeft: int = 0

        xRight: int = 30
        yRight: int = 0

        self._projectileManagement.shoot(xLeft, yLeft, False)

        self._projectileManagement.shoot(xRight, yRight, True)
        self._projectileManagement.manageProjectiles()

        if yLeft == SW_Constants.BORDER_BOTTOM:
            self._sounds.SpaceSounds.playSoundShipShot()
            # self._sounds.playSoundShipMove()
            # self._sounds.playSoundShipHasBeenHit()
            # self._sounds.playSoundShipShot()
            yLeft = 0
        else:
            yLeft += 1
        
        if yRight == SW_Constants.BORDER_BOTTOM:
            yRight = 0
            checkCollision = not checkCollision
        else:
            yRight += 1
        pass
