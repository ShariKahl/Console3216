
TIME_BASIS_MS = 20

MAIN_TIMER_PERIOD = 1250

class MainClockStatus_t:
    def __init__(self) -> None:
        # TODO Beide Variablen im C++ Struct auf nur ein Bit begrenzt
        # C++:
        # typedef struct{
        # 	uint8_t systemTick:1;
        # 	uint8_t systemTickOverflow:1;
        # }MainClockStatus_t;
        self.systemTick: int = 0
        self.systemTickOverflow: int = 0


class MainClock:
    __systemTime: int = 0

    def __init__(self) -> None:
        self.__status: MainClockStatus_t = MainClockStatus_t()
    
    def startTimer(self):
        # TODO C++ Quellcode:
        # cli();
        # Aus "Arduino.h", "avr/interrupt.h" oder "avr/io.h"

        global mainClock
        mainClock = self

        # TODO C++ Quellcode:
        # TCCR3A =   (1<<WGM31) | (0<<WGM30);
        # TCCR3B = (1<<CS32) | (0<<CS31) | (0<<CS30)| ( 1<<WGM33 ) | (1<<WGM32 );
        
        # TCNT3H = 0;
        # TCNT3L = 0;

        # ICR3 = MAIN_TIMER_PERIOD;

        # TIMSK3 |= (1 << TOIE3);

        # OCR3AH=0;
        # OCR3AL=0;

        # OCR3BH=0;
        # OCR3BL=0;

        # sei();
        # Aus "Arduino.h", "avr/interrupt.h" oder "avr/io.h"

        type(self).__systemTime = 0
        pass

    def setTick(self):
        if self.__status.systemTick != 0:
            self.__status.systemTickOverflow = 1
        
        self.__status.systemTick = 1
        type(self).__systemTime += 1
        pass
    def isTick(self) -> bool:
        if self.__status.systemTick == 1:
            self.__status.systemTick = 0
            return True
        
        return False
    def hasOverflow(self) -> bool:
        if self.__status.systemTickOverflow == 1:
            self.clearOverflow()
            return True
        
        return False
    def clearOverflow(self):
        self.__status.systemTickOverflow = 0
        pass

    @classmethod
    def getSystemTime(cls) -> int:
        return cls.__systemTime * TIME_BASIS_MS

# TODO C++ Quellcode:
# ISR(TIMER3_OVF_vect) 
# {
# 		mainClock->setTick();
# }

# TODO Im C++ Quellcode ein pointer:
# MainClock * mainClock;
mainClock: MainClock = MainClock()
