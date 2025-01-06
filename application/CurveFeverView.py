import CurveFeverLogic
import Display
import NumericDisplay
import Sound


EMPTY_COLOR = Display.Display.getColorFrom333(0, 0, 0)
PLAYER_1_COLOR_1 = Display.Display.getColorFrom333(7, 0, 0)
PLAYER_1_COLOR_2 = Display.Display.getColorFrom333(4, 0, 0)
PLAYER_2_COLOR_1 = Display.Display.getColorFrom333(0, 7, 0)
PLAYER_2_COLOR_2 = Display.Display.getColorFrom333(0, 4, 0)
ITEM_1_COLOR = Display.Display.getColorFrom333(0, 0, 7)
ITEM_2_COLOR = Display.Display.getColorFrom333(0, 2, 2)
ITEM_3_COLOR = Display.Display.getColorFrom333(3, 3, 3)


class CurveFeverView:
    @staticmethod
    def __getColorOfState(state: int) -> int:
        """
        Liefert die Farbe basierend auf dem Zustand der Zelle.
        """
        if state == CurveFeverLogic.STATE_PLAYER_1:
            return PLAYER_1_COLOR_1
        elif state == CurveFeverLogic.STATE_PLAYER_2:
            return PLAYER_2_COLOR_1
        elif state == CurveFeverLogic.STATE_ITEM_SLOW:
            return ITEM_1_COLOR
        elif state == CurveFeverLogic.STATE_ITEM_WALL:
            return ITEM_2_COLOR
        elif state == CurveFeverLogic.STATE_ITEM_CLEAR:
            return ITEM_3_COLOR
        elif state == CurveFeverLogic.STATE_TAIL_1:
            return PLAYER_1_COLOR_2
        elif state == CurveFeverLogic.STATE_TAIL_2:
            return PLAYER_2_COLOR_2
        return EMPTY_COLOR

    def printGameName(self, name: str):
        """
        Zeigt den Namen des Spiels an.
        """
        nameColor = Display.Display.getColorFrom333(2, 0, 2)
        Display.Display.drawText(name, 4, 4, nameColor, 1)
        Display.Display.refresh()

    def updatePixels(self, cells: list, cellCount: int):
        """
        Aktualisiert die Pixel basierend auf den Zelländerungen.
        """
        for j in range(2):  # Zweimaliges Zeichnen für Anzeige-Stabilität
            for i in range(cellCount):
                cell = cells[i]
                Display.Display.drawPixel(cell.x, cell.y, self.__getColorOfState(cell.state))

            if j == 0:
                Display.Display.refresh()

    def clearScreen(self):
        """
        Löscht den Bildschirm.
        """
        Display.Display.clearDisplay()
        Display.Display.refresh()

    def setBoost(self, player: int, boost: int):
        """
        Zeigt den Boost-Wert für den Spieler an.
        """
        display = NumericDisplay.DISPLAY_LEFT if player == CurveFeverLogic.PLAYER_1 else NumericDisplay.DISPLAY_RIGHT
        NumericDisplay.NumericDisplay.displayValue(display, boost)

    def setTime(self, time: int):
        """
        Zeigt die verbleibende Zeit an.
        """
        NumericDisplay.NumericDisplay.displayTime(NumericDisplay.DISPLAY_MIDDLE, time)

    def printWinner(self, winner: int):
        """
        Zeigt den Gewinner des Spiels an.
        """
        value = 0
        output = "Draw!"
        color = Display.Display.getColorFrom333(7, 7, 7)  # Weiß

        if winner == CurveFeverLogic.PLAYER_1:
            value = 60 * 11 + 11
            output = "P1 Wins!"
            color = PLAYER_1_COLOR_1
        elif winner == CurveFeverLogic.PLAYER_2:
            value = 60 * 22 + 22
            output = "P2 Wins!"
            color = PLAYER_2_COLOR_1

        NumericDisplay.NumericDisplay.displayTime(NumericDisplay.DISPLAY_LEFT, value)
        NumericDisplay.NumericDisplay.displayTime(NumericDisplay.DISPLAY_MIDDLE, value)
        NumericDisplay.NumericDisplay.displayTime(NumericDisplay.DISPLAY_RIGHT, value)
        Display.Display.drawText(output, 1, 1, color, 1)

    def playSound(self, soundId: int):
        """
        Spielt den entsprechenden Sound basierend auf der Sound-ID.
        """
        for i in range(0, 256, 5):
            if soundId == Sound.SOUND_ITEM_COLLECT:
                Sound.Sound.playSoundDura(i, 9, 100)
            elif soundId == Sound.SOUND_ITEM_ACTIVATE:
                Sound.Sound.playSoundDura(255 - i, 9, 100)
            elif soundId == Sound.SOUND_GAMEOVER:
                Sound.Sound.playSoundDura(60, 9, 100)
