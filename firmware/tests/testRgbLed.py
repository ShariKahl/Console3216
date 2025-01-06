from RgbLed import RgbLed, ColorRed, ColorGreen, ColorBlue

def test_rgb_led():
    led = RgbLed()

    # Test: Farben einstellen
    led.setLEDColor(ColorRed)
    led.setLEDColor(ColorGreen)
    led.setLEDColor(ColorBlue)

    # Test: LED ausschalten
    led.setLEDStatusOff()

    # GPIO bereinigen
    led.cleanup()

test_rgb_led()
