# #include "game.h"
import Game
# #include "Joystick.h"
import Joystick
# #include "CurveFeverLogic.h"
import CurveFeverLogic
# #include "CurveFeverView.h"
import CurveFeverView

# Not in C++ includes, but needed for Position class:
import CurveFeverPlayer

# TODO C++ includes:
# #include "inc/curve_game.h"
# #include <display.h>
# #include <numericDisplay.h>
# #include <sine.h>
# #include "MIDI_Control_Commands.h"
import MIDI_Control_Commands

# TODO C++ Defines
TICKS_TO_EVENT: int = 10
TRACK_ID: int = 10

# TODO C++ Global Vars.
demoTop: CurveFeverPlayer.Position = None
demoBottom: CurveFeverPlayer.Position = None
ticks: int = 0

clearDemoLines: bool = False

class Curve(Game.Game):
    # TODO C++ Konstruktor: Curve(Joystick & leftJoystick, Joystick & rightJoystick);
    def __init__(self, leftJoystick: Joystick, rightJoystick: Joystick):
        # TODO C++ Source (Empty brackets {}):
        # Curve::Curve(Joystick &leftJoystick, Joystick &rightJoystick) : Game(leftJoystick, rightJoystick, (char *) "CURV") {}
        super().__init__(leftJoystick, rightJoystick, "CURV")
        
        # TODO C++: GameStatus* gameStatus;
        self.__gameStatus: CurveFeverLogic.GameStatus = None
        self.__logic: CurveFeverLogic.Logic = None
        self.__view: CurveFeverView.CurveFeverView = None

    def prepareDemo(self):
        self.__view.clearScreen()

        demoTop.x = 0
        demoTop.y = 2
        demoBottom.x = CurveFeverLogic.FIELD_WIDTH - 1
        demoBottom.y = 13
        ticks = 0
        pass

    def playDemo(self):
        self.__view.setBoost(CurveFeverLogic.PLAYER_1, 0)
        self.__view.setBoost(CurveFeverLogic.PLAYER_2, 0)
        self.__view.setTime(0)

        # TODO C++ Source:
        # CellUpdate posUpdate[FIELD_WIDTH * FIELD_HEIGHT]
        posUpdate = [None for _ in range(CurveFeverLogic.FIELD_WIDTH * CurveFeverLogic.FIELD_HEIGHT)]

        updateCount: int = 0
        i: int = 0

        for x in range(CurveFeverLogic.FIELD_WIDTH):
            for y in range(CurveFeverLogic.FIELD_HEIGHT):
                # TODO Copy paste from C++, bulk edited to Python syntax and sorted based on x
                # Unique numbers for x and y:
                # x = 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26
                # y = 4, 5, 6, 7, 8, 9, 10
                if x == 4 and y == 5:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 4 and y == 6:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 4 and y == 7:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 4 and y == 8:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 4 and y == 9:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 5 and y == 4:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 5 and y == 10:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 6 and y == 4:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 6 and y == 10:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 7 and y == 4:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 7 and y == 10:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 8 and y == 5:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 8 and y == 9:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 10 and y == 4:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 10 and y == 5:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 10 and y == 6:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 10 and y == 7:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 10 and y == 8:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 10 and y == 9:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 11 and y == 10:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 12 and y == 10:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 13 and y == 10:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 14 and y == 4:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 14 and y == 5:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 14 and y == 6:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 14 and y == 7:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 14 and y == 8:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 14 and y == 9:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 16 and y == 4:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 16 and y == 5:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 16 and y == 6:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 16 and y == 7:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 16 and y == 8:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 16 and y == 9:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 16 and y == 10:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 17 and y == 4:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 17 and y == 7:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 18 and y == 4:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 18 and y == 7:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 18 and y == 8:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 19 and y == 4:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 19 and y == 7:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 19 and y == 9:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 20 and y == 5:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 20 and y == 6:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 20 and y == 10:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 22 and y == 4:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 22 and y == 5:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 22 and y == 6:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 22 and y == 7:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 22 and y == 8:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 23 and y == 9:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 24 and y == 10:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 25 and y == 9:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 26 and y == 4:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 26 and y == 5:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 26 and y == 6:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 26 and y == 7:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                elif x == 26 and y == 8:
                    posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1
                else:
                    posUpdate[i].state = CurveFeverLogic.STATE_EMPTY

                if clearDemoLines:
                    if x < demoTop.x and y == demoTop.y:
                        posUpdate[i].state = CurveFeverLogic.STATE_PLAYER_1
                    if x < demoBottom.x and y == demoBottom.y:
                        posUpdate[i].state = CurveFeverLogic.STATE_PLAYER_2
                else:
                    if x > demoTop.x and y == demoTop.y:
                        posUpdate[i].state = CurveFeverLogic.STATE_PLAYER_1
                    if x > demoBottom.x and y == demoBottom.y:
                        posUpdate[i].state = CurveFeverLogic.STATE_PLAYER_2
                
                posUpdate[i].x = x
                posUpdate[i].y = y
                i += 1
        demoTop.x += 1
        demoBottom.x += 1

        if demoTop.x >= CurveFeverLogic.FIELD_WIDTH:
            clearDemoLines = not clearDemoLines
            demoTop.x = 0
            demoBottom.x = CurveFeverLogic.FIELD_WIDTH - 1
        
        updateCount = 255
        self.__view.updatePixels(posUpdate, updateCount)
        # TODO C++ Source:
        # view.updatePixels(posUpdate + 256, updateCount);
        # + 256 is C++ array arithmetic, will fail in Python, code untested
        self.__view.updatePixels(posUpdate[256], updateCount)
        ticks += 1
        pass

    def prepareGame(self):
        self.__view.clearScreen()
        # TODO C++ Source:
        # this->timeStart();
        self._timeStart()
        ticks = 0

        # TODO C++ Source:
        # MIDI_Control_Commands::setupMidi();
        # MIDI_Control_Commands::playTrack(TRACK_ID,100);
        MIDI_Control_Commands.MIDI_Control_Commands.setupMidi()
        MIDI_Control_Commands.MIDI_Control_Commands.playTrack(TRACK_ID, 100)

        # TODO C++ Source:
        # gameStatus = logic.initGame(joystickLeft, joystickRight);
        self.__gameStatus = self.__logic.initGame(self._leftJoystick, self._rightJoystick)

        pass

    def playGame(self):
        ticks += 1
        self.__gameStatus = self.__logic.move()

        self.__view.setBoost(CurveFeverLogic.PLAYER_1, self.__gameStatus.player1Boost)
        self.__view.setBoost(CurveFeverLogic.PLAYER_2, self.__gameStatus.player2Boost)
        
        self.__view.setTime(int(self._time / 1000))

        if self.__gameStatus.clearScreen:
            self.__view.clearScreen()
        
        self.__view.updatePixels(self.__gameStatus.cellUpdates, self.__gameStatus.updateCount)

        if self.__gameStatus.gameOver:
            self._state = Game.GAME_STATE_END
        
        self.__view.playSound(self.__gameStatus.soundStatus)
        pass

    def gameOver(self):
        super()._gameOver()
        MIDI_Control_Commands.MIDI_Control_Commands.stopTrack(TRACK_ID)
        self.__view.printWinner(self.__logic.getWinner())
        pass

    def process(self):
        super().process()

        # TODO C++ Source:
        # if (this->state == GAME_STATE_PLAY) {
            # playGame();
        # }

        if self._state == Game.GAME_STATE_PLAY:
            self.playGame()
        pass
