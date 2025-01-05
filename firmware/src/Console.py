
import random
import time

from Microcontroller import *
from CoinDetection import *
from Display import *
from Game import *
from Joystick import *
from MainClock import *
from RgbLed import *
from StartButton import *

CONSOLE_STATE_COIN = 0
CONSOLE_STATE_DEMO = 1
CONSOLE_STATE_GAME = 2

# TODO Globaler Pointer
# C++ Game *game;
game: Game = None

color: int = 0

COIN_MOVEMENT_DELAY = 10
COIN_MOVEMENT_FRAME_MAX = 14

class Console:
    def __init__(self):
        # TODO GPIO setup eventuell hierhin verschieben, CoinDetection.py
        self._joystickLeft: Joystick = Joystick()
        self._joystickRight: Joystick = Joystick()

        self._rgbLed: RgbLed = RgbLed()

        self._display: Display = Display()

        self._mainClock: MainClock = MainClock()

        self._state: int = 0

        # TODO Pointer
        # C++: Game * games[10];
        # Leeres, 10 Elemente großes Array wird angelegt
        self._games = [None for _ in range(10)]

        self._gameCount: int = 0
        self._gameindex: int = 0

        # TODO Pointer
        # C++: Game * actualGame;
        self._actualGame: Game = None

        # TODO auf 12 Bits beschränken
        # C++: uint16_t coinMovementDelay:12;
        self._coinMovementDelay: int = 0

        # TODO auf 4 Bits beschränken
        # C++: uint16_t coinMovementFrame:4;
        self._coinMovementFrame: int = 0

    def init(self):
        self._gameCount = 0
        self._gameindex = 0
        self._state = CONSOLE_STATE_COIN

        # Ursprungscode hatte einen Tippfehler im Namen:
        # C++: JoystickPins_t joyctickPins;
        # TODO split for Python
        joystickPinsLeft: JoystickPins_t = JoystickPins_t()

        joystickPinsLeft.left = PIN_JOYSTICK_LEFT_LEFT
        joystickPinsLeft.up = PIN_JOYSTICK_LEFT_UP
        joystickPinsLeft.right = PIN_JOYSTICK_LEFT_RIGHT
        joystickPinsLeft.down = PIN_JOYSTICK_LEFT_DOWN
        joystickPinsLeft.buttonTop = PIN_JOYSTICK_LEFT_BUTTON_TOP
        joystickPinsLeft.buttonBody = PIN_JOYSTICK_LEFT_BUTTON_BODY

        # TODO Übergabe als Referenz in C++
        # C++: this->joystickLeft.init(&joyctickPins);
        self._joystickLeft.init(joystickPinsLeft)

        # TODO split for Python
        joystickPinsRight: JoystickPins_t = JoystickPins_t()

        joystickPinsRight.left = PIN_JOYSTICK_RIGHT_LEFT
        joystickPinsRight.up = PIN_JOYSTICK_RIGHT_UP
        joystickPinsRight.right = PIN_JOYSTICK_RIGHT_RIGHT
        joystickPinsRight.down = PIN_JOYSTICK_RIGHT_DOWN
        joystickPinsRight.buttonTop = PIN_JOYSTICK_RIGHT_BUTTON_TOP
        joystickPinsRight.buttonBody = PIN_JOYSTICK_RIGHT_BUTTON_BODY

        # TODO Übergabe als Referenz in C++
        # C++: this->joystickRight.init(&joyctickPins);
        self._joystickRight.init(joystickPinsRight)

        self._display.init()

        # TODO
        # C++: randomSeed(analogRead(0));
        random.seed(int(time.time()))
        
        StartButton.init()

        self._mainClock.startTimer()

        CoinDetection.init()

    def process(self):
        if (self._mainClock.isTick()):
            self._joystickLeft.process()
            self._joystickRight.process()
            color += 1
            # TODO Auskommentierte Zeile
            # C++: Serial.println(color);
            # Serial.println(color)
        
        # C++ Switch zu if/else umgewandelt
        if (self._state == CONSOLE_STATE_COIN):
            self.displayCoinAnimation()

            if (CoinDetection.startGame()):
                self._state = CONSOLE_STATE_DEMO
        elif (self._state == CONSOLE_STATE_DEMO):
            self.stateDemo()
        elif (self._state == CONSOLE_STATE_GAME):
            self._games[self._gameindex].process()
            if (self._games[self._gameindex].getState() == GAME_STATE_PLAY_DEMO):
                self._state = CONSOLE_STATE_COIN
        
        # TODO Funktionsaufruf, eventuell nicht mehr benötigt
        # C++: random();
        # random.random()

        # TODO Auskommentierte Zeile
        # C++: Serial.println("alive");

    def addGame(self, newGame: Game):
        # In C++ mit this->gameCount++ post-incrementiert
        self._games[self._gameCount] = newGame
        self._gameCount += 1

    def stateDemo(self):
        if ((self._joystickLeft.getControlStatus(JOYSTICK_SWITCH_LEFT) == JOYSTICK_STATUS_PRESSED) or
            (self._joystickRight.getControlStatus(JOYSTICK_SWITCH_LEFT) == JOYSTICK_STATUS_PRESSED)):
            self._gameindex -= 1
            if (self._gameindex < 0):
                self._gameindex = self._gameCount - 1
        
        if ((self._joystickLeft.getControlStatus(JOYSTICK_SWITCH_RIGHT) == JOYSTICK_STATUS_PRESSED) or
            (self._joystickRight.getControlStatus(JOYSTICK_SWITCH_RIGHT) == JOYSTICK_STATUS_PRESSED)):
            self._gameindex += 1
            if (self._gameindex > (self._gameCount - 1)):
                self._gameindex = 0
        
        self._games[self._gameindex].process()
        if (self._games[self._gameindex].getState() == GAME_STATE_CONFIG):
            self._state = CONSOLE_STATE_GAME

    def displayCoinAnimation(self):
        self._coinMovementDelay += 1

        if (self._coinMovementDelay < COIN_MOVEMENT_DELAY):
            return
        
        self._coinMovementDelay = 0
        coinXPos = 18 - self._coinMovementFrame

        Display.clearDisplay()
        # TODO These methods do not exist in Python or are in a different place
        Display.drawRect(7, 1, 4, 14, Display.getColorFrom333(7, 7, 7))
        Display.fillCircle(coinXPos, 8, 5, Display.getColorFrom333(7, 4, 0))
        Display.fillRect(0, 0, 7, 16, Display.getColorFrom333(0, 0, 0))
        Display.drawLine(7, 1, 7, 14, Display.getColorFrom333(7, 7, 7))
        Display.refresh()

        self._coinMovementFrame += 1

        if (self._coinMovementFrame > COIN_MOVEMENT_FRAME_MAX):
            self._coinMovementFrame = 0

    def getJoystick(self, index: int) -> Joystick:
        # C++ Switch zu if/else umgewandelt
        if (index == 1):
            return self._joystickRight
        else:
            return self._joystickLeft

    @classmethod
    def checkMem(self):
        # Original C++ Methode:
        # void Console::checkMem()
        # { 

        #     uint8_t * t;
        #     t = malloc(1);
        #     Serial.print("mem : ");
        #     Serial.println((uint32_t)t,HEX);
        #     free(t);

        #     uint8_t a;
        #     Serial.print("heap : ");
        #     Serial.println((uint32_t)&a,HEX);
        # }

        # Die Methode macht nur ein wenig mit Speicher rum und gibt was aus.
        # Unwichtig für die Ausführung.
        pass
