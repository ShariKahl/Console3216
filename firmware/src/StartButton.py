import RPi.GPIO as GPIO
from Microcontroller import *

START_BUTTON_IDLE = 0
START_BUTTON_PRESSED = 1
START_BUTTON_HOLD = 2


class StartButton:
    _status: int = START_BUTTON_IDLE

    @classmethod
    def init(cls):
        """
        Initialisiert den Start-Button und konfiguriert den GPIO-Pin.
        """
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(PIN_START_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            print("Start button initialized.")
        except RuntimeError as e:
            print(f"GPIO initialization failed: {e}")

    @classmethod
    def cleanup(cls):
        """
        Bereinigt die GPIO-Konfiguration.
        """
        GPIO.cleanup(PIN_START_BUTTON)
        print("GPIO cleanup completed for start button.")

    @classmethod
    def isPressed(cls) -> bool:
        """
        Überprüft, ob der Start-Button gedrückt ist.
        :return: True, wenn der Button gedrückt ist, sonst False.
        """
        return GPIO.input(PIN_START_BUTTON) == GPIO.LOW

    @classmethod
    def getStatus(cls) -> int:
        """
        Gibt den aktuellen Status des Start-Buttons zurück:
        - IDLE: Button nicht gedrückt.
        - PRESSED: Button gerade gedrückt.
        - HOLD: Button gehalten.
        :return: Der aktuelle Status des Buttons.
        """
        pressed = cls.isPressed()

        if cls._status == START_BUTTON_IDLE and pressed:
            cls._status = START_BUTTON_PRESSED
            print("Start button pressed.")
        elif cls._status == START_BUTTON_PRESSED and pressed:
            cls._status = START_BUTTON_HOLD
            print("Start button held.")
        elif not pressed:
            if cls._status != START_BUTTON_IDLE:
                print("Start button released.")
            cls._status = START_BUTTON_IDLE

        return cls._status
