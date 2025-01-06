import random
import time

from CoinDetection import CoinDetection
from Display import Display
from Game import Game
from Joystick import Joystick
from MainClock import MainClock
from StartButton import StartButton

CONSOLE_STATE_COIN = 0
CONSOLE_STATE_DEMO = 1
CONSOLE_STATE_GAME = 2

COIN_MOVEMENT_DELAY = 10
COIN_MOVEMENT_FRAME_MAX = 14


class Console:
    def __init__(self):
        # Instanzen von Komponenten initialisieren
        self._joystickLeft = Joystick()
        self._joystickRight = Joystick()
        self._display = Display()
        self._mainClock = MainClock()
        self._state = CONSOLE_STATE_COIN
        self._games = [None for _ in range(10)]  # Liste für Spiele
        self._gameCount = 0
        self._gameindex = 0
        self._coinMovementDelay = 0
        self._coinMovementFrame = 0

    def init(self):
        """Initialisierung aller Komponenten."""
        self._gameCount = 0
        self._gameindex = 0
        self._state = CONSOLE_STATE_COIN

        # Joysticks initialisieren
        self._joystickLeft.init({"left": 17, "up": 27, "right": 22, "down": 10, "buttonTop": 9, "buttonBody": 11})
        self._joystickRight.init({"left": 5, "up": 6, "right": 13, "down": 19, "buttonTop": 26, "buttonBody": 21})

        # Display und Komponenten starten
        self._display.init()
        random.seed(int(time.time()))
        StartButton.init()
        self._mainClock.startTimer()
        CoinDetection.init()

    def process(self):
        """Zentrale Verarbeitungslogik."""
        if self._mainClock.isTick():
            self._joystickLeft.process()
            self._joystickRight.process()

        if self._state == CONSOLE_STATE_COIN:
            self.displayCoinAnimation()
            if CoinDetection.startGame():
                self._state = CONSOLE_STATE_DEMO
        elif self._state == CONSOLE_STATE_DEMO:
            self.stateDemo()
        elif self._state == CONSOLE_STATE_GAME:
            current_game = self._games[self._gameindex]
            if current_game:
                current_game.process()
                if current_game.getState() == Game.GAME_STATE_PLAY_DEMO:
                    self._state = CONSOLE_STATE_COIN

    def addGame(self, newGame: Game):
        """Fügt ein neues Spiel zur Liste hinzu."""
        if self._gameCount < len(self._games):
            self._games[self._gameCount] = newGame
            self._gameCount += 1

    def stateDemo(self):
        """Verwaltet den Demo-Zustand der Konsole."""
        if self._joystickLeft.getControlStatus("left") or self._joystickRight.getControlStatus("left"):
            self._gameindex = (self._gameindex - 1) % self._gameCount

        if self._joystickLeft.getControlStatus("right") or self._joystickRight.getControlStatus("right"):
            self._gameindex = (self._gameindex + 1) % self._gameCount

        current_game = self._games[self._gameindex]
        if current_game:
            current_game.process()
            if current_game.getState() == Game.GAME_STATE_CONFIG:
                self._state = CONSOLE_STATE_GAME

    def displayCoinAnimation(self):
        """Zeigt die Münzanimation an."""
        self._coinMovementDelay += 1
        if self._coinMovementDelay < COIN_MOVEMENT_DELAY:
            return

        self._coinMovementDelay = 0
        coinXPos = 18 - self._coinMovementFrame

        # Animation zeichnen
        Display.clear()
        Display.drawRect(7, 1, 4, 14, Display.get_color(255, 255, 255))  # Weißer Rand
        Display.fillCircle(coinXPos, 8, 5, Display.get_color(255, 165, 0))  # Orange Münze
        Display.fillRect(0, 0, 7, 16, Display.get_color(0, 0, 0))  # Hintergrund
        Display.refresh()

        self._coinMovementFrame = (self._coinMovementFrame + 1) % (COIN_MOVEMENT_FRAME_MAX + 1)

    def getJoystick(self, index: int) -> Joystick:
        """Gibt den gewünschten Joystick zurück."""
        return self._joystickRight if index == 1 else self._joystickLeft
