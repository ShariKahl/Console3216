import threading
import time

TIME_BASIS_MS = 20  # Zeitbasis in Millisekunden
MAIN_TIMER_PERIOD = 1250  # Timer-Periode (nicht direkt benötigt in Python)

class MainClockStatus_t:
    """Statusstruktur für den MainClock."""
    def __init__(self):
        self.systemTick: int = 0
        self.systemTickOverflow: int = 0


class MainClock:
    """Softwarebasierter Ersatz für den MainClock-Timer."""
    __systemTime: int = 0  # Gesamtzeit in Ticks

    def __init__(self):
        self.__status = MainClockStatus_t()
        self.__timer = None
        self.__running = False

    def startTimer(self):
        """Startet den Timer."""
        self.__running = True
        self.__schedule_next_tick()

    def stopTimer(self):
        """Stoppt den Timer."""
        self.__running = False
        if self.__timer:
            self.__timer.cancel()

    def __schedule_next_tick(self):
        """Plant den nächsten Tick ein."""
        if self.__running:
            self.__timer = threading.Timer(TIME_BASIS_MS / 1000.0, self.__tick)
            self.__timer.start()

    def __tick(self):
        """Wird bei jedem Timer-Tick aufgerufen."""
        self.setTick()
        self.__schedule_next_tick()

    def setTick(self):
        """Setzt den Tick-Status und erhöht die Systemzeit."""
        if self.__status.systemTick != 0:
            self.__status.systemTickOverflow = 1
        self.__status.systemTick = 1
        type(self).__systemTime += 1

    def isTick(self) -> bool:
        """Prüft, ob ein Tick aktiv ist."""
        if self.__status.systemTick == 1:
            self.__status.systemTick = 0
            return True
        return False

    def hasOverflow(self) -> bool:
        """Prüft, ob ein Überlauf aufgetreten ist."""
        if self.__status.systemTickOverflow == 1:
            self.clearOverflow()
            return True
        return False

    def clearOverflow(self):
        """Löscht den Überlauf-Status."""
        self.__status.systemTickOverflow = 0

    @classmethod
    def getSystemTime(cls) -> int:
        """Gibt die Systemzeit in Millisekunden zurück."""
        return cls.__systemTime * TIME_BASIS_MS


# Globale Instanz des MainClock
mainClock = MainClock()
