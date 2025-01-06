import time
import psutil
import os

# #include "game.h"
import Game
# #include "Joystick.h"
import Joystick
# #include "inc/TetrisDemo.h"
import TetrisDemo
# #include "inc/TetrisLogic.h"
import TetrisLogic

import StartButton


class TetrisGame(Game.Game):
    def __init__(self, leftJoystick: Joystick.Joystick, rightJoystick: Joystick.Joystick):
        # TODO Super constructor call
        super().__init__(leftJoystick, rightJoystick, "TTRS")

        # Initialisierung von Demo und Spiellogik
        self.__tetrisDemo: TetrisDemo.TetrisDemo = None
        self.__tetrisLogic: TetrisLogic.TetrisLogic = None
        self.__playerLeft: TetrisLogic.TetrisPlayer = None
        self.__playerRight: TetrisLogic.TetrisPlayer = None

        # Status der Joysticks
        self.__statusLeftJoystickOld = self.__JoystickStatus()
        self.__statusRightJoystickOld = self.__JoystickStatus()

        self.__lastTime: int = 0
        self.__repeatLeftRightTime: int = 100
        self.__joystickLeftRepeatLeft: int = 0
        self.__joystickLeftRepeatRight: int = 0
        self.__joystickRightRepeatLeft: int = 0
        self.__joystickRightRepeatRight: int = 0

    class __JoystickStatus:
        def __init__(self):
            self.left: bool = False
            self.right: bool = False
            self.down: bool = False
            self.up: bool = False
            self.buttonTop: bool = False
            self.buttonBody: bool = False

    def prepareDemo(self):
        # Vorbereiten des Tetris-Demos
        self.__tetrisDemo = TetrisDemo.TetrisDemo()
        self.__lastTime = self.millis()

    def playDemo(self):
        # Demo-Modus spielen
        timeNow = self.millis()
        loopTime = timeNow - self.__lastTime
        self.__lastTime = timeNow
        self.__tetrisDemo.update(loopTime)

    def prepareGame(self):
        # Vorbereitung des Spiels
        del self.__tetrisDemo
        self.__tetrisLogic = TetrisLogic.TetrisLogic()
        self.__lastTime = self.millis()
        self.__playerLeft = self.__tetrisLogic.playerLeft
        self.__playerRight = self.__tetrisLogic.playerRight

    def playGame(self):
        # Spielmodus spielen
        timeNow = self.millis()
        loopTime = timeNow - self.__lastTime
        self.__lastTime = timeNow

        if self.__tetrisLogic.isGameEnd():
            self._state = Game.GAME_STATE_END

        if StartButton.StartButton.getStatus() == Game.START_BUTTON_PRESSED:
            self.__tetrisLogic.startButtonPressed()

        if not self.__tetrisLogic.isEndScreen():
            self.handleJoystickInputs(self.__playerLeft, self._joystickLeft, self.__statusLeftJoystickOld, loopTime)
            self.handleJoystickInputs(self.__playerRight, self._joystickRight, self.__statusRightJoystickOld, loopTime)

        self.updateStatus()
        self.__tetrisLogic.update(loopTime)

    def handleJoystickInputs(self, player, joystick, joystickStatus, loopTime):
        # Diese Methode verarbeitet die Eingaben des Joysticks und führt die entsprechenden Aktionen aus
        if joystickStatus.left and joystick.isLeft():
            self.__joystickLeftRepeatLeft += loopTime
            if self.__joystickLeftRepeatLeft > self.__repeatLeftRightTime:
                self.__joystickLeftRepeatLeft -= self.__repeatLeftRightTime
                player.inputMoveLeft()

        # Wiederholung der Eingabe für "Rechts"
        if joystickStatus.right and joystick.isRight():
            self.__joystickLeftRepeatRight += loopTime
            if self.__joystickLeftRepeatRight > self.__repeatLeftRightTime:
                self.__joystickLeftRepeatRight -= self.__repeatLeftRightTime
                player.inputMoveRight()

        # Wenn die "Hoch"-Taste gedrückt wird
        if joystick.isUp() and not joystickStatus.up:
            player.inputRotateClockwise()

        # Wenn die "Runter"-Taste gedrückt wird
        if joystick.isDown() and not joystickStatus.down:
            player.softDropOn()

        # Tastenfreigabe
        if joystickStatus.down and not joystick.isDown():
            player.softDropOff()

        joystickStatus.left = joystick.isLeft()
        joystickStatus.right = joystick.isRight()
        joystickStatus.up = joystick.isUp()
        joystickStatus.down = joystick.isDown()
        joystickStatus.buttonTop = joystick.isButtonTop()
        joystickStatus.buttonBody = joystick.isButtonBody()

    def updateStatus(self):
        # Aktualisierung des Joystick-Status
        pass

    def millis(self) -> int:
        # Diese Methode gibt die Zeit in Millisekunden zurück
        p = psutil.Process(os.getpid())
        return int(time.time() - p.create_time())
