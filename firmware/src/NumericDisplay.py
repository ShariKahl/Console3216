
from SevenSegmentDisplay import *

DISPLAY_LEFT = 0
DISPLAY_MIDDLE = 1
DISPLAY_RIGHT = 2

DISPLAY_LEFT_INIT = 0x72
DISPLAY_MIDDLE_INIT = 0x71
DISPLAY_RIGHT_INIT = 0x70

class NumericDisplay:
    _leftDisplay: SevenSegmentDisplay = SevenSegmentDisplay()
    _middleDisplay: SevenSegmentDisplay = SevenSegmentDisplay()
    _rightDisplay: SevenSegmentDisplay = SevenSegmentDisplay()

    def __init__(self) -> None:
        # TODO C++ Quellcode:
        # Wire.setClock(400000L);
        # Aus Arduino Wire.h

        # TODO War so im original C++ Quellcode, 3x leftDisplay.init()
        # Eventuell ein Bug und die anderen müssen auch initialisiert werden
        # self._leftDisplay.init(DISPLAY_LEFT_INIT)
        # self._leftDisplay.init(DISPLAY_MIDDLE_INIT)
        # self._leftDisplay.init(DISPLAY_RIGHT_INIT)
        self._leftDisplay.init(DISPLAY_LEFT_INIT)
        self._middleDisplay.init(DISPLAY_MIDDLE_INIT)
        self._rightDisplay.init(DISPLAY_RIGHT_INIT)
        
    # Hilfsmethode
    @classmethod
    def __getDisplay(cls, display) -> SevenSegmentDisplay:
        if display == DISPLAY_LEFT:
            # TODO in C++ wird Speicheradresse übergeben:
            # actualDisplay = & NumericDisplay::leftDisplay;
            return cls._leftDisplay
        elif display == DISPLAY_MIDDLE:
            # TODO in C++ wird Speicheradresse übergeben:
            # actualDisplay = & NumericDisplay::middleDisplay;
            return cls._middleDisplay
        elif display == DISPLAY_RIGHT:
            # TODO in C++ wird Speicheradresse übergeben:
            # actualDisplay = & NumericDisplay::rightDisplay;
            return cls._rightDisplay
        return None

    @classmethod
    def test(cls):
        cls._leftDisplay.init(DISPLAY_LEFT_INIT)
        cls._middleDisplay.init(DISPLAY_MIDDLE_INIT)
        cls._rightDisplay.init(DISPLAY_RIGHT_INIT)

        cls._leftDisplay.setNumber(190)
        cls._middleDisplay.setNumber(191)
        cls._rightDisplay.setNumber(192)

    @classmethod
    def displayTime(cls, display: int, seconds: int):
        # TODO In C++ ein Pointer:
        # SevenSegmentDisplay * actualDisplay;
        actualDisplay: SevenSegmentDisplay = cls.__getDisplay(display)
        
        if actualDisplay == None:
            return

        minutes = int(seconds / 60)
        seconds = seconds % 60
        
        actualDisplay.setNumber(minutes * 100 + seconds)

        if seconds & 1:
            actualDisplay.setColon()
        else:
            actualDisplay.clearColon()

    @classmethod
    def displayValue(cls, display: int, value: int):
        # TODO In C++ ein Pointer:
        # SevenSegmentDisplay * actualDisplay;
        actualDisplay: SevenSegmentDisplay = cls.__getDisplay(display)
        
        if actualDisplay == None:
            return
        
        actualDisplay.setNumber(value)
