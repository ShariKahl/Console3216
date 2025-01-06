from MidiTicks import Ticks

def test_ticks():
    # Ticks-Objekt erstellen
    tick1 = Ticks(120)
    print(tick1)  # Erwartet: Ticks(duration=120)

    # Dauer ändern
    tick1.set_duration(240)
    print(f"Updated duration: {tick1.get_duration()}")  # Erwartet: 240

    # Zweites Ticks-Objekt erstellen
    tick2 = Ticks(480)
    print(tick2)  # Erwartet: Ticks(duration=480)

test_ticks()
