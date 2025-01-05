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

        # TODO C++: TetrisDemo* tetrisDemo;
        self.__tetrisDemo: TetrisDemo.TetrisDemo = None
        # TODO C++: TetrisLogic* tetrisLogic;
        self.__tetrisLogic: TetrisLogic.TetrisLogic = None
        # TODO C++: TetrisPlayer* playerLeft;
        self.__playerLeft: TetrisLogic.TetrisPlayer = None
        # TODO C++: TetrisPlayer* playerRight;
        self.__playerRight: TetrisLogic.TetrisPlayer = None

        self.__statusLeftJoystickOld: self.__JoystickStatus = None
        self.__statusRightJoystickOld: self.__JoystickStatus = None

        self.__lastTime: int = 0

        self.__repeatLeftRightTime: int = 100

        self.__joystickLeftRepeatLeft: int = 0
        self.__joystickLeftRepeatRight: int = 0

        self.__joystickRightRepeatLeft: int = 0
        self.__joystickRightRepeatRight: int = 0

        # TODO pyserial
        # Serial.println("Tetris Game Konstruktor!")

    # TODO C++: struct JoystickStatus {...};
    class __JoystickStatus:
        def __init__(self):
            self.left: bool = False
            self.right: bool = False
            self.down: bool = False
            self.up: bool = False

            self.buttonTop: bool = False
            self.buttonBody: bool = False

    def prepareDemo(self):
        # TODO pyserial
        # Serial.println("Tetris Game prepare Demo!")
        self.__tetrisDemo = TetrisDemo.TetrisDemo()
        self.__lastTime = self.millis()
        pass

    def playDemo(self):
        timeNow: int = self.millis()
        loopTime: int = timeNow - self.__lastTime
        self.__lastTime = timeNow

        self.__tetrisDemo.update(loopTime)
        pass

    def prepareGame(self):
        del self.__tetrisDemo

        # TODO pyserial
        # Serial.println("Tetris Game prepare Game!")
        self.__tetrisLogic = TetrisLogic.TetrisLogic()
        self.__lastTime = self.millis()
        self.__playerLeft = self.__tetrisLogic.playerLeft
        self.__playerRight = self.__tetrisLogic.playerRight
        pass

    def playGame(self):
        timeNow: int = self.millis()
        loopTime: int = timeNow - self.__lastTime
        self.__lastTime = timeNow

        if self.__tetrisLogic.isGameEnd():
            self._state = Game.GAME_STATE_END
            # TODO pyserial
            # Serial.println("End Game")
        
        if StartButton.StartButton.getStatus() == Game.START_BUTTON_PRESSED:
            self.__tetrisLogic.startButtonPressed()
        
        if not self.__tetrisLogic.isEndScreen():
            # Left Joystick Left + Repeat
            if (self.__statusLeftJoystickOld.left and self._joystickLeft.isLeft()):
                self.__joystickLeftRepeatLeft += loopTime
                if self.__joystickLeftRepeatLeft > self.__repeatLeftRightTime:
                    self.__joystickLeftRepeatLeft -= self.__repeatLeftRightTime
                    self.__playerLeft.inputMoveLeft()
            else:
                self.__joystickLeftRepeatLeft = self.__repeatLeftRightTime
            
            # Left Joystick Right + Repeat
            if (self.__statusLeftJoystickOld.right and self._joystickLeft.isRight()):
                self.__joystickLeftRepeatRight += loopTime
                if self.__joystickLeftRepeatRight > self.__repeatLeftRightTime:
                    self.__joystickLeftRepeatRight -= self.__repeatLeftRightTime
                    self.__playerLeft.inputMoveRight()
            else:
                self.__joystickLeftRepeatRight = self.__repeatLeftRightTime
            
            # Left Joystick Up
            if ((not self.__statusLeftJoystickOld.up) and self._joystickLeft.isUp()):
                # TODO Condition body empty in C++ Source
                pass
            
            # Left Joystick Down
            if ((not self.__statusLeftJoystickOld.down) and self._joystickLeft.isDown()):
                self.__playerLeft.softDropOn()
            
            # Left Joystick Not Down
            if (self.__statusLeftJoystickOld.down and (not self._joystickLeft.isDown())):
                self.__playerLeft.softDropOff()
            
            # Left Top Button Down
            if (self.__statusLeftJoystickOld.buttonTop and (not self._joystickLeft.isButtonTop())):
                self.__playerLeft.inputRotateClockwise()
            
            # Left Body Button Down
            if (self.__statusLeftJoystickOld.buttonBody and (not self._joystickLeft.isButtonBody())):
                # TODO Condition body empty in C++ Source
                pass

            # Right Joystick Left + Repeat
            if (self.__statusRightJoystickOld.left and self._joystickRight.isLeft()):
                self.__joystickRightRepeatLeft += loopTime
                if self.__joystickRightRepeatLeft > self.__repeatLeftRightTime:
                    self.__joystickRightRepeatLeft -= self.__repeatLeftRightTime
                    self.__playerRight.inputMoveLeft()
            else:
                self.__joystickRightRepeatLeft = self.__repeatLeftRightTime
            
            # Right Joystick Right + Repeat
            if (self.__statusRightJoystickOld.right and self._joystickRight.isRight()):
                self.__joystickRightRepeatRight += loopTime
                if self.__joystickRightRepeatRight > self.__repeatLeftRightTime:
                    self.__joystickRightRepeatRight -= self.__repeatLeftRightTime
                    self.__playerRight.inputMoveRight()
            else:
                self.__joystickRightRepeatRight = self.__repeatLeftRightTime
            
            # Right Joystick Up
            if ((not self.__statusRightJoystickOld.up) and self._joystickRight.isUp()):
                # TODO Condition body empty in C++ Source
                pass
            
            # Right Joystick Down
            if ((not self.__statusRightJoystickOld.down) and self._joystickRight.isDown()):
                self.__playerRight.softDropOn()
            
            # Right Joystick Not Down
            if (self.__statusRightJoystickOld.down and (not self._joystickRight.isDown())):
                self.__playerRight.softDropOff()
            
            # Right Top Button Down
            if (self.__statusRightJoystickOld.buttonTop and (not self._joystickRight.isButtonTop())):
                self.__playerRight.inputRotateClockwise()
            
            # Right Body Button Down
            if (self.__statusRightJoystickOld.buttonBody and (not self._joystickRight.isButtonBody())):
                # TODO Condition body empty in C++ Source
                pass
            
            self.updateStatus()
        
        self.__tetrisLogic.update(loopTime)
        pass

    def updateStatus(self):
        self.__statusLeftJoystickOld.left = self._joystickLeft.isLeft()
        self.__statusLeftJoystickOld.right = self._joystickLeft.isRight()
        self.__statusLeftJoystickOld.up = self._joystickLeft.isUp()
        self.__statusLeftJoystickOld.down = self._joystickLeft.isDown()
        self.__statusLeftJoystickOld.buttonTop = self._joystickLeft.isButtonTop()
        self.__statusLeftJoystickOld.buttonBody = self._joystickLeft.isButtonBody()
        
        self.__statusRightJoystickOld.left = self._joystickRight.isLeft()
        self.__statusRightJoystickOld.right = self._joystickRight.isRight()
        self.__statusRightJoystickOld.up = self._joystickRight.isUp()
        self.__statusRightJoystickOld.down = self._joystickRight.isDown()
        self.__statusRightJoystickOld.buttonTop = self._joystickRight.isButtonTop()
        self.__statusRightJoystickOld.buttonBody = self._joystickRight.isButtonBody()
        pass

    # TODO Replacement for Arduinos millis() function
    """
    /**
    * Original Arduino function returns the process uptime.
    * This function can return Process uptime or System uptime.
    *
    * Method 1: Calculates the process uptime.
    * Grabs current process.
    * Grabs current time in unix timestamp format.
    * Subtracts unix timestamp of process creation time.
    * Returns result in milliseconds.
    *
    * Method 2: Calculates the system uptime.
    *
    * Grabs current time in unix timestamp format.
    * Subtracts unix timestamp of boot time.
    * Returns result in milliseconds.
    */
    """
    def millis(self) -> int:
        p = psutil.Process(os.getpid())
        return int(time.time() - p.create_time())
        # return int(time.time() - psutil.boot_time())
