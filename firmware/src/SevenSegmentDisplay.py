from Ht16k33 import Ht16k33

# Zahlen- und Segmenttabelle
numbertable = [
    0x3F,  # 0
    0x06,  # 1
    0x5B,  # 2
    0x4F,  # 3
    0x66,  # 4
    0x6D,  # 5
    0x7D,  # 6
    0x07,  # 7
    0x7F,  # 8
    0x6F,  # 9
    0x77,  # a
    0x7C,  # b
    0x39,  # C
    0x5E,  # d
    0x79,  # E
    0x71,  # F
]

# Positionen der Segmente
SEVEN_SEGMENT_POS = [8, 6, 2, 0]

# Masken für Punkte und Doppelpunkte
SEVEN_SEGMENT_DOT_MASK = (1 << 7)
SEVEN_SEG_COLON_MASK = 0x2


class SevenSegmentDisplay(Ht16k33):
    def setNumberAt(self, number: int, position: int):
        """
        Setzt eine Zahl an eine bestimmte Position.
        :param number: Zahl (0-9)
        :param position: Position (0-3)
        """
        self._dataBuffer[SEVEN_SEGMENT_POS[position]] = numbertable[number]
        print(f"Set number {number} at position {position}")

    def setSegmentsAt(self, segments: int, position: int):
        """
        Setzt bestimmte Segmente an eine Position.
        :param segments: Segmentwert
        :param position: Position (0-3)
        """
        self._dataBuffer[SEVEN_SEGMENT_POS[position]] = segments
        print(f"Set segments {segments:#x} at position {position}")

    def clearDotAt(self, position: int):
        """
        Entfernt den Punkt an der angegebenen Position.
        :param position: Position (0-3)
        """
        self._dataBuffer[SEVEN_SEGMENT_POS[position]] &= ~SEVEN_SEGMENT_DOT_MASK
        print(f"Cleared dot at position {position}")

    def setDotAt(self, position: int):
        """
        Setzt den Punkt an der angegebenen Position.
        :param position: Position (0-3)
        """
        self._dataBuffer[SEVEN_SEGMENT_POS[position]] |= SEVEN_SEGMENT_DOT_MASK
        print(f"Set dot at position {position}")

    def setColon(self):
        """
        Aktiviert die Doppelpunkte.
        """
        self._dataBuffer[4] = SEVEN_SEG_COLON_MASK
        print("Colon set")

    def clearColon(self):
        """
        Deaktiviert die Doppelpunkte.
        """
        self._dataBuffer[4] = 0
        print("Colon cleared")

    def toggleColon(self):
        """
        Wechselt den Status der Doppelpunkte.
        """
        self._dataBuffer[4] ^= SEVEN_SEG_COLON_MASK
        print("Colon toggled")

    def setNumber(self, value: int):
        """
        Zeigt eine Zahl (bis zu 4 Stellen) auf der Anzeige an.
        :param value: Zahl, die angezeigt werden soll
        """
        bcdValue: int = 0

        for index in range(13, -1, -1):
            if (bcdValue & 0xF) >= 5:
                bcdValue += 3
            if (bcdValue & 0xF0) >= (5 << 4):
                bcdValue += (3 << 4)
            if (bcdValue & 0xF00) >= (5 << 8):
                bcdValue += (3 << 8)

            bcdValue = (bcdValue << 1) | ((value >> index) & 1)

        self._dataBuffer[SEVEN_SEGMENT_POS[0]] = numbertable[bcdValue & 0xF]
        self._dataBuffer[SEVEN_SEGMENT_POS[1]] = numbertable[(bcdValue & 0xF0) >> 4]
        self._dataBuffer[SEVEN_SEGMENT_POS[2]] = numbertable[(bcdValue & 0xF00) >> 8]
        self._dataBuffer[SEVEN_SEGMENT_POS[3]] = numbertable[(bcdValue & 0xF000) >> 12]

        self.refresh()
        print(f"Displayed number: {value}")
