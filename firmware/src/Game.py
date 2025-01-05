
# TODO
# C++: #include <Arduino.h>

from time import sleep

from Joystick import *
from NumericDisplay import *
from MainClock import *
from StartButton import *
from Display import *


GAME_STATE_PREPARE_DEMO = 0
GAME_STATE_PLAY_DEMO = GAME_STATE_PREPARE_DEMO + 1

GAME_STATE_CONFIG = GAME_STATE_PLAY_DEMO + 1
GAME_STATE_PLAY = GAME_STATE_CONFIG + 1

GAME_STATE_SCORE = GAME_STATE_PLAY + 1
GAME_STATE_HIGHSCORE_GRAPHIC = GAME_STATE_SCORE + 1
GAME_STATE_HIGHSCORE_NEW = GAME_STATE_HIGHSCORE_GRAPHIC + 1
GAME_STATE_HIGHSCORE_NAME = GAME_STATE_HIGHSCORE_NEW + 1
GAME_STATE_DISPLAY_HIGHSCORES = GAME_STATE_HIGHSCORE_NAME + 1
GAME_STATE_END = GAME_STATE_DISPLAY_HIGHSCORES + 1

PLAYER_TYPE_HUMAN = 0
PLAYER_TYPE_AI_0 = 1
PLAYER_TYPE_AI_1 = 2
PLAYER_TYPE_AI_2 = 3
PLAYER_TYPE_AI_3 = 4
PLAYER_TYPE_AI_4 = 5
PLAYER_TYPE_AI_5 = 6
PLAYER_TYPE_AI_6 = 7
PLAYER_TYPE_AI_7 = 8
PLAYER_TYPE_AI_8 = 9
PLAYER_TYPE_AI_9 = 10

GAME_NAME_MAX_LENGHT = 6


# TODO Struct
# C++:
# typedef struct  {
#     uint16_t score;
#     char name[4];
# } Score_t;
class Score_t:
    def __init__(self, score, name) -> None:
        self.score: int = score
        self.name: str = name


