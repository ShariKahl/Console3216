from enum import Enum

# TODO #include "Arduino.h"

class CoinDetection:
    # to check if a coin signal appear. - merke den zustand der letzten flanke
    coinToggle: bool = False
    # to save the time how long the coin signal toggles
    timer: int = 0

    class coin(Enum):
        cent5 = 0
        cent10 = 1
        cent20 = 2
        cent0 = 3

    def __init__(self) -> None:
        # TODO const volatile uint8_t pulse1 = 4;
        # the flank nr for coin1 (coin 1 = 1 pulse = 2 flanks = 1x high + 1x low flank)
        self._pulse1: int = 4

        # TODO const volatile uint8_t pulse2 = 6;
        # ... for coin 2
        self._pulse2: int = 6

        # TODO const volatile uint8_t pulse3 = 8;
        # ... place holder for future coins
        self._pulse3: int = 8

        # count the number of flanks. 2 flanks = 1 pulse
        self._flankenCounter: int = 0

        # TODO C++: volatile uint8_t pinLED;
        self.pinLED: int = 0
        # TODO C++: volatile uint8_t pinCoinAcceptor
        self.pinCoinAcceptor: int = 0

    def cd_returnCoin(self):
        pass

    def cd_coinDetection(self):
        pass
