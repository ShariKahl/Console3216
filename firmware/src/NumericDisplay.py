from SevenSegmentDisplay import SevenSegmentDisplay

# Display-IDs
DISPLAY_LEFT = 0
DISPLAY_MIDDLE = 1
DISPLAY_RIGHT = 2

# Initialisierungswerte für die Displays
DISPLAY_LEFT_INIT = 0x72
DISPLAY_MIDDLE_INIT = 0x71
DISPLAY_RIGHT_INIT = 0x70


class NumericDisplay:
    _leftDisplay: SevenSegmentDisplay = SevenSegmentDisplay()
    _middleDisplay: SevenSegmentDisplay = SevenSegmentDisplay()
    _rightDisplay: SevenSegmentDisplay = SevenSegmentDisplay()

    def __init__(self):
        """
        Initialisiert die drei sieben-Segment-Anzeigen.
        """
        self._leftDisplay.init(DISPLAY_LEFT_INIT)
        self._middleDisplay.init(DISPLAY_MIDDLE_INIT)
        self._rightDisplay.init(DISPLAY_RIGHT_INIT)
        print("NumericDisplay initialized.")

    @classmethod
    def __getDisplay(cls, display: int) -> SevenSegmentDisplay:
        """
        Gibt das entsprechende Display-Objekt zurück.
        :param display: Display-ID (DISPLAY_LEFT, DISPLAY_MIDDLE, DISPLAY_RIGHT)
        :return: Das entsprechende SevenSegmentDisplay-Objekt
        """
        if display == DISPLAY_LEFT:
            return cls._leftDisplay
        elif display == DISPLAY_MIDDLE:
            return cls._middleDisplay
        elif display == DISPLAY_RIGHT:
            return cls._rightDisplay
        else:
            print(f"Invalid display ID: {display}")
            return None

    @classmethod
    def test(cls):
        """
        Testet die Anzeigen mit vordefinierten Werten.
        """
        cls._leftDisplay.setNumber(190)
        cls._middleDisplay.setNumber(191)
        cls._rightDisplay.setNumber(192)
        print("Test values set on displays.")

    @classmethod
    def displayTime(cls, display: int, seconds: int):
        """
        Zeigt eine Zeit auf einem der Displays an.
        :param display: Display-ID (DISPLAY_LEFT, DISPLAY_MIDDLE, DISPLAY_RIGHT)
        :param seconds: Zeit in Sekunden
        """
        actualDisplay: SevenSegmentDisplay = cls.__getDisplay(display)

        if actualDisplay is None:
            return

        minutes = seconds // 60
        remaining_seconds = seconds % 60
        actualDisplay.setNumber(minutes * 100 + remaining_seconds)

        if seconds % 2 == 1:
            actualDisplay.setColon()
        else:
            actualDisplay.clearColon()
        print(f"Time displayed on {display}: {minutes}:{remaining_seconds:02}")

    @classmethod
    def displayValue(cls, display: int, value: int):
        """
        Zeigt einen numerischen Wert auf einem der Displays an.
        :param display: Display-ID (DISPLAY_LEFT, DISPLAY_MIDDLE, DISPLAY_RIGHT)
        :param value: Anzuzeigender Wert
        """
        actualDisplay: SevenSegmentDisplay = cls.__getDisplay(display)

        if actualDisplay is None:
            return

        actualDisplay.setNumber(value)
        print(f"Value displayed on {display}: {value}")
