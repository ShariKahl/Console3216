import RPi.GPIO as GPIO
from Microcontroller import RGB_R_PIN, RGB_G_PIN, RGB_B_PIN

class Color_t:
    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue

# Vordefinierte Farben
ColorBlack = Color_t(0, 0, 0)
ColorRed = Color_t(255, 0, 0)
ColorYellow = Color_t(255, 255, 0)
ColorOrange = Color_t(255, 165, 0)
ColorGreen = Color_t(0, 255, 0)
ColorBlue = Color_t(0, 0, 255)
ColorPurple = Color_t(128, 0, 128)
ColorPink = Color_t(255, 192, 203)

class RgbLed:
    def __init__(self):
        """
        Initialisiert die RGB-LED-Pins für PWM.
        """
        GPIO.setmode(GPIO.BCM)  # Verwende Broadcom-Pin-Nummerierung
        GPIO.setup(RGB_R_PIN, GPIO.OUT)
        GPIO.setup(RGB_G_PIN, GPIO.OUT)
        GPIO.setup(RGB_B_PIN, GPIO.OUT)

        # PWM initialisieren
        self.__pwm_red = GPIO.PWM(RGB_R_PIN, 100)  # 100 Hz Frequenz
        self.__pwm_green = GPIO.PWM(RGB_G_PIN, 100)
        self.__pwm_blue = GPIO.PWM(RGB_B_PIN, 100)

        # PWM starten mit 0% Duty Cycle (aus)
        self.__pwm_red.start(0)
        self.__pwm_green.start(0)
        self.__pwm_blue.start(0)

        self.__actualColor = ColorBlack
        print("RGB LED initialized.")

    def __setPWM(self, pwm, value):
        """
        Setzt den PWM-Wert für eine LED-Farbe.
        :param pwm: PWM-Objekt
        :param value: Helligkeit (0-255)
        """
        duty_cycle = max(0, min(100, (value / 255) * 100))  # Umrechnung auf 0-100%
        pwm.ChangeDutyCycle(duty_cycle)

    def setLEDColorRGB(self, red: int, green: int, blue: int):
        """
        Setzt die RGB-Farbe der LED.
        :param red: Rot-Wert (0-255)
        :param green: Grün-Wert (0-255)
        :param blue: Blau-Wert (0-255)
        """
        self.__actualColor = Color_t(red, green, blue)

        # PWM-Werte aktualisieren
        self.__setPWM(self.__pwm_red, red)
        self.__setPWM(self.__pwm_green, green)
        self.__setPWM(self.__pwm_blue, blue)

        print(f"Set LED color to RGB({red}, {green}, {blue})")

    def setLEDColor(self, color: Color_t):
        """
        Setzt die Farbe der LED basierend auf einem Color_t-Objekt.
        :param color: Color_t-Objekt mit RGB-Werten
        """
        self.setLEDColorRGB(color.red, color.green, color.blue)

    def getLEDColor(self) -> Color_t:
        """
        Gibt die aktuelle Farbe der LED zurück.
        :return: Color_t-Objekt mit der aktuellen Farbe
        """
        return self.__actualColor

    def setLEDStatusOn(self):
        """
        Schaltet die LED mit der aktuellen Farbe ein.
        """
        self.setLEDColor(self.__actualColor)
        print("LED turned on.")

    def setLEDStatusOff(self):
        """
        Schaltet die LED aus.
        """
        self.setLEDColorRGB(0, 0, 0)
        print("LED turned off.")

    def cleanup(self):
        """
        Bereinigt die GPIO-Konfiguration.
        """
        self.__pwm_red.stop()
        self.__pwm_green.stop()
        self.__pwm_blue.stop()
        GPIO.cleanup()
        print("GPIO cleaned up.")
