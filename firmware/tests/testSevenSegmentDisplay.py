from SevenSegmentDisplay import SevenSegmentDisplay

def test_seven_segment_display():
    display = SevenSegmentDisplay()

    # Test: Zahlen setzen
    display.setNumberAt(3, 0)
    display.setNumberAt(5, 1)

    # Test: Punkte setzen und löschen
    display.setDotAt(0)
    display.clearDotAt(0)

    # Test: Doppelpunkte
    display.setColon()
    display.toggleColon()
    display.clearColon()

    # Test: Ganze Zahl anzeigen
    display.setNumber(1234)

test_seven_segment_display()
