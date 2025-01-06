from Ht16k33 import Ht16k33

ht16k33 = Ht16k33()
ht16k33.init(0x70)  # Ersetze 0x70 durch die ermittelte Adresse
ht16k33.setBrightness(10)

# Setze einige Werte im Puffer
ht16k33.setBuffer(0, 0xFF)  # Alle LEDs in der ersten Zeile einschalten
ht16k33.refresh()

# Puffer löschen und aktualisieren
ht16k33.clearBuffer()
ht16k33.refresh()

ht16k33.close()
