from NumericDisplay import NumericDisplay, DISPLAY_LEFT, DISPLAY_MIDDLE, DISPLAY_RIGHT

def test_numeric_display():
    # Initialisiere NumericDisplay
    display = NumericDisplay()

    # Test: Zahlen anzeigen
    display.displayValue(DISPLAY_LEFT, 123)
    display.displayValue(DISPLAY_MIDDLE, 456)
    display.displayValue(DISPLAY_RIGHT, 789)

    # Test: Zeit anzeigen
    display.displayTime(DISPLAY_LEFT, 3661)  # Erwartet: 61:01
    display.displayTime(DISPLAY_MIDDLE, 123)  # Erwartet: 02:03

test_numeric_display()
