import random

# #include "CurveFeverPlayer.h"
import CurveFeverPlayer
# #include "Joystick.h"
import Joystick

FIELD_HEIGHT = 16
FIELD_WIDTH = 32
FIELD_SIZE = 4 * FIELD_HEIGHT * FIELD_WIDTH / 8
MAX_CHANGE_COUNT = 5

PLAYER_1 = 0
PLAYER_2 = 1
DRAW = 2

NO_SOUND = 0
SOUND_BACKGROUND = 1
SOUND_ITEM_COLLECT = 2
SOUND_ITEM_ACTIVATE = 3
SOUND_GAMEOVER = 4

STATE_EMPTY = 0
STATE_PLAYER_1 = 1
STATE_PLAYER_2 = 2
STATE_ITEM_SLOW = 3
STATE_ITEM_WALL = 4
STATE_ITEM_CLEAR = 5
STATE_TAIL_1 = 6
STATE_TAIL_2 = 7

PROBABILITY_ITEM_SLOW = 16
PROBABILITY_ITEM_WALL = 8
PROBABILITY_ITEM_CLEAR = 4

STATE_ITEM_1 = 3
STATE_ITEM_2 = 4
STATE_ITEM_3 = 5


# TODO C++: typedef struct {...} CellUpdate;
class CellUpdate:
    def __init__(self):
        self.x: int = 0
        self.y: int = 0
        self.state: int = STATE_EMPTY


# TODO C++: typedef struct {...} GameStatus;
class GameStatus:
    def __init__(self):
        self.gameOver: bool = False
        self.clearScreen: bool = True
        self.cellUpdates: CellUpdate = None # TODO C++: CellUpdate* cellUpdates;
        self.updateCount: int = 0
        self.soundStatus: int = NO_SOUND
        self.player1Boost: int = 0
        self.player2Boost: int = 0


