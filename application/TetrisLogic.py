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

        # Spielerinitialisierung
        self.playerLeft: TetrisPlayer.TetrisPlayer = None
        self.playerRight: TetrisPlayer.TetrisPlayer = None

        # Spielinitialisierung
        self.initializeGame()

    def __handleStatus(self, player: TetrisPlayer.TetrisPlayer):
        # Statusbehandlung der Spieler
        if player.getStatus() == TetrisPlayer.TetrisPlayerStatus.PLAYING:
            pass
        elif player.getStatus() == TetrisPlayer.TetrisPlayerStatus.LOST:
            self.__status = TetrisLogicStatus.ENDSCREEN

    def __drawBorders(self):
        # Zeichnet die Spielgrenzen
        for y in range(16):
            Display.Display.drawPixel(10, y, Display.Display.getColorFrom333(2, 0, 0))
            Display.Display.drawPixel(21, y, Display.Display.getColorFrom333(2, 0, 0))

    def update(self, delta: int):
        # Hauptspielupdate
        Display.Display.clearDisplay()

        # Spielstatus und Spielerupdates
        if self.__status == TetrisLogicStatus.UPDATING:
            self.__handleStatus(self.playerLeft)
            self.__handleStatus(self.playerRight)

            # Spieler aktualisieren und anzeigen
            self.playerLeft.update(delta)
            self.playerRight.update(delta)
            self.playerLeft.displayPlayerPoints(True)
            self.playerRight.displayPlayerPoints(False)

            # Grenzen zeichnen
            self.__drawBorders()

            # Nächste Tetrominos und Spieler zeichnen
            self.playerLeft.drawNextTetroms(12, 2)
            self.playerRight.drawNextTetroms(17, 2)

            # Spieler selbst zeichnen
            self.playerLeft.draw()
            self.playerRight.draw()

        elif self.__status == TetrisLogicStatus.ENDSCREEN:
            self.__drawBorders()
            self.playerLeft.draw()
            self.playerRight.draw()

        elif self.__status == TetrisLogicStatus.ENDGAME:
            # Bei Endgame nichts weiter tun
            pass

        Display.Display.refresh()

    def startButtonPressed(self):
        # Behandelt den Startknopf
        if self.__status == TetrisLogicStatus.UPDATING:
            self.__status = TetrisLogicStatus.ENDSCREEN
        elif self.__status == TetrisLogicStatus.ENDSCREEN:
            self.__status = TetrisLogicStatus.ENDGAME
        elif self.__status == TetrisLogicStatus.ENDGAME:
            pass

    def isGameEnd(self) -> bool:
        # Überprüft, ob das Spiel zu Ende ist
        return self.__status == TetrisLogicStatus.ENDGAME

    def isEndScreen(self) -> bool:
        # Überprüft, ob das Endbildschirm angezeigt wird
        return self.__status == TetrisLogicStatus.ENDSCREEN

    def initializeGame(self):
        # Initialisiert das Spiel
        NumericDisplay.NumericDisplay.test()
        self.playerLeft = TetrisPlayer.TetrisPlayer(0, 0)
        self.playerRight = TetrisPlayer.TetrisPlayer(22, 0)
        self.__status = TetrisLogicStatus.UPDATING

    def resetGame(self):
        # Setzt das Spiel zurück
        self.playerLeft.reset()
        self.playerRight.reset()
