
import RPi.GPIO as GPIO
from Microcontroller import *

START_BUTTON_IDLE = 0
START_BUTTON_PRESSED = 1
START_BUTTON_HOLD = 2

class StartButton:
    _status: int = 0
    
    def __init__(self) -> None:
        type(self)._status = START_BUTTON_IDLE
        pass
    
    @classmethod
    def init(cls):
        # TODO C++ Quellcode:
        # pinMode(PIN_START_BUTTON, INPUT_PULLUP);
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_START_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        pass

    @classmethod
    def isPressed(cls) -> bool:
        # TODO C++ Quellcode:
        # if (digitalRead(PIN_START_BUTTON) == LOW)
        if GPIO.input(PIN_START_BUTTON) == GPIO.LOW:
            return True
        return False

    @classmethod
    def getStatus(cls) -> int:
        pressed = cls.isPressed()

        if cls._status == START_BUTTON_IDLE and pressed:
            cls._status = START_BUTTON_PRESSED
        elif cls._status == START_BUTTON_PRESSED and pressed:
            cls._status = START_BUTTON_HOLD
        elif not pressed:
            cls._status = START_BUTTON_IDLE
        return cls._status
