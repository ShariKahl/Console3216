import Game
import Joystick
import CurveFeverLogic
import CurveFeverView
import MIDI_Control_Commands

# Not in C++ includes, but needed for Position class:
import CurveFeverPlayer

TICKS_TO_EVENT: int = 10
TRACK_ID: int = 10


class Curve(Game.Game):
    def __init__(self, leftJoystick: Joystick, rightJoystick: Joystick):
        super().__init__(leftJoystick, rightJoystick, "CURV")
        self.demoTop = CurveFeverPlayer.Position(0, 0)
        self.demoBottom = CurveFeverPlayer.Position(0, 0)
        self.ticks = 0
        self.clearDemoLines = False
        self.__gameStatus = None
        self.__logic = CurveFeverLogic.Logic()
        self.__view = CurveFeverView.CurveFeverView()

    def prepareDemo(self):
        self.__view.clearScreen()
        self.demoTop = CurveFeverPlayer.Position(0, 2)
        self.demoBottom = CurveFeverPlayer.Position(CurveFeverLogic.FIELD_WIDTH - 1, 13)
        self.ticks = 0

    def playDemo(self):
        self.__view.setBoost(CurveFeverLogic.PLAYER_1, 0)
        self.__view.setBoost(CurveFeverLogic.PLAYER_2, 0)
        self.__view.setTime(0)

        posUpdate = [CurveFeverLogic.CellUpdate(0, 0, CurveFeverLogic.STATE_EMPTY) 
                     for _ in range(CurveFeverLogic.FIELD_WIDTH * CurveFeverLogic.FIELD_HEIGHT)]
        
        item_positions = {(4, 5), (4, 6), (4, 7), (4, 8), (4, 9), 
                          (5, 4), (5, 10), (6, 4), (6, 10), (7, 4),
                          (7, 10), (8, 5), (8, 9), (10, 4), (10, 5),
                          (10, 6), (10, 7), (10, 8), (10, 9), (11, 10),
                          (12, 10), (13, 10), (14, 4), (14, 5), (14, 6),
                          (14, 7), (14, 8), (14, 9), (16, 4), (16, 5),
                          (16, 6), (16, 7), (16, 8), (16, 9), (16, 10),
                          (17, 4), (17, 7), (18, 4), (18, 7), (18, 8),
                          (19, 4), (19, 7), (19, 9), (20, 5), (20, 6),
                          (20, 10), (22, 4), (22, 5), (22, 6), (22, 7),
                          (22, 8), (23, 9), (24, 10), (25, 9), (26, 4),
                          (26, 5), (26, 6), (26, 7), (26, 8)}

        for x in range(CurveFeverLogic.FIELD_WIDTH):
            for y in range(CurveFeverLogic.FIELD_HEIGHT):
                i = x * CurveFeverLogic.FIELD_HEIGHT + y
                posUpdate[i].x, posUpdate[i].y = x, y
                posUpdate[i].state = CurveFeverLogic.STATE_ITEM_1 if (x, y) in item_positions else CurveFeverLogic.STATE_EMPTY
                
                if self.clearDemoLines:
                    if x < self.demoTop.x and y == self.demoTop.y:
                        posUpdate[i].state = CurveFeverLogic.STATE_PLAYER_1
                else:
                    if x > self.demoBottom.x and y == self.demoBottom.y:
                        posUpdate[i].state = CurveFeverLogic.STATE_PLAYER_2
        
        self.demoTop.x += 1
        self.demoBottom.x += 1

        if self.demoTop.x >= CurveFeverLogic.FIELD_WIDTH:
            self.clearDemoLines = not self.clearDemoLines
            self.demoTop.x = 0
            self.demoBottom.x = CurveFeverLogic.FIELD_WIDTH - 1

        updateCount = 255
        self.__view.updatePixels(posUpdate, updateCount)
        self.__view.updatePixels(posUpdate[256:], updateCount)
        self.ticks += 1

    def prepareGame(self):
        self.__view.clearScreen()
        self._timeStart()
        self.ticks = 0
        MIDI_Control_Commands.setupMidi()
        MIDI_Control_Commands.playTrack(TRACK_ID, 100)
        self.__gameStatus = self.__logic.initGame(self._leftJoystick, self._rightJoystick)

    def playGame(self):
        self.ticks += 1
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

    def gameOver(self):
        super()._gameOver()
        MIDI_Control_Commands.stopTrack(TRACK_ID)
        self.__view.printWinner(self.__logic.getWinner())

    def process(self):
        super().process()
        if self._state == Game.GAME_STATE_PLAY:
            self.playGame()
