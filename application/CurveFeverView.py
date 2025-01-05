# #include "Arduino.h"
# #include "CurveFeverLogic.h"
import CurveFeverLogic
# #include "inc/CurveFeverView.h"


# TODO C++ includes:
# #include "display.h"
import Display
# #include "numericDisplay.h"
import NumericDisplay
# #include "Sound.h"
import Sound

# TODO C++: #define EMPTY_COLOR Display::getColor(0, 0, 0);
EMPTY_COLOR = Display.Display.getColorFrom333(0, 0, 0) # Display::getColor(0, 0, 0);
PLAYER_1_COLOR_1 = Display.Display.getColorFrom333(7, 0, 0) # Display::getColor(7, 0, 0);
PLAYER_1_COLOR_2 = Display.Display.getColorFrom333(4, 0, 0) # Display::getColor(4, 0, 0);
PLAYER_2_COLOR_1 = Display.Display.getColorFrom333(0, 7, 0) # Display::getColor(0, 7, 0);
PLAYER_2_COLOR_2 = Display.Display.getColorFrom333(0, 4, 0) # Display::getColor(0, 4, 0);
ITEM_1_COLOR = Display.Display.getColorFrom333(0, 0, 7) # Display::getColor(0, 0, 7);
ITEM_2_COLOR = Display.Display.getColorFrom333(0, 2, 2) # Display::getColor(0, 2, 2);
ITEM_3_COLOR = Display.Display.getColorFrom333(3, 3, 3) # Display::getColor(3, 3, 3);


class CurveFeverView:
    def __getColorOfState(state: int) -> int:
        color: int = EMPTY_COLOR
        # TODO C++ source was switch/case
        # TODO C++ source never used PLAYER_1_COLOR_2, assuming bug
        if state == CurveFeverLogic.STATE_PLAYER_1:
            color = PLAYER_1_COLOR_1
        elif state == CurveFeverLogic.STATE_PLAYER_2:
            color = PLAYER_2_COLOR_1 # TODO C++ source used PLAYER_2_COLOR_2
        elif state == CurveFeverLogic.STATE_ITEM_SLOW:
            color = ITEM_1_COLOR
        elif state == CurveFeverLogic.STATE_ITEM_WALL:
            color = ITEM_2_COLOR
        elif state == CurveFeverLogic.STATE_ITEM_CLEAR:
            color = ITEM_3_COLOR
        elif state == CurveFeverLogic.STATE_TAIL_1:
            color = PLAYER_1_COLOR_2 # TODO C++ source used PLAYER_1_COLOR_1
        elif state == CurveFeverLogic.STATE_TAIL_2:
            color = PLAYER_2_COLOR_2 # TODO C++ source used PLAYER_2_COLOR_1
        
        return color

    # TODO C++: void printGameName(char *name);
    def printGameName(self, name: int):
        nameColor: int = Display.Display.getColorFrom333(2, 0, 2)
        Display.Display.drawText(name, 4, 4, nameColor, 1)
        Display.Display.refresh()
        Display.Display.drawText(name, 4, 4, nameColor, 1)
        pass

    # TODO C++: void updatePixels(CellUpdate* cells, uint8_t cellCount);
    def updatePixels(self, cells: CurveFeverLogic.CellUpdate, cellCount: int):
        for j in range(2):
            for i in range(cellCount):
                Display.Display.drawPixel(cells[i].x, cells[i].y, self.__getColorOfState(cells[i].state))

            if j == 0:
                Display.Display.refresh()
        pass

    def clearScreen(self):
        Display.Display.clearDisplay()
        Display.Display.refresh()
        Display.Display.clearDisplay()
        pass

    def setBoost(self, player: int, boost: int):
        display: int = NumericDisplay.DISPLAY_LEFT
        if player == CurveFeverLogic.PLAYER_2:
            display = NumericDisplay.DISPLAY_RIGHT
        
        NumericDisplay.NumericDisplay.displayValue(display, boost)
        pass

    def setTime(self, time: int):
        NumericDisplay.NumericDisplay.displayTime(NumericDisplay.DISPLAY_MIDDLE, time)
        pass

    def printWinner(self, winner: int):
        value: int = 0
        # TODO C++ source: char* output = "Draw!";
        output: str = "Draw!"

        if winner == CurveFeverLogic.PLAYER_1:
            value = 60 * 11 + 11
            output = "P1 Wins!"
        elif winner == CurveFeverLogic.PLAYER_2:
            value = 60 * 22 + 22
            output = "P2 Wins!" # C++ Source: output = "P1 Wins!";
        
        NumericDisplay.NumericDisplay.displayTime(NumericDisplay.DISPLAY_LEFT, value)
        NumericDisplay.NumericDisplay.displayTime(NumericDisplay.DISPLAY_MIDDLE, value)
        NumericDisplay.NumericDisplay.displayTime(NumericDisplay.DISPLAY_RIGHT, value)
        Display.Display.drawText(output, 1, 1, CurveFeverLogic.PLAYER_1, 1)
        pass

    def playSound(self, soundId: int):
        for i in range(0, 256, 5):
            if soundId == Sound.SOUND_ITEM_COLLECT:
                Sound.Sound.playSoundDura(i, 9, 100)
            elif soundId == Sound.SOUND_ITEM_ACTIVATE:
                Sound.Sound.playSoundDura(255 - i, 9, 100)
            elif soundId == Sound.SOUND_GAMEOVER:
                Sound.Sound.playSoundDura(60, 9, 100)
        pass
