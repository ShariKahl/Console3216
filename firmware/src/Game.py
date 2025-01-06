from time import sleep
from Joystick import Joystick
from NumericDisplay import NumericDisplay
from MainClock import MainClock
from StartButton import StartButton
from Display import Display

# Spielzustände
GAME_STATE_PREPARE_DEMO = 0
GAME_STATE_PLAY_DEMO = 1
GAME_STATE_CONFIG = 2
GAME_STATE_PLAY = 3
GAME_STATE_SCORE = 4
GAME_STATE_HIGHSCORE_GRAPHIC = 5
GAME_STATE_HIGHSCORE_NEW = 6
GAME_STATE_HIGHSCORE_NAME = 7
GAME_STATE_DISPLAY_HIGHSCORES = 8
GAME_STATE_END = 9

# Spielertypen
PLAYER_TYPE_HUMAN = 0
PLAYER_TYPE_AI_0 = 1
PLAYER_TYPE_AI_9 = 10

# Maximale Länge des Spielnamens
GAME_NAME_MAX_LENGTH = 6


class Score_t:
    """Datenstruktur für Highscores."""
    def __init__(self, score=0, name="   "):
        self.score: int = score
        self.name: str = name


class Game:
    def __init__(self, leftJoystick: Joystick, rightJoystick: Joystick, gameName: str):
        self._joystickLeft: Joystick = leftJoystick
        self._joystickRight: Joystick = rightJoystick
        self._name: str = gameName[:GAME_NAME_MAX_LENGTH]
        self._state: int = GAME_STATE_PREPARE_DEMO
        self._time: int = 0
        self._player1Type: int = PLAYER_TYPE_HUMAN
        self._player2Type: int = PLAYER_TYPE_AI_0
        self._startButtonStatus: int = 0
        self._currentScore = Score_t(0, "   ")
        self._Highscores = [Score_t() for _ in range(3)]
        self.__isHighscore: int = -1
        self.__click_Count: int = 0

    def process(self):
        """Verarbeitet den aktuellen Spielzustand."""
        if self._state == GAME_STATE_PREPARE_DEMO:
            self._prepareDemo()
            self._state = GAME_STATE_PLAY_DEMO
        elif self._state == GAME_STATE_PLAY_DEMO:
            if StartButton.getStatus() == StartButton.START_BUTTON_PRESSED:
                self._state = GAME_STATE_CONFIG
        elif self._state == GAME_STATE_CONFIG:
            self._configMultiplayerGame()
            if StartButton.getStatus() == StartButton.START_BUTTON_PRESSED:
                self._prepareGame()
                self._state = GAME_STATE_PLAY
        elif self._state == GAME_STATE_PLAY:
            self._playGame()
        elif self._state == GAME_STATE_SCORE:
            self.__submitHighscore()
            if self.__isHighscore < 0:
                self._state = GAME_STATE_DISPLAY_HIGHSCORES
            else:
                self._state = GAME_STATE_HIGHSCORE_GRAPHIC
        elif self._state == GAME_STATE_HIGHSCORE_GRAPHIC:
            self._displayNewHighscore()
            if StartButton.getStatus() == StartButton.START_BUTTON_PRESSED:
                self._state = GAME_STATE_HIGHSCORE_NAME
        elif self._state == GAME_STATE_HIGHSCORE_NAME:
            self.__enterName(self._Highscores[self.__isHighscore])
        elif self._state == GAME_STATE_DISPLAY_HIGHSCORES:
            self._displayHighscores()
            if StartButton.getStatus() == StartButton.START_BUTTON_PRESSED:
                self.__click_Count = 0
                self._state = GAME_STATE_PREPARE_DEMO
        elif self._state == GAME_STATE_END:
            self._gameOver()
            if StartButton.getStatus() == StartButton.START_BUTTON_PRESSED:
                self._state = GAME_STATE_PREPARE_DEMO

        self._timeCountUp()

    def _prepareDemo(self):
        """Bereitet die Demo-Ansicht vor."""
        Display.clear()
        Display.drawText("DEMO", 10, 10, Display.get_color(255, 255, 0), 1)
        Display.refresh()

    def _playGame(self):
        """Spielt das eigentliche Spiel."""
        Display.clear()
        Display.drawText("PLAY", 10, 10, Display.get_color(0, 255, 0), 1)
        Display.refresh()

    def _gameOver(self):
        """Zeigt das Spielende an."""
        textColor = Display.get_color(255, 0, 0)
        Display.clear()
        Display.drawText("GAME", 4, 0, textColor, 1)
        Display.drawText("OVER", 4, 8, textColor, 1)
        Display.refresh()

    def __submitHighscore(self):
        """Prüft und fügt neue Highscores hinzu."""
        for i in range(3):
            if self._currentScore.score > self._Highscores[i].score:
                self._Highscores.insert(i, self._currentScore)
                self._Highscores.pop()
                self.__isHighscore = i
                return
        self.__isHighscore = -1

    def __enterName(self, score: Score_t):
        """Ermöglicht das Eingeben eines Highscore-Namens."""
        # Name-Eingabe-Logik hier implementieren
        pass

    def _displayHighscores(self):
        """Zeigt die Highscores an."""
        Display.clear()
        for i, highscore in enumerate(self._Highscores):
            Display.drawText(f"{i+1}. {highscore.name}", 5, i * 10, Display.get_color(255, 255, 255), 1)
        Display.refresh()

    def setState(self, newState: int):
        self._state = newState

    def getState(self):
        return self._state
