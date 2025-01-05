
from Ht16k33 import *

# TODO In C++ Quellcode eine Konstante:
# static const uint8_t numbertable[] = { ... }
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

# TODO Alter Positionscode
# SEVEN_SEGMENT_SEGMENT_0_POS = 8
# SEVEN_SEGMENT_SEGMENT_1_POS = 6
# SEVEN_SEGMENT_SEGMENT_2_POS = 2
# SEVEN_SEGMENT_SEGMENT_3_POS = 0
# TODO Neuer positionscode
SEVEN_SEGMENT_POS = [8, 6, 2, 0]

SEVEN_SEGMENT_DOT_MASK = (1<<7)

SEVEN_SEG_COLON_MASK = 0x2 

# TODO C++ Klassendeklaration:
# class SevenSegmentDisplay	: public Ht16k33 { ... };
class SevenSegmentDisplay(Ht16k33):

    def setNumberAt(self, number: int, position: int):
        # TODO Alter code
        # if position == 0:
        #     self._dataBuffer[SEVEN_SEGMENT_SEGMENT_0_POS] = numbertable[number]
        # elif position == 1:
        #     self._dataBuffer[SEVEN_SEGMENT_SEGMENT_1_POS] = numbertable[number]
        # elif position == 2:
        #     self._dataBuffer[SEVEN_SEGMENT_SEGMENT_2_POS] = numbertable[number]
        # elif position == 3:
        #     self._dataBuffer[SEVEN_SEGMENT_SEGMENT_3_POS] = numbertable[number]
        
        self._dataBuffer[SEVEN_SEGMENT_POS[position]] = numbertable[number]
        pass

    def setSegmentsAt(self, segments: int, position: int):
        # TODO Alter code
        # if position == 0:
        #     self._dataBuffer[SEVEN_SEGMENT_SEGMENT_0_POS] = segments
        # elif position == 1:
        #     self._dataBuffer[SEVEN_SEGMENT_SEGMENT_1_POS] = segments
        # elif position == 2:
        #     self._dataBuffer[SEVEN_SEGMENT_SEGMENT_2_POS] = segments
        # elif position == 3:
        #     self._dataBuffer[SEVEN_SEGMENT_SEGMENT_3_POS] = segments
        
        self._dataBuffer[SEVEN_SEGMENT_POS[position]] = segments
        pass

    def clearDotAt(self, number: int, position: int):
        # TODO:
        # Muss getestet werden, ob bitwise-Operationen sich in Python
        # genau so wie in C++ verhalten.

        # dataBuffer in C++:
        # uint8_t dataBuffer[HT16K33_DISPLAY_SIZE];
        # SEVEN_SEGNMENT_DOT_MASK in C++:
        # #define SEVEN_SEGMENT_DOT_MASK (1<<7)
        
        # TODO Alter code
        # if position == 0:
        #     self._dataBuffer[SEVEN_SEGMENT_SEGMENT_0_POS] &= ~SEVEN_SEGMENT_DOT_MASK
        # elif position == 1:
        #     self._dataBuffer[SEVEN_SEGMENT_SEGMENT_1_POS] &= ~SEVEN_SEGMENT_DOT_MASK
        # elif position == 2:
        #     self._dataBuffer[SEVEN_SEGMENT_SEGMENT_2_POS] &= ~SEVEN_SEGMENT_DOT_MASK
        # elif position == 3:
        #     self._dataBuffer[SEVEN_SEGMENT_SEGMENT_3_POS] &= ~SEVEN_SEGMENT_DOT_MASK
        
        self._dataBuffer[SEVEN_SEGMENT_POS[position]] &= ~SEVEN_SEGMENT_DOT_MASK
        # TODO Parameter number wird in C++ auch nicht verwendet.
        pass

    def setDotAt(self, number: int, position: int):
        # TODO:
        # Muss getestet werden, ob bitwise-Operationen sich in Python
        # genau so wie in C++ verhalten.

        # dataBuffer in C++:
        # uint8_t dataBuffer[HT16K33_DISPLAY_SIZE];
        # SEVEN_SEGNMENT_DOT_MASK in C++:
        # #define SEVEN_SEGMENT_DOT_MASK (1<<7)
        
        # TODO Alter code
        # if position == 0:
        #     self._dataBuffer[SEVEN_SEGMENT_SEGMENT_0_POS] |= SEVEN_SEGMENT_DOT_MASK
        # elif position == 1:
        #     self._dataBuffer[SEVEN_SEGMENT_SEGMENT_1_POS] |= SEVEN_SEGMENT_DOT_MASK
        # elif position == 2:
        #     self._dataBuffer[SEVEN_SEGMENT_SEGMENT_2_POS] |= SEVEN_SEGMENT_DOT_MASK
        # elif position == 3:
        #     self._dataBuffer[SEVEN_SEGMENT_SEGMENT_3_POS] |= SEVEN_SEGMENT_DOT_MASK
        
        self._dataBuffer[SEVEN_SEGMENT_POS[position]] |= SEVEN_SEGMENT_DOT_MASK
        # TODO Parameter number wird in C++ auch nicht verwendet.
        pass

    def setColon(self):
        self._dataBuffer[4] = SEVEN_SEG_COLON_MASK
        pass

    def clearColon(self):
        self._dataBuffer[4] = 0
        pass

    def toggleColon(self):
        # TODO:
        # Muss getestet werden, ob bitwise-Operationen sich in Python
        # genau so wie in C++ verhalten.

        # Kurze tests in beiden Sprachen lieferten die gleichen Ergebnisse
        self._dataBuffer[4] ^= SEVEN_SEG_COLON_MASK
        pass

    def setNumber(self, value: int):
        # TODO C++ Quellcode:
        # uint16_t bcdValue =  0;
        # Muss getestet werden, ob sich die shift-Operationen bei 16 bit C++ ints
        # anders verhalten, als bei Python ints
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
        pass
