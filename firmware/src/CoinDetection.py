
# TODO Wahrscheinlich nicht nötig, wegen dem Matrix Bonnet
import RPi.GPIO as GPIO

# TODO
#import RgbLed
from RgbLed import *
from Display import *

COIN_PIN = 19
GAME_COST = 1


class CoinDetection:
    _balance: int = 0
    _rgbLed: RgbLed = RgbLed()

    @classmethod
    def __setLed(cls):
        if cls._balance >= GAME_COST:
            cls._rgbLed.setLEDColorRGB(0, 3, 0)
        else:
            cls._rgbLed.setLEDColorRGB(3, 0, 0)

    @classmethod
    def __detectFallingEdge(cls):
        cls._balance += 1
        cls.__setLed()
        # TODO pyserial
        # Serial.println("edge");

    @classmethod
    def init(cls):
        # TODO Aus C++ Quellcode
        # pinMode(COIN_PIN, INPUT_PULLUP);
        # attachInterrupt(digitalPinToInterrupt(COIN_PIN), detectFallingEdge, FALLING);
        # TODO setmode muss wahrscheinlich woanders aktiviert werden
        GPIO.setmode(GPIO.BCM)
        cls.__detectFallingEdge()
        GPIO.setup(COIN_PIN, GPIO.IO, GPIO.PUD_UP)
        cls._balance = 0

    @classmethod
    def startGame(cls) -> bool:
        if cls._balance >= GAME_COST:
            cls._balance -= GAME_COST
            cls.__setLed()
            return True
        return False
