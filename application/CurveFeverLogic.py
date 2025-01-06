import random
import CurveFeverPlayer
import Joystick

FIELD_HEIGHT = 16
FIELD_WIDTH = 32
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


class CellUpdate:
    def __init__(self):
        self.x: int = 0
        self.y: int = 0
        self.state: int = STATE_EMPTY


class GameStatus:
    def __init__(self):
        self.gameOver: bool = False
        self.clearScreen: bool = True
        self.cellUpdates: list[CellUpdate] = []
        self.updateCount: int = 0
        self.soundStatus: int = NO_SOUND
        self.player1Boost: int = 0
        self.player2Boost: int = 0


class Logic:
    def __init__(self):
        self.__joystick1: Joystick.Joystick = None
        self.__joystick2: Joystick.Joystick = None
        self.__cellUpdates = [CellUpdate() for _ in range(MAX_CHANGE_COUNT)]
        self.__status: GameStatus = GameStatus()
        self.__player1: CurveFeverPlayer.Player = CurveFeverPlayer.Player()
        self.__player2: CurveFeverPlayer.Player = CurveFeverPlayer.Player()
        self.__winner: int = DRAW
        self.__currentItem: int = CurveFeverPlayer.NO_ITEM
        self.__itemPosition: CurveFeverPlayer.Position = CurveFeverPlayer.Position(0, 0)
        self.__gameTicks: int = 0
        self.__field = [[STATE_EMPTY for _ in range(FIELD_HEIGHT)] for _ in range(FIELD_WIDTH)]

    def __getCellState(self, x: int, y: int) -> int:
        return self.__field[x][y]

    def __setCellState(self, x: int, y: int, state: int, publish: bool = False):
        self.__field[x][y] = state
        if publish:
            update = self.__cellUpdates[self.__status.updateCount]
            update.x = x
            update.y = y
            update.state = state
            self.__status.updateCount += 1

    def __clearField(self):
        self.__status.clearScreen = True
        self.__status.updateCount = 0

        for i in range(FIELD_WIDTH):
            for j in range(FIELD_HEIGHT):
                self.__field[i][j] = STATE_EMPTY

        self.__setCellState(self.__player1.getPosition().x, self.__player1.getPosition().y, STATE_PLAYER_1, True)
        self.__setCellState(self.__player2.getPosition().x, self.__player2.getPosition().y, STATE_PLAYER_2, True)

        if self.__currentItem != CurveFeverPlayer.NO_ITEM:
            self.__setCellState(self.__itemPosition.x, self.__itemPosition.y, STATE_ITEM_CLEAR, True)

    def __setDirectionForPlayer(self, player: CurveFeverPlayer.Player):
        joystick = self.__joystick1 if player.getName() == PLAYER_1 else self.__joystick2
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

    def __updatePlayer(self, player: CurveFeverPlayer.Player, joystick: Joystick.Joystick) -> bool:
        if not self.__updateOccursThisTick(player.getSpeed()):
            return False
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
                self.__clearField()

        if not player.update():
            self.__status.gameOver = True
            self.__winner = DRAW if self.__winner == DRAW else (PLAYER_2 if player.getName() == PLAYER_1 else PLAYER_1)
            return False

        return True

    def __maybeGenerateItem(self):
        if random.randint(0, 99) < PROBABILITY_ITEM_SLOW:
            self.__currentItem = CurveFeverPlayer.ITEM_SLOW
        elif random.randint(0, 99) < PROBABILITY_ITEM_WALL:
            self.__currentItem = CurveFeverPlayer.ITEM_WALL
        elif random.randint(0, 99) < PROBABILITY_ITEM_CLEAR:
            self.__currentItem = CurveFeverPlayer.ITEM_CLEAR
        else:
            self.__currentItem = CurveFeverPlayer.NO_ITEM

    def initGame(self, p1_joystick: Joystick.Joystick, p2_joystick: Joystick.Joystick) -> GameStatus:
        self.__joystick1 = p1_joystick
        self.__joystick2 = p2_joystick
        self.__clearField()
        self.__player1.reset()
        self.__player1.setPosition(1, FIELD_HEIGHT // 2)
        self.__player1.setDirection(CurveFeverPlayer.RIGHT)
        self.__player2.reset()
        self.__player2.setPosition(FIELD_WIDTH - 2, FIELD_HEIGHT // 2)
        self.__player2.setDirection(CurveFeverPlayer.LEFT)
        return self.__status
