import RPi.GPIO as GPIO
import time
from enum import Enum


class CoinDetection:
    """
    Klasse zur Erkennung von Münzeinwürfen.
    """

    # Flankenstatus
    coinToggle: bool = False

    # Zeitmesser
    timer: float = 0.0

    class Coin(Enum):
        CENT5 = 0
        CENT10 = 1
        CENT20 = 2
        UNKNOWN = 3

    def __init__(self, coin_pin: int, led_pin: int):
        """
        Initialisiert die Münzerkennung und die zugehörigen GPIO-Pins.
        :param coin_pin: GPIO-Pin für den Münzprüfer
        :param led_pin: GPIO-Pin für die LED-Anzeige
        """
        self.coin_pin = coin_pin
        self.led_pin = led_pin

        self._pulse1 = 4
        self._pulse2 = 6
        self._pulse3 = 8

        self._flankenCounter = 0

        # GPIO-Initialisierung
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.coin_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.led_pin, GPIO.OUT)

        # LED aus
        GPIO.output(self.led_pin, GPIO.LOW)

    def cd_returnCoin(self):
        """
        Gibt eine Münze zurück (LED als Signal).
        """
        print("Returning coin...")
        GPIO.output(self.led_pin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(self.led_pin, GPIO.LOW)

    def cd_coinDetection(self):
        """
        Erkennung eines Münzeinwurfs basierend auf Signalflanken.
        """
        if GPIO.input(self.coin_pin) == GPIO.LOW and not self.coinToggle:
            # Flanke erkannt
            self.coinToggle = True
            self._flankenCounter += 1
            self.timer = time.time()
            print(f"Flanke erkannt: {self._flankenCounter} Flanken gezählt.")
        elif GPIO.input(self.coin_pin) == GPIO.HIGH and self.coinToggle:
            # Rückkehr zur Ruheposition
            self.coinToggle = False

        # Zeitüberschreitung prüfen
        if self.coinToggle and (time.time() - self.timer > 2):
            print("Timeout: Kein vollständiger Münzimpuls erkannt.")
            self._flankenCounter = 0

        # Münzerkennung
        if self._flankenCounter == self._pulse1:
            print("5-Cent-Münze erkannt.")
            self._flankenCounter = 0
            return self.Coin.CENT5
        elif self._flankenCounter == self._pulse2:
            print("10-Cent-Münze erkannt.")
            self._flankenCounter = 0
            return self.Coin.CENT10
        elif self._flankenCounter == self._pulse3:
            print("20-Cent-Münze erkannt.")
            self._flankenCounter = 0
            return self.Coin.CENT20
        else:
            return self.Coin.UNKNOWN

    def cleanup(self):
        """
        Bereinigt die GPIO-Konfiguration.
        """
        GPIO.cleanup(self.coin_pin)
        GPIO.cleanup(self.led_pin)
        print("GPIO cleaned up.")
