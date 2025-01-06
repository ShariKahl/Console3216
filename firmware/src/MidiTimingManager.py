class TimingManager:
    def __init__(self):
        """
        Initialisiert den Timing-Manager.
        """
        self.__ticksSinceLastCommand: int = 0
        self.__ppq: int = 1  # Pulses per Quarter Note
        self.__mspq: int = 1  # Millisekunden pro Quarter Note
        self.__delayUntilNext: int = 0

    def advanceTick(self):
        """
        Erhöht den Tick-Zähler.
        """
        self.__ticksSinceLastCommand += 1
        print(f"Advanced tick: {self.__ticksSinceLastCommand}")

    def isCommandReady(self) -> bool:
        """
        Überprüft, ob der nächste MIDI-Befehl verarbeitet werden kann.
        :return: True, wenn der nächste Befehl bereit ist.
        """
        return self.__ticksSinceLastCommand >= self.__delayUntilNext

    def setDelayUntilNextCommand(self, duration: int):
        """
        Setzt die Verzögerung bis zum nächsten MIDI-Befehl.
        :param duration: Verzögerung in Ticks
        """
        self.__delayUntilNext = duration
        self.__reset()
        print(f"Delay until next command set to: {self.__delayUntilNext}")

    def isBeatEnd(self) -> bool:
        """
        Überprüft, ob das Ende eines Beats erreicht wurde.
        :return: True, wenn ein Beat-Ende erreicht ist.
        """
        return self.__ticksSinceLastCommand % self.__ppq == 0

    def setPPQ(self, ppq: int):
        """
        Setzt die Pulses per Quarter Note.
        :param ppq: PPQ-Wert (muss >= 1 sein)
        """
        if ppq < 1:
            ppq = 1
        self.__ppq = ppq
        print(f"PPQ set to: {self.__ppq}")
        self.__updateInterrupt()

    def setMSPQ(self, mspq: int):
        """
        Setzt die Millisekunden pro Quarter Note.
        :param mspq: MSPQ-Wert (muss >= 1 sein)
        """
        if mspq < 1:
            mspq = 1
        self.__mspq = mspq
        print(f"MSPQ set to: {self.__mspq}")
        self.__updateInterrupt()

    def __reset(self):
        """
        Setzt den Tick-Zähler zurück.
        """
        self.__ticksSinceLastCommand = 0
        print("Tick counter reset.")

    def __updateInterrupt(self):
        """
        Aktualisiert die Interrupt-Einstellungen basierend auf MSPQ und PPQ.
        """
        print(f"Updating interrupt with MSPQ={self.__mspq}, PPQ={self.__ppq}")
        # Hier könnte die `updateInterrupt`-Logik implementiert werden.
        # Beispiel: updateInterrupt(self.__mspq, self.__ppq)

    def getPPQ(self) -> int:
        """
        Gibt den aktuellen PPQ-Wert zurück.
        :return: PPQ-Wert
        """
        return self.__ppq

    def getMSPQ(self) -> int:
        """
        Gibt den aktuellen MSPQ-Wert zurück.
        :return: MSPQ-Wert
        """
        return self.__mspq
