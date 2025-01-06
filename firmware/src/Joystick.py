import RPi.GPIO as GPIO

# Konstanten für Joystick-Status
JOYSTICK_STATUS_NOT_PRESSED = 0
JOYSTICK_STATUS_PRESSED = 1
JOYSTICK_STATUS_HOLD = 2

# Joystick-Schalter
JOYSTICK_SWITCH_LEFT = 0
JOYSTICK_SWITCH_UP = 1
JOYSTICK_SWITCH_RIGHT = 2
JOYSTICK_SWITCH_DOWN = 3
JOYSTICK_SWITCH_BUTTON_TOP = 4
JOYSTICK_SWITCH_BUTTON_BODY = 5

JOYSTICK_SWITCHES_COUNT = 6


class JoystickPins_t:
    """Struktur für Joystick-Pins."""
    def __init__(self, left=0, up=0, right=0, down=0, buttonTop=0, buttonBody=0):
        self.left = left
        self.up = up
        self.right = right
        self.down = down
        self.buttonTop = buttonTop
        self.buttonBody = buttonBody


class JoystickEdge_t:
    """Struktur für Joystick-Kanten (Edge Detection)."""
    def __init__(self):
        self.left = JOYSTICK_STATUS_NOT_PRESSED
        self.up = JOYSTICK_STATUS_NOT_PRESSED
        self.right = JOYSTICK_STATUS_NOT_PRESSED
        self.down = JOYSTICK_STATUS_NOT_PRESSED
        self.buttonTop = JOYSTICK_STATUS_NOT_PRESSED
        self.buttonBody = JOYSTICK_STATUS_NOT_PRESSED


class Joystick:
    """Klasse zur Steuerung eines Joysticks über GPIO."""
    def __init__(self):
        self.__pins = JoystickPins_t()
        self.__edges = JoystickEdge_t()

    def init(self, pins: JoystickPins_t):
        """Initialisiert den Joystick mit den angegebenen GPIO-Pins."""
        self.__pins = pins

        # Pins als Eingänge mit Pull-Up-Widerstand konfigurieren
        GPIO.setup(self.__pins.left, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.__pins.up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.__pins.right, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.__pins.down, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.__pins.buttonTop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.__pins.buttonBody, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def isLeft(self) -> bool:
        return GPIO.input(self.__pins.left) == GPIO.LOW

    def isUp(self) -> bool:
        return GPIO.input(self.__pins.up) == GPIO.LOW

    def isRight(self) -> bool:
        return GPIO.input(self.__pins.right) == GPIO.LOW

    def isDown(self) -> bool:
        return GPIO.input(self.__pins.down) == GPIO.LOW

    def isButtonTop(self) -> bool:
        return GPIO.input(self.__pins.buttonTop) == GPIO.LOW

    def isButtonBody(self) -> bool:
        return GPIO.input(self.__pins.buttonBody) == GPIO.LOW

    def process(self):
        """Aktualisiert den Status aller Joystick-Schalter."""
        for switch_id in range(JOYSTICK_SWITCHES_COUNT):
            self.checkEdge(switch_id)

    def getSwitchStatus(self, switch_id: int) -> bool:
        """Gibt den Zustand eines bestimmten Joystick-Schalters zurück."""
        switch_methods = {
            JOYSTICK_SWITCH_LEFT: self.isLeft,
            JOYSTICK_SWITCH_UP: self.isUp,
            JOYSTICK_SWITCH_RIGHT: self.isRight,
            JOYSTICK_SWITCH_DOWN: self.isDown,
            JOYSTICK_SWITCH_BUTTON_TOP: self.isButtonTop,
            JOYSTICK_SWITCH_BUTTON_BODY: self.isButtonBody,
        }
        return switch_methods.get(switch_id, lambda: False)()

    def checkEdge(self, switch_id: int):
        """Prüft auf Kantenwechsel (Edge Detection) für einen Schalter."""
        current_status = self.getSwitchStatus(switch_id)
        previous_status = self.getControlStatus(switch_id)

        if current_status:  # Schalter ist gedrückt
            if previous_status == JOYSTICK_STATUS_NOT_PRESSED:
                self.setControlStatus(switch_id, JOYSTICK_STATUS_PRESSED)
            elif previous_status == JOYSTICK_STATUS_PRESSED:
                self.setControlStatus(switch_id, JOYSTICK_STATUS_HOLD)
        else:  # Schalter ist nicht gedrückt
            self.setControlStatus(switch_id, JOYSTICK_STATUS_NOT_PRESSED)

    def getControlStatus(self, switch_id: int) -> int:
        """Gibt den aktuellen Steuerstatus eines Schalters zurück."""
        status_mapping = {
            JOYSTICK_SWITCH_LEFT: self.__edges.left,
            JOYSTICK_SWITCH_UP: self.__edges.up,
            JOYSTICK_SWITCH_RIGHT: self.__edges.right,
            JOYSTICK_SWITCH_DOWN: self.__edges.down,
            JOYSTICK_SWITCH_BUTTON_TOP: self.__edges.buttonTop,
            JOYSTICK_SWITCH_BUTTON_BODY: self.__edges.buttonBody,
        }
        return status_mapping.get(switch_id, JOYSTICK_STATUS_NOT_PRESSED)

    def setControlStatus(self, switch_id: int, status: int):
        """Setzt den Steuerstatus eines Schalters."""
        if switch_id == JOYSTICK_SWITCH_LEFT:
            self.__edges.left = status
        elif switch_id == JOYSTICK_SWITCH_UP:
            self.__edges.up = status
        elif switch_id == JOYSTICK_SWITCH_RIGHT:
            self.__edges.right = status
        elif switch_id == JOYSTICK_SWITCH_DOWN:
            self.__edges.down = status
        elif switch_id == JOYSTICK_SWITCH_BUTTON_TOP:
            self.__edges.buttonTop = status
        elif switch_id == JOYSTICK_SWITCH_BUTTON_BODY:
            self.__edges.buttonBody = status
