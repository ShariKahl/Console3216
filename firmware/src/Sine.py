
sinetable = [
    0, 6, 13, 19, 25, 31, 37, 43,
    49, 55, 60, 66, 71, 76, 81, 86,
    91, 95, 99, 103, 106, 110, 113, 116,
    118, 121, 122, 124, 126, 127, 127, 128, 128
]

class Sine:
    def __init__(self) -> None:
        pass

    # Hilfsmethode
    # Reproduziert das Verhalten des Modulo Operators aus C++.
    @classmethod
    def __cpp_mod(cls, dividend: int, divisor: int) -> int:
        sign = 1 if dividend >= 0 else -1
        dividend, divisor = abs(dividend), abs(divisor)
        while dividend >= divisor:
            dividend -= divisor

        return sign * dividend

    @classmethod
    def getSineValue(cls, angle: int) -> int:
        # TODO Python modulo operator
        # angle %= 128
        # TODO C++ Verhalten durch Hilfsmethode
        angle = cls.__cpp_mod(angle, 128)

        # TODO Modulo liefert bei Negativzahlen andere Ergebnisse in Python
        """
        Python:
        i: -128, i % 128: 0
        i: -127, i % 128: 1
        i: -126, i % 128: 2
        ...
        i: -1, i % 128: 127
        i: 0, i % 128: 0
        i: 1, i % 128: 1
        i: 2, i % 128: 2
        ...
        i: 127, i % 128: 127
        
        C++:
        i: -128, i % 128: 0
        i: -127, i % 128: -127
        i: -126, i % 128: -126
        ...
        i: -1, i % 128: -1
        i: 0, i % 128: 0
        i: 1, i % 128: 1
        i: 2, i % 128: 2
        ...
        i: 127, i % 128: 127
        """
        if angle < 0:
            angle = 128 + angle
        if angle < 33:
            return sinetable[angle]
        elif angle < 65:
            return sinetable[64 - angle]
        elif angle < 97:
            return -sinetable[angle - 64]
        elif angle < 128:
            return -sinetable[128 - angle]
        
        return 0

    @classmethod
    def getCosineValue(cls, angle: int) -> int:
        return cls.getSineValue(32 - angle)
