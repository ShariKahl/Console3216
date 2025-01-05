import random

# #include "game.h"
import Game

# #include "pong_ball.h"
from Pong_ball import Ball
# #include "pong_paddle.h"
import Pong_Paddle
# #include "Joystick.h"
import Joystick

import Display
import NumericDisplay
import Sine
import Sound

from rgbmatrix import graphics

EVENT_NONE: int = 0
EVENT_PLAYER_LEFT_POINT: int = 1
EVENT_PLAYER_RIGHT_POINT: int = 2
EVENT_BOUNCE_TOP: int = 3
EVENT_BOUNCE_BOTTOM: int = 4
BALL_SPEED_INCREASE_FACTOR: int = 150

# C++ Source had typo: PADLE_SOUND_EFFECT_
PADDLE_SOUND_EFFECT_LEFT: int = 35
PADDLE_SOUND_EFFECT_RIGHT: int = 36

# TODO
aa: int = 0


class Pong(Game):
    def __init__(self, leftJoystick: Joystick.Joystick, rightJoystick: Joystick.Joystick):
        # TODO Super constructor call
        super().__init__(leftJoystick, rightJoystick, "PONG")

        self._ball: Ball = None
        self._paddleLeft: Pong_Paddle.Paddle = None
        self._paddleRight: Pong_Paddle.Paddle = None

        self._player1Points: int = 0
        self._player2Points: int = 0

        # TODO Rechtschreibfehler behoben: movePrescaller -> movePrescaler
        self._movePrescaler: int = 0
        self._ballSpeedPrescaler: int = 0

        self._paddleLeft.setPosition(0, Display.DISPLAY_Y_EXTEND / 2)
        self._paddleRight.setPosition(Display.DISPLAY_X_EXTEND - 2, Display.DISPLAY_Y_EXTEND / 2)

        self._paddleLeft.setBounceSoundEffect(PADDLE_SOUND_EFFECT_LEFT)
        self._paddleRight.setBounceSoundEffect(PADDLE_SOUND_EFFECT_RIGHT)

        self._paddleLeft.setOrientation(False)
        self._paddleRight.setOrientation(True)

        self._restart()

        self._fieldLineColor: graphics.Color = Display.Display.getColorFrom333(0, 7, 0)

        NumericDisplay.NumericDisplay.test()

    def play(self):
        self._movePrescaler += 1

        # TODO
        if self._movePrescaler & 0x4:
            self._movePlayer()
            self._movePrescaler = 0
        
        self._ball.move()

        if self._ball.hasMoved():
            if not self._checkCollision():
                # C++ Source was Switch/case
                boundries = self._checkBoundaries()
                if boundries == EVENT_PLAYER_LEFT_POINT:
                    self._player1Points += 1
                    self._restart()
                elif boundries == EVENT_PLAYER_RIGHT_POINT:
                    self._player2Points += 1
                    self._restart()
                elif (boundries == EVENT_BOUNCE_TOP) or (boundries == EVENT_BOUNCE_BOTTOM):
                    self._ball.bounceY
        pass

    def draw(self):
        aa += 1
        textColor: int = Display.Display.getColorFrom333(0, 2, aa >> 5)

        NumericDisplay.NumericDisplay.displayTime(NumericDisplay.DISPLAY_MIDDLE, self._time / 1000)

        Display.Display.clearDisplay()
        Display.Display.drawText(self._name, 4, 4, textColor, 1)

        self._drawField()

        self._paddleLeft.draw()
        self._paddleRight.draw()
        self._ball.draw()

        Display.Display.refresh()
        pass

    def prepareDemo(self):
        # Game.py variable
        self._player1Type = Game.PLAYER_TYPE_AI_0
        self._player2Type = Game.PLAYER_TYPE_AI_0

        self._prepareGame()
        pass

    def playDemo(self):
        self._playGame()
        pass

    def prepareGame(self):
        self._player1Points = 0
        self._player2Points = 0

        NumericDisplay.NumericDisplay.displayValue(NumericDisplay.DISPLAY_LEFT, self._player1Points)
        NumericDisplay.NumericDisplay.displayValue(NumericDisplay.DISPLAY_RIGHT, self._player2Points)

        self._restart()
        self._timeStart()
        pass

    def playGame(self):
        self.play()
        self.draw()

        if self._ballSpeedPrescaler > BALL_SPEED_INCREASE_FACTOR:
            self._ballSpeedPrescaler = 0
            self._ball.increaseSpeed()
        
        self._ballSpeedPrescaler += 1
        pass

    def process(self):
        super().process()

        if self._state == Game.GAME_STATE_PLAY:
            if (self._player1Points == 10) or (self._player2Points == 10):
                self._state = Game.GAME_STATE_END
        pass

    def _movePlayer(self):
        # Player 1
        if self._player1Type > Game.PLAYER_TYPE_HUMAN:
            self._computerMove(self._paddleLeft, False)
        else:
            if self._joystickLeft.isUp():
                self._paddleLeft.move(True)
            if self._joystickLeft.isDown():
                self._paddleLeft.move(False)
            if self._joystickLeft.isRight():
                self._paddleLeft.bend()
            else:
                self._paddleLeft.unBend()
        
        # Player 2
        if self._player2Type > Game.PLAYER_TYPE_HUMAN:
            self._computerMove(self._paddleRight, False)
        else:
            if self._joystickRight.isUp():
                self._paddleRight.move(True)
            if self._joystickRight.isDown():
                self._paddleRight.move(False)
            if self._joystickRight.isRight():
                self._paddleRight.bend()
            else:
                self._paddleRight.unBend()
        pass

    def _drawField(self):
        for i in range(Display.DISPLAY_Y_EXTEND):
            if i % 2 == 0:
                Display.Display.drawPixel(15, i, self._fieldLineColor)
            else:
                Display.Display.drawPixel(16, i, self._fieldLineColor)
        pass

    # TODO C++: void computerMove(Paddle * paddle, bool direction);
    def _computerMove(self, paddle: Pong_Paddle.Paddle, direction: bool):
        ballY: int = self._ball.getYPos()
        ballX: int = self._ball.getXPos()
        paddleY: int = paddle.getYPos()

        if direction:
            if ballX < Display.DISPLAY_X_EXTEND / 2:
                return
        else:
            if ballX > Display.DISPLAY_X_EXTEND / 2:
                return
        
        if ballY > paddleY + 2:
            paddle.move(False)
        elif ballY < paddleY + 2:
            paddle.move(True)
        pass

    # TODO Rechtschreibfehler behoben: _checkBoundarys -> _checkBoundaries
    def _checkBoundaries(self) -> int:
        x: int = self._ball.getXPos()
        y: int = self._ball.getYPos()

        if x < 0:
            return EVENT_PLAYER_RIGHT_POINT
        elif x > Display.DISPLAY_X_EXTEND - 1:
            return EVENT_PLAYER_LEFT_POINT

        if y <= 0:
            return EVENT_BOUNCE_TOP
        elif y >= Display.DISPLAY_Y_EXTEND - 1:
            return EVENT_BOUNCE_BOTTOM
            
        return EVENT_NONE

    # TODO Rechtschreibfehler behoben: _checkColision -> _checkCollision
    def _checkCollision(self) -> bool:
        x: int = self._ball.getXPos()
        y: int = self._ball.getYPos()

        collision: bool = False

        event: int = self._paddleLeft.checkContact(x, y)

        if event == Pong_Paddle.EVENT_NO_BOUNCE:
            event: int = self._paddleRight.checkContact(x, y)
            if event != Pong_Paddle.EVENT_NO_BOUNCE:
                # Serial.print("event")
                # Serial.println(event)

                # Serial.print(" : X =")
                # Serial.print(x)
                # Serial.print(" : Y =")
                # Serial.print(y)
                # TODO pyserial
                pass
    
            # C++ Source was Switch/case
            # if event == Pong_Paddle.EVENT_NO_BOUNCE:
            #     pass
            # el
            if event in [Pong_Paddle.EVENT_BOUNCE_MIDDLE, Pong_Paddle.EVENT_BOUNCE_LOW, Pong_Paddle.EVENT_BOUNCE_HIGH]:
                collision = True
                self._ball.bounceX()
            elif event == Pong_Paddle.EVENT_BOUNCE_MIDDLE_BEND:
                collision = True
                self._ball.bounceX()
                self._ball.increaseSpeed()
        
        return collision

    def _restart(self):
        angle: int = random.randrange(16)
        vectorX: int = Sine.Sine.getSineValue(angle)
        vectorY: int = Sine.Sine.getCosineValue(angle)

        # TODO C++ Source was Switch/case
        randomNr = random.randrange(3)
        if randomNr == 1:
            vectorX = - vectorX
        elif randomNr == 2:
            vectorY = - vectorY
        elif randomNr == 3:
            vectorX = - vectorX
            vectorY = - vectorY
        
        vectorX >>= 3
        vectorY >>= 3

        self._ball.setPosition(Display.DISPLAY_X_EXTEND / 2, Display.DISPLAY_Y_EXTEND / 2)
        self._ball.setVector(vectorX, vectorY)
        self._ball.setSpeed(10)

        NumericDisplay.NumericDisplay.displayValue(NumericDisplay.DISPLAY_LEFT, self._player1Points)
        NumericDisplay.NumericDisplay.displayValue(NumericDisplay.DISPLAY_RIGHT, self._player2Points)

        self._ballSpeedPrescaler = 0
        pass
