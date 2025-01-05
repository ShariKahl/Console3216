from enum import Enum

# #include "inc/TetrisPlayer.h"
import TetrisPlayer

import Display
import NumericDisplay

class TetrisLogicStatus(Enum):
    UPDATING = 0
    ENDSCREEN = 1
    ENDGAME = 2


class TetrisLogic:
    def __init__(self):
        self.__status: TetrisLogicStatus = None

        # TODO C++: TetrisPlayer* playerLeft;
        self.playerLeft: TetrisPlayer.TetrisPlayer = None
        # TODO C++: TetrisPlayer* playerRight;
        self.playerRight: TetrisPlayer.TetrisPlayer = None

        self.initializeGame()

    def __handleStatus(self, player: TetrisPlayer.TetrisPlayer):
        # TODO C++ Source was Switch/case
        if player.getStatus() == TetrisPlayer.TetrisPlayerStatus.PLAYING:
            pass
        elif player.getStatus() == TetrisPlayer.TetrisPlayerStatus.LOST:
            self.__status = TetrisLogicStatus.ENDSCREEN
        pass

    def __drawBorders(self):
        for y in range(16):
            Display.Display.drawPixel(10, y, Display.Display.getColorFrom333(2, 0, 0))
            Display.Display.drawPixel(21, y, Display.Display.getColorFrom333(2, 0, 0))
        pass

    def update(self, delta: int):
        Display.Display.clearDisplay()

        # TODO C++ Source was Switch/case
        if self.__status == TetrisLogicStatus.UPDATING:
            self.__handleStatus(self.playerLeft)
            self.__handleStatus(self.playerRight)

            # Serial.println("UPDATING")
            self.playerLeft.update(delta)
            self.playerRight.update(delta)
            self.playerLeft.displayPlayerPoints(True)
            self.playerRight.displayPlayerPoints(False)

            self.__drawBorders()
            self.playerLeft.drawNextTetroms(12, 2)
            self.playerRight.drawNextTetroms(17, 2)

            self.playerLeft.draw()
            self.playerRight.draw()
        elif self.__status == TetrisLogicStatus.ENDSCREEN:
            # Serial.println("ENDSCREEN")
            self.__drawBorders()
            self.playerLeft.draw()
            self.playerRight.draw()
        elif self.__status == TetrisLogicStatus.ENDGAME:
            # TODO C++ Source lines were commented out
            # Serial.println("ENDGAME");
            # self.resetGame();
            pass

        Display.Display.refresh()
        pass

    def startButtonPressed(self):
        # TODO C++ Source was Switch/case
        if self.__status == TetrisLogicStatus.UPDATING:
            # Serial.println("Button to EndScreen")
            self.__status = TetrisLogicStatus.ENDSCREEN
        elif self.__status == TetrisLogicStatus.ENDSCREEN:
            # Serial.println("Button to EndGame")
            self.__status = TetrisLogicStatus.ENDGAME
        elif self.__status == TetrisLogicStatus.ENDGAME:
            pass
        pass

    def isGameEnd(self) -> bool:
        if self.__status == TetrisLogicStatus.ENDGAME:
            return True
        
        return False

    def isEndScreen(self) -> bool:
        if self.__status == TetrisLogicStatus.ENDSCREEN:
            return True
        
        return False

    def initializeGame(self):
        NumericDisplay.NumericDisplay.test()
        self.playerLeft = TetrisPlayer.TetrisPlayer(0, 0)
        self.playerRight = TetrisPlayer.TetrisPlayer(22, 0)
        self.__status = TetrisLogicStatus.UPDATING
        pass

    def resetGame(self):
        self.playerLeft.reset()
        self.playerRight.reset()
        pass
