import RPi.GPIO as GPIO
from Display import Display
from rgbmatrix import graphics

COIN_PIN = 19
GAME_COST = 1

class CoinDetection:
    _balance: int = 0

    @classmethod
    def __set_led(cls):
        """Setzt den LED-Status auf der Matrix basierend auf dem Guthaben."""
        if cls._balance >= GAME_COST:
            # Grün anzeigen (Guthaben vorhanden)
            color = Display.get_color(0, 255, 0)
        else:
            # Rot anzeigen (kein Guthaben)
            color = Display.get_color(255, 0, 0)
        # Pixel oder Indikator auf der Matrix setzen (z. B. Ecke oben rechts)
        Display.fill_rect(0, 0, 10, 10, color)

    @classmethod
    def __detect_falling_edge(cls, channel):
        """Wird bei einer fallenden Flanke am COIN_PIN ausgelöst."""
        cls._balance += 1
        cls.__set_led()
        print(f"Neue Münze erkannt. Aktuelles Guthaben: {cls._balance}")

    @classmethod
    def init(cls):
        """Initialisiert die GPIOs und Interrupts."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(COIN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Interrupt für fallende Flanke aktivieren
        GPIO.add_event_detect(COIN_PIN, GPIO.FALLING, callback=cls.__detect_falling_edge, bouncetime=300)

        cls._balance = 0
        cls.__set_led()

    @classmethod
    def start_game(cls) -> bool:
        """Startet ein Spiel, wenn genügend Guthaben vorhanden ist."""
        if cls._balance >= GAME_COST:
            cls._balance -= GAME_COST
            cls.__set_led()
            print(f"Spiel gestartet. Restguthaben: {cls._balance}")
            return True
        print("Nicht genug Guthaben für ein Spiel.")
        return False
