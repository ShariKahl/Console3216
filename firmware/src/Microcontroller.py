# GPIO-Pin-Zuweisungen für den Raspberry Pi

# Coin-Acceptor
PIN_COIN_ACCEPTOR_COUNTER = 17  # Beispiel-Pin, anpassen falls nötig

# Start-Button
PIN_START_BUTTON = 27  # Beispiel-Pin, anpassen falls nötig

# Joystick-Pins (links)
PIN_JOYSTICK_LEFT_LEFT = 5
PIN_JOYSTICK_LEFT_UP = 6
PIN_JOYSTICK_LEFT_RIGHT = 13
PIN_JOYSTICK_LEFT_DOWN = 19
PIN_JOYSTICK_LEFT_BUTTON_TOP = 26
PIN_JOYSTICK_LEFT_BUTTON_BODY = 21

# Joystick-Pins (rechts)
PIN_JOYSTICK_RIGHT_LEFT = 20
PIN_JOYSTICK_RIGHT_UP = 16
PIN_JOYSTICK_RIGHT_DOWN = 12
PIN_JOYSTICK_RIGHT_RIGHT = 25
PIN_JOYSTICK_RIGHT_BUTTON_TOP = 24
PIN_JOYSTICK_RIGHT_BUTTON_BODY = 23

# Sieben-Segment-Anzeigen (optional, falls nicht benötigt, entfernen)
PIN_SIEBEN_SEGMENT_ANZEIGE_1 = 22
PIN_SIEBEN_SEGMENT_ANZEIGE_2 = 10

# Lautsprecher (optional, falls nicht benötigt, entfernen)
PIN_LAUTSPRECHER = 18

# Pins für die LED-Matrix (werden von Adafruit-Bibliothek verwendet)
PIN_DISPLAY_CLK = 11  # Wird direkt von der Bibliothek gesteuert
PIN_DISPLAY_OE = 9
PIN_DISPLAY_LAT = 8

# RGB-LED-Pins (optional, falls nicht benötigt, entfernen)
RGB_R_PIN = 2
RGB_G_PIN = 3
RGB_B_PIN = 4

# Hinweis: Analoge Pins des Arduino wie A0-A3 sind auf dem Raspberry Pi nicht verfügbar.
# Diese wurden entfernt oder durch digitale GPIO-Pins ersetzt.
