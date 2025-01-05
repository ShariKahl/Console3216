from Microcontroller import *

# TODO Eventuell wird diese Datei garnicht mehr benötigt

# TODO Im original ein Struct
class Color_t:
    def __init__(self, red: int, green: int, blue: int) -> None:
        self.red = red
        self.green = green
        self.blue = blue


ColorBlack = Color_t(0, 0, 0)
ColorRed = Color_t(3, 0, 0)
ColorYellow = Color_t(3, 3, 0)
ColorOrange = Color_t(3, 1, 0)
ColorGreen = Color_t(0, 3, 0)
ColorBlue = Color_t(0, 0, 3)
ColorPurple = Color_t(3, 0, 3)
ColorPink = Color_t(3, 0, 1)

RGB_LED_DELAY_MASK = 0x03

# TODO Im original ein Struct
# TODO Einzige Variable dieses Typs im Originalcode wird nie verwendet
# class RGBCycle_t:
#     def __init__(self, color: Color_t, delay: int) -> None:
#         self.color = color
#         self.delay = delay


class RgbLed:
    # Start the timer for PWM.
    def __startTimer(self):
        pass

    # Stop the timer.
    def __stopTimer(self):
        pass

    # Constructor for the LED module.
    def __init__(self):
        # TODO Im C++ Code deklariert aber nie verwendet
        # self.__LEDCycle: RGBCycle_t

        self.__actualColor: Color_t = Color_t(0, 0, 0)

        # TODO C++ Quellcode:
        # analogWrite(RGB_R_PIN, 0);
        # analogWrite(RGB_G_PIN, 0);
        # analogWrite(RGB_B_PIN, 0);

        # TODO Python, funktion analogWrite (noch) nicht importiert
        # analogWrite(RGB_R_PIN, 0)
        # analogWrite(RGB_G_PIN, 0)
        # analogWrite(RGB_B_PIN, 0)

    # Sets the color for the RGB led.
    # TODO Python unterstützt kein overloading, vorher setLEDColor(...)
    def setLEDColorRGB(self, red: int, green: int, blue: int):
        self.__actualColor.red = 255 - red
        self.__actualColor.green = 255 - green
        self.__actualColor.blue = 255 - blue

        # TODO C++ Quellcode:
        # analogWrite(RGB_R_PIN, this->actualColor.red);
        # analogWrite(RGB_G_PIN, this->actualColor.green);
        # analogWrite(RGB_B_PIN, this->actualColor.blue);

        # TODO Python, Funktion analogWrite (noch) nicht importiert
        # analogWrite(RGB_R_PIN, self.__actualColor.red);
        # analogWrite(RGB_G_PIN, self.__actualColor.green);
        # analogWrite(RGB_B_PIN, self.__actualColor.blue);

    # Sets the color for the RGB led.
    def setLEDColor(self, color: Color_t):
        self.setLEDColorRGB(color.red, color.green, color.blue)

    # Gets the current color for the RGB led.
    def getLEDColor(self, color: Color_t):
        color.red = 255 - self.__actualColor.red
        color.green = 255 - self.__actualColor.green
        color.blue = 255 - self.__actualColor.blue

    # Turns on the RGB led.
    def setLEDStatusOn(self):
        # TODO C++ Quellcode:
        # digitalWrite(RGB_R_PIN, this->actualColor.red);
        # digitalWrite(RGB_G_PIN, this->actualColor.green);
        # digitalWrite(RGB_B_PIN, this->actualColor.blue);

        # TODO Python, Funktion digitalWrite (noch) nicht importiert
        # digitalWrite(RGB_R_PIN, self.__actualColor.red)
        # digitalWrite(RGB_G_PIN, self.__actualColor.green)
        # digitalWrite(RGB_B_PIN, self.__actualColor.blue)
        pass

    # Turns off the RGB led.
    def setLEDStatusOff(self):
        # TODO C++ Quellcode:
        # digitalWrite(RGB_R_PIN, 0);
        # digitalWrite(RGB_G_PIN, 0);
        # digitalWrite(RGB_B_PIN, 0);

        # TODO Python, Funktion digitalWrite (noch) nicht importiert
        # digitalWrite(RGB_R_PIN, 0)
        # digitalWrite(RGB_G_PIN, 0)
        # digitalWrite(RGB_B_PIN, 0)
        pass