class Game:
    # TODO gameName ist ein char Pointer in C++
    def __init__(self, leftJoystick: Joystick, rightJoystick: Joystick, gameName: str):
        # TODO Pointer
        # C++:  Joystick * joystickLeft;
        #       Joystick * joystickRight;
        self._joystickLeft: Joystick = leftJoystick
        self._joystickRight: Joystick = rightJoystick

        # C++: char name[GAME_NAME_MAX_LENGHT];
        # TODO Alter Code: self._name = [""] * GAME_NAME_MAX_LENGHT
        self._name: str = gameName

        self._state: int = GAME_STATE_PREPARE_DEMO
        self._time: int = 0

        # TODO Auf 4 Bits begrenzt
        # C++:  uint8_t player1Type:4;
        #       uint8_t player2Type:4;
        self._player1Type: int = PLAYER_TYPE_HUMAN
        self._player2Type: int = PLAYER_TYPE_AI_0

        # TODO Auf 2 Bits begrenzt
        # C++:  uint8_t startButtonStatus:2;
        self._startButtonStatus: int = 0

        self._currentScore = Score_t(0, "   ")

        # Diese Zeile erstellt ein Objekt mit 3 Referenzen darauf
        # FALSCH: self._Highscores = [Score_t(0, "   ")] * 3
        # Diese Zeile erstellt 3 Objekte die unabhängig von einander verändert werden können
        self._Highscores = Score_t(0, "   "), Score_t(0, "   "), Score_t(0, "   ")
        # C++: Score_t Highscores[3] = { {0, "   "}, {0, "   "}, {0, "   "} };

        self.__isHighscore: int = 0
        self.__click_Count: int = 0

        # TODO Serial nicht implementiert/importiert
        # C++ Code:
        # Serial.print("stick : ");
        # Serial.println((uint32_t) &leftJoystick, HEX);
        # Serial.println((uint32_t) &rightJoystick, HEX);

        # TODO C++:
        # for (uint8_t counter = 0; counter < GAME_NAME_MAX_LENGHT; counter++) {
        # this->name[counter] = *gameName++;
        # }
        # this->name[GAME_NAME_MAX_LENGHT - 1] = 0;
        # TODO gameName vorerst in str umgewandelt und einfach übernommen
        # for counter in range(0, GAME_NAME_MAX_LENGHT):
        #     self._name[counter] = gameName
        #     gameName += 1

        # self._name[-1] = 0

    # TODO BEGIN Virtuelle Methoden:
    def process(self):
        # In C++ ein Switch/Case
        if self._state == GAME_STATE_PREPARE_DEMO:
            self._prepareDemo()
            self._state = GAME_STATE_PLAY_DEMO
        elif self._state == GAME_STATE_PLAY_DEMO:
            if StartButton.getStatus() == START_BUTTON_PRESSED:
                self._state = GAME_STATE_CONFIG
        elif self._state == GAME_STATE_CONFIG:
            self._configMultiplayerGame()
            if StartButton.getStatus() == START_BUTTON_PRESSED:
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
            if StartButton.getStatus() == START_BUTTON_PRESSED:
                self._state = GAME_STATE_HIGHSCORE_NAME
        elif self._state == GAME_STATE_HIGHSCORE_NAME:
            self.__enterName(self._Highscores[self.__isHighscore])
        elif self._state == GAME_STATE_DISPLAY_HIGHSCORES:
            self._displayHighscores()
            if StartButton.getStatus() == START_BUTTON_PRESSED:
                self.__click_Count = 0
                self._state = GAME_STATE_PREPARE_DEMO
        elif self._state == GAME_STATE_END:
            self._gameOver()
            if StartButton.getStatus() == START_BUTTON_PRESSED:
                self._state = GAME_STATE_PREPARE_DEMO
    
        self._timeCountUp()

    def _draw(self):
        # TODO In C++ game.cpp leer
        pass

    def _play(self):
        # TODO In C++ game.cpp leer
        pass

    def _prepareDemo(self):
        # TODO In C++ game.cpp leer
        pass

    def _playDemo(self):
        # TODO In C++ game.cpp leer
        pass

    def _prepareGame(self):
        # TODO In C++ game.cpp leer
        pass

    def _playGame(self):
        # TODO In C++ game.cpp leer
        pass

    def _gameOver(self):
        # Farbe wird nicht mehr in 9 bit angegeben, sondern 24 bit (3x 255)
        # Umrechnung erfolgt wie folgt: 256 / 8 * x - 1
        # C++ Code:
        # uint16_t textColor;
        # textColor = Display::getColor(2, 2, 0);
        textColor = Display.getColorFrom333(2, 2, 0)
        Display.clearDisplay()
        Display.drawText("GAME", 4, 0, textColor, 1)
        Display.drawText("OVER", 4, 8, textColor, 1)

        Display.refresh()
        pass

    def _timeStart(self):
        self._time = 0
        pass

    def _timeCountUp(self):
        self._time += TIME_BASIS_MS
        pass

    def _displayNewHighscore(self):
        textColor = Display.getColorFrom333(2, 2, 0)
        Display.clearDisplay()
        Display.drawText("NEW HS", 4, 0, textColor, 1)

        Display.refresh()
        NumericDisplay.displayValue(1, self._currentScore.score)
        pass

    def _displayHighscores(self):
        for i in range(0, 3):
            NumericDisplay.displayValue(i, self._Highscores[i].score)

        # In C++ 3 Zeilen
        # NumericDisplay.displayValue(0, self._Highscores[0].score)
        # NumericDisplay.displayValue(1, self._Highscores[1].score)
        # NumericDisplay.displayValue(2, self._Highscores[2].score)

        # C++ Quellcode:
        # uint16_t textColor = Display::getColor(2, 2, 0);
        textColor = Display.getColorFrom333(2, 2, 0)

        if self._joystickLeft.isUp() or self._joystickRight.isUp() \
            or self._joystickLeft.isDown() or self._joystickRight.isDown():
            self.__click_Count += 1

        if self.__click_Count % 2 == 0:
            index = 1
        else:
            index = 2

        Display.clearDisplay()
        Display.drawText(f"{index}.", 1, 0, textColor, 1)
        Display.drawText(self._Highscores[index - 1].name, 14, 0, textColor, 1)
        Display.drawText(f"{index + 1}.", 1, 9, textColor, 1)
        Display.drawText(self._Highscores[index].name, 14, 9, textColor, 1)
        Display.refresh()

        # TODO C++ Quellcode:
        # delay(100);
        sleep(0.1)
        pass
    # TODO END Virtuelle Methoden

    def setState(self, newState: int):
        self._state = newState
        pass

    def getState(self):
        return self._state

    def _configMultiplayerGame(self):
        nameTextColor = Display.getColorFrom333(0, 2, 0)
        Display.clearDisplay()
        Display.drawText(self._name, 4, 0, nameTextColor, 1)

        self._player1Type = self._configurePlayer(0, self._joystickLeft, self._player1Type)
        self._player2Type = self._configurePlayer(1, self._joystickRight, self._player2Type)

        Display.refresh()
        pass

    def _configurePlayer(self, playerNr: int, joystick: Joystick, playerType: int) -> int:
        # C++ Quellcode:
        # char tmpString[3];
        tmpString = ["" for _ in range(3)]
        
        textColor = Display.getColorFrom333(2, 2, 0)

        if playerType == PLAYER_TYPE_HUMAN:
            Display.drawText("P", playerNr * 19, 8, textColor, 1)
        else:
            tmpString[0] = 'C'
            tmpString[1] = chr(playerType + 48)
            tmpString[2] = 0

            Display.drawText(tmpString, playerNr * 19, 8, textColor, 1)
        
        if joystick.isLeft() and playerType > 0:
            return playerType - 1
        
        if joystick.isLeft() and playerType < (PLAYER_TYPE_AI_9 - 1):
            return playerType + 1
        
        return playerType

    def __submitHighscore(self):
        for i in range(0, 3):
            if self._currentScore.score > self._Highscores[i].score:
                self.__insertHighscore(i)
                self.__isHighscore = i
                return
        self.__isHighscore = -1
        pass

    def __enterName(self, s: Score_t):
        # TODO s in C++ ein Pointer, wird innerhalb dieser Funktion geändert
        # Wird in Pythonals Referenz übergeben und ändert
        # sich deshalb auch ausßerhalb der Funktion
        # TODO Direkte Änderung eines Zeichens in Python nicht möglich
        # Diese Umweg-Lösung muss getestet werden
        if ord(s.name[self.__click_Count]) < ord('A'):
            s.name = s.name[0:self.__click_Count] + 'A' + s.name[self.__click_Count + 1:]
        if ord(s.name[self.__click_Count]) > ord('Z'):
            s.name = s.name[0:self.__click_Count] + 'Z' + s.name[self.__click_Count + 1:]
        
        if (self._joystickLeft.isButtonTop() or self._joystickRight.isButtonTop()):
            # C++ Quellcode:
            # s->name[click_Count]++;
            # s->name[click_Count] = (s->name[click_Count] - 'A') % 26 + 'A';
            char = chr((ord(s.name[self.__click_Count]) + 1 - ord('A')) % 26 + ord('A'))
            s.name = s.name[0:self.__click_Count] + char + s.name[self.__click_Count + 1:]
        elif self._joystickLeft.isDown() or self._joystickRight.isDown():
            # C++ Quellcode:
            # s->name[click_Count]--;
            # if (s->name[click_Count] < 'A') { s->name[click_Count] = 'Z'; }
            # s->name[click_Count] = (s->name[click_Count] - 'A') % 26 + 'A';
            if ord(s.name[self.__click_Count - 1]) < ord('A'):
                char = 'Z'
            else:
                char = chr((ord(s.name[self.__click_Count]) - 1) - ord('A') % 26 + ord('A'))
            s.name = s.name[0:self.__click_Count] + char + s.name[self.__click_Count + 1:]
        
        Display.clearDisplay()
        Display.drawText(s.name, 7, 4, Display.getColorFrom333(2, 2, 0), 1)
        Display.refresh()
        
        # TODO C++ Quellcode:
        # delay(100);
        # Aus Arduino.h, genaue Funktionalität unklar
        pass

    def __insertHighscore(self, i: int):
        self._Highscores[i].score = self._currentScore.score
        pass