class Logic:

    def __init__(self):
        # TODO C++: Joystick* joystick1;
        self.__joystick1: Joystick.Joystick = None
        # TODO C++: Joystick* joystick2;
        self.__joystick2: Joystick.Joystick = None
        # TODO C++: CellUpdate cellUpdates[MAX_CHANGE_COUNT];
        self.__cellUpdates = [CellUpdate for _ in range(MAX_CHANGE_COUNT)]

        self.__status: GameStatus = None
        self.__player1: CurveFeverPlayer.Player = None
        self.__player2: CurveFeverPlayer.Player = None
        self.__winner: int = 0
        # TODO Item ist ein einfaches Int
        self.__currentItem: CurveFeverPlayer.Item = CurveFeverPlayer.NO_ITEM
        self.__itemPosition: CurveFeverPlayer.Position = None
        self.__gameTicks: int = 0

        # TODO C++: uint8_t field[FIELD_WIDTH][FIELD_HEIGHT];
        self.__field = [[0 for _ in range(FIELD_HEIGHT)] for _ in range(FIELD_WIDTH)]

    # TODO C++ Source had no definition
    def __generateItem(self) -> int:
        pass

    def __getCellState(self, x: int, y: int) -> int:
        return self.__field[x][y]

    def __setCellState(self, x: int, y: int, state: int, publish: bool=False):
        self.__field[x][y] = state

        if publish:
            self.__cellUpdates[self.__status.updateCount].x = x
            self.__cellUpdates[self.__status.updateCount].y = y
            self.__cellUpdates[self.__status.updateCount].state = state
            self.__status.updateCount += 1
        pass
    
    def __clearField(self):
        self.__status.clearScreen = True
        self.__status.updateCount = 0
        itemState: int = self.__getCellState(self.__itemPosition.x, self.__itemPosition.y)

        for i in range(FIELD_WIDTH):
            for j in range(FIELD_HEIGHT):
                self.__field[i][j] = STATE_EMPTY
        
        p: CurveFeverPlayer.Position = self.__player1.getPosition()
        self.__setCellState(p.x, p.y, STATE_PLAYER_1, True)
        p = self.__player2.getPosition()
        self.__setCellState(p.x, p.y, STATE_PLAYER_2, True)

        if self.__currentItem != CurveFeverPlayer.NO_ITEM:
            self.__setCellState(self.__itemPosition.x, self.__itemPosition.y, itemState, True)
        pass

    def __setDirectionForPlayer(self, player: CurveFeverPlayer.Player):
        # TODO C++ Source:
        # Joystick* joystick = this->joystick1;
        joystick: Joystick.Joystick = self.__joystick1
        if player.getName() == PLAYER_2:
            joystick = self.__joystick2
        
        direction: int
        if joystick.isLeft():
            direction = CurveFeverPlayer.LEFT
        elif joystick.isRight():
            direction = CurveFeverPlayer.RIGHT
        elif joystick.isUp():
            direction = CurveFeverPlayer.UP
        elif joystick.isDown():
            direction = CurveFeverPlayer.DOWN
        else:
            direction = player.getDirection()
        
        player.setDirection(direction)
        pass

    def __updateOccursThisTick(self, speed: int) -> bool:
        # If speed is FAST, this will always be true.
        # If speed is REGULAR, this will be true for every second tick.
        # If speed is SLOW this will be true for every fourth tick.
        return self.__gameTicks & (speed - 1) == 0

    def __updateCell(self, player: CurveFeverPlayer.Player, head: bool):
        state: int = STATE_EMPTY
        name: int = player.getName()

        if head:
            item: CurveFeverPlayer.Item = player.getItem()
            if item != CurveFeverPlayer.NO_ITEM and (not player.isItemActive() or (player.getItemDuration() & 1) != 0):
                if item == CurveFeverPlayer.ITEM_SLOW:
                    state = STATE_ITEM_SLOW
                elif item == CurveFeverPlayer.ITEM_WALL:
                    state = STATE_ITEM_WALL
                else:
                    state = STATE_ITEM_CLEAR
            elif name == PLAYER_1:
                state = STATE_PLAYER_1
            else:
                state = STATE_PLAYER_2
        elif not player.isCreatingGap():
            if name == PLAYER_1:
                state = STATE_TAIL_1
            else:
                state = STATE_TAIL_2
        
        position: CurveFeverPlayer.Position = player.getPosition()
        self.__setCellState(position.x, position.y, state, True)
        pass

    def __setWinnerAfterValidMove(self, player1Updated: bool, player2Updated: bool):
        pos1: CurveFeverPlayer.Position = self.__player1.getPosition()
        pos2: CurveFeverPlayer.Position = self.__player2.getPosition()
        if self.__havePlayersCollided(pos1, pos2, self.__player1.getDirection(), self.__player2.getDirection()):
            self.__status.gameOver = True
            self.__status.soundStatus = SOUND_GAMEOVER
            if (player1Updated and not player2Updated) or self.__player1.isFasterThan(self.__player2):
                self.__winner = PLAYER_2
            elif (player2Updated and not player1Updated) or self.__player2.isFasterThan(self.__player1):
                self.__winner = PLAYER_1
            else:
                self.__winner = DRAW
        else:
            if self.__getCellState(pos1.x, pos1.y) != STATE_EMPTY and player1Updated:
                self.__status.gameOver = True
                self.__winner = PLAYER_2
            
            if self.__getCellState(pos2.x, pos2.y) != STATE_EMPTY and player2Updated:
                self.__status.gameOver = True
                if self.__winner == PLAYER_2:
                    self.__winner = DRAW
                else:
                    self.__winner = PLAYER_1
        pass

    def __maybeGenerateItem(self):
        # TODO C++ Source:
        # uint32_t randNum = random(100);
        # random() is an Arduino Function, upper bound -> exclusive
        randNum: int = random.randrange(100)
        x: int = int(random.randrange(FIELD_WIDTH))
        y: int = int(random.randrange(FIELD_HEIGHT))

        if self.__getCellState(x, y) == STATE_EMPTY:
            self.__itemPosition.x = x
            self.__itemPosition.y = y

            if randNum < PROBABILITY_ITEM_CLEAR:
                self.__currentItem = CurveFeverPlayer.ITEM_CLEAR
            elif randNum < PROBABILITY_ITEM_WALL + PROBABILITY_ITEM_CLEAR:
                self.__currentItem = CurveFeverPlayer.ITEM_WALL
            elif randNum < PROBABILITY_ITEM_SLOW + PROBABILITY_ITEM_WALL + PROBABILITY_ITEM_CLEAR:
                self.__currentItem = CurveFeverPlayer.ITEM_SLOW
            else:
                self.__currentItem = CurveFeverPlayer.NO_ITEM
            
            if self.__currentItem != CurveFeverPlayer.NO_ITEM:
                cellState: int = STATE_ITEM_SLOW
                if self.__currentItem == CurveFeverPlayer.ITEM_WALL:
                    cellState = STATE_ITEM_WALL
                elif self.__currentItem == CurveFeverPlayer.ITEM_CLEAR:
                    cellState = STATE_ITEM_CLEAR
                
                self.__setCellState(self.__itemPosition.x, self.__itemPosition.y, cellState, True)
        pass

    def __updatePlayer(self, player: CurveFeverPlayer.Player, joystick: Joystick.Joystick) -> bool:
        playerUpdated: bool = False

        if self.__updateOccursThisTick(player.getSpeed()):
            self.__updateCell(player, False)
            self.__setDirectionForPlayer(player)

            if joystick.isButtonTop():
                player.activateBoost()
            else:
                player.deactivateBoost()
            
            if joystick.isButtonBody() and not player.isItemActive():
                player.activateItem()
                self.__status.soundStatus = SOUND_ITEM_ACTIVATE
                if player.getItem() == CurveFeverPlayer.ITEM_CLEAR:
                    self.clearField()
            
            if not player.update():
                self.__status.gameOver = True
                if self.__winner != DRAW:
                    self.__winner = DRAW
                elif player.getName() == PLAYER_1:
                    self.__winner = PLAYER_2
                else:
                    self.__winner = PLAYER_1
            
            playerUpdated = True
        
        return playerUpdated

    def __maybeAbsorbItem(self):
        if self.__currentItem != CurveFeverPlayer.NO_ITEM:
            pos1: CurveFeverPlayer.Position = self.__player1.getPosition()
            pos2: CurveFeverPlayer.Position = self.__player2.getPosition()

            if self.__itemPosition.x == pos1.x and self.__itemPosition.y == pos1.y:
                self.__player1.setItem(self.__currentItem)
                self.__currentItem = CurveFeverPlayer.NO_ITEM
                self.__setCellState(self.__itemPosition.x, self.__itemPosition.y, STATE_EMPTY)
                self.__status.soundStatus = SOUND_ITEM_COLLECT
            elif self.__itemPosition.x == pos2.x and self.__itemPosition.y == pos2.y:
                self.__player2.setItem(self.__currentItem)
                self.__currentItem = CurveFeverPlayer.NO_ITEM
                self.__setCellState(self.__itemPosition.x, self.__itemPosition.y, STATE_EMPTY)
                self.__status.soundStatus = SOUND_ITEM_COLLECT
        else:
            self.__maybeGenerateItem()
        pass

    def __havePlayersCollided(self, pos1: CurveFeverPlayer.Position, pos2: CurveFeverPlayer.Position, dir1: int, dir2: int) -> bool:
        dx: int = abs(int(pos1.x) - int(pos2.x))
        dy: int = abs(int(pos1.y) - int(pos2.y))
        player1Horizontal: bool = dir1 == CurveFeverPlayer.LEFT or dir1 == CurveFeverPlayer.RIGHT
        player2Horizontal: bool = dir2 == CurveFeverPlayer.LEFT or dir2 == CurveFeverPlayer.RIGHT
        oppositeDirection: bool = (dir1 != dir2) and (player1Horizontal == player2Horizontal)
        
        # TODO bitwise XOR operation with boolean, seems to work in Python as well
        return (dx + dy == 0) or ((dx + dy == 1) and oppositeDirection and ((dy == 1) ^ player1Horizontal))

    # TODO C++ return Pointer
    def initGame(self, p1_joystick: Joystick.Joystick, p2_joystick: Joystick.Joystick) -> GameStatus:
        self.__joystick1 = p1_joystick
        self.__joystick2 = p2_joystick
        self.__gameTicks = 0
        self.__currentItem = 0
        self.__itemPosition.x = 0
        self.__itemPosition.y = 0
        self.__winner = DRAW

        CurveFeverPlayer.Player.setBounds(FIELD_WIDTH, FIELD_HEIGHT)

        self.__player1.setName(PLAYER_1)
        self.__player2.setName(PLAYER_2)

        self.__player1.reset()
        self.__player1.setPosition(1, FIELD_HEIGHT / 2)
        self.__player1.setDirection(CurveFeverPlayer.RIGHT)

        self.__player2.reset()
        self.__player2.setPosition(FIELD_WIDTH - 1, FIELD_HEIGHT / 2)
        self.__player2.setDirection(CurveFeverPlayer.LEFT)

        self.__status.gameOver = False
        self.__status.clearScreen = True
        self.__status.cellUpdates = self.__cellUpdates;
        self.__status.updateCount = 0
        self.__status.soundStatus = 0
        self.__status.player1Boost = self.__player1.getBoost()
        self.__status.player2Boost = self.__player2.getBoost()

        self.__clearField()
        # TODO return value is an address in C++
        return self.__status

    # TODO C++ return Pointer
    def move(self):
        if not self.__status.gameOver:
            self.__status.updateCount = 0
            self.__status.clearScreen = False

            self.__status.soundStatus = NO_SOUND
            player1Updated: bool = self.__updatePlayer(self.__player1, self.__joystick1)
            player2Updated: bool = self.__updatePlayer(self.__player2, self.__joystick2)

            self.__status.player1Boost = self.__player1.getBoost()
            self.__status.player2Boost = self.__player2.getBoost()

            # Has there been an update?
            if (player1Updated or player2Updated) and (not self.__status.gameOver):
                self.__maybeAbsorbItem()

                if not self.__status.clearScreen:
                    self.__setWinnerAfterValidMove(player1Updated, player2Updated)

                    if player1Updated:
                        self.__updateCell(self.__player1, True)
                    
                    if player2Updated:
                        self.__updateCell(self.__player2, True)

            self.__gameTicks += 1
        
        # TODO return value is an address in C++
        return self.__status

    def getWinner(self) -> int:
        return self.__winner
