from time import sleep
from smbus2 import SMBus

# pip install smbus2

HT16K33_DISPLAY_SIZE = 16
HT16K33_CMD_BRIGHTNESS = 0xE0
HT16K33_CMD_OSCILLATOR = 0x21
HT16K33_CMD_DISPLAY_ON = 0x81
HT16K33_CMD_DISPLAY_OFF = 0x80

class Ht16k33:
    def __init__(self, i2c_bus: int = 1):
        """Initialisiert den HT16K33-Treiber."""
        self._i2c_address = 0
        self._dataBuffer = [0x00] * HT16K33_DISPLAY_SIZE
        self._i2c_bus = SMBus(i2c_bus)  # Standard I2C-Bus ist 1 auf Raspberry Pi

    def init(self, i2c_address: int):
        """Initialisiert den HT16K33 mit der angegebenen I2C-Adresse."""
        self._i2c_address = i2c_address

        # HT16K33 einschalten (Oszillator aktivieren)
        self._write_command(HT16K33_CMD_OSCILLATOR)

        # Display einschalten, keine Blinken (Blink = 0)
        self._write_command(HT16K33_CMD_DISPLAY_ON)

        # Standard-Helligkeit einstellen
        self.setBrightness(15)

        sleep(0.1)

    def setBrightness(self, brightness: int):
        """Setzt die Helligkeit (0-15)."""
        brightness = max(0, min(brightness, 15))  # Begrenzen auf 0-15
        self._write_command(HT16K33_CMD_BRIGHTNESS | brightness)

    def refresh(self):
        """Aktualisiert das Display mit den Daten im Puffer."""
        try:
            # Daten an die I2C-Adresse senden
            self._i2c_bus.write_i2c_block_data(self._i2c_address, 0x00, self._dataBuffer)
        except IOError as e:
            print(f"I2C Error while refreshing: {e}")

    def setBuffer(self, index: int, value: int):
        """Setzt einen Wert im Datenpuffer."""
        if 0 <= index < HT16K33_DISPLAY_SIZE:
            self._dataBuffer[index] = value

    def clearBuffer(self):
        """Löscht den Datenpuffer."""
        self._dataBuffer = [0x00] * HT16K33_DISPLAY_SIZE

    def _write_command(self, command: int):
        """Sendet einen Befehl an den HT16K33."""
        try:
            self._i2c_bus.write_byte(self._i2c_address, command)
        except IOError as e:
            print(f"I2C Error while writing command: {e}")

    def close(self):
        """Schließt die Verbindung zum I2C-Bus."""
        self._i2c_bus.close()
