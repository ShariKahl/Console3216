sinetable = [
    0, 6, 13, 19, 25, 31, 37, 43,
    49, 55, 60, 66, 71, 76, 81, 86,
    91, 95, 99, 103, 106, 110, 113, 116,
    118, 121, 122, 124, 126, 127, 127, 128, 128
]

class Sine:
    @classmethod
    def getSineValue(cls, angle: int) -> int:
        """
        Berechnet den Sinuswert eines Winkels anhand einer Tabelle.
        :param angle: Winkel in "128-Ticks", entsprechend 0°-360°
        :return: Sinuswert
        """
        # Modulo 128, um den Winkel auf den Bereich [0, 127] zu reduzieren
        angle %= 128
        print(f"Adjusted angle: {angle}")

        # Berechnung des Sinuswerts basierend auf der Tabelle
        if angle < 33:
            value = sinetable[angle]
        elif angle < 65:
            value = sinetable[64 - angle]
        elif angle < 97:
            value = -sinetable[angle - 64]
        else:  # angle < 128
            value = -sinetable[128 - angle]

        print(f"Sine value for angle {angle}: {value}")
        return value

    @classmethod
    def getCosineValue(cls, angle: int) -> int:
        """
        Berechnet den Kosinuswert eines Winkels basierend auf der Sinustabelle.
        :param angle: Winkel in "128-Ticks", entsprechend 0°-360°
        :return: Kosinuswert
        """
        # Kosinus ist der Sinuswert mit einem Phasenversatz von 90° (32 Ticks)
        value = cls.getSineValue((angle + 32) % 128)
        print(f"Cosine value for angle {angle}: {value}")
        return value
