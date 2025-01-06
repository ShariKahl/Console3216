from MidiCommand import Command, CommandType


class Song:
    def __init__(self):
        """
        Initialisiert einen MIDI-Song.
        """
        self.__myMask: int = 1 << 7
        self.__dataStart: bytearray = bytearray()  # Song-Daten als bytearray
        self.__offset: int = 0
        self.__ppq: int = 0  # Pulses per Quarter Note

    def __read_byte(self, address: int) -> int:
        """
        Liest ein Byte aus den Song-Daten.
        :param address: Adresse des Bytes
        :return: Das gelesene Byte
        """
        if address >= len(self.__dataStart):
            raise IndexError(f"Address {address} out of bounds for song data.")
        return self.__dataStart[address]

    def __findDeltaTime(self) -> int:
        """
        Findet die Delta-Time (Zeit bis zum nächsten Kommando).
        :return: Die berechnete Delta-Time
        """
        currentByte: int = self.__read_byte(self.__offset)
        deltaTime: int = 0

        while currentByte & self.__myMask != 0:
            currentByte &= 0x7F  # 0b01111111
            deltaTime = (deltaTime << 7) + currentByte
            self.__offset += 1
            currentByte = self.__read_byte(self.__offset)

        deltaTime = (deltaTime << 7) + currentByte
        self.__offset += 1
        return deltaTime

    def reset(self):
        """
        Setzt den Song zurück.
        """
        self.setSong(self.__dataStart)

    def nextCommand(self) -> Command:
        """
        Liest das nächste MIDI-Kommando aus den Song-Daten.
        :return: Das nächste Kommando als Command-Objekt
        """
        command = Command()
        command.deltaTime = self.__findDeltaTime()
        currentByte: int = self.__read_byte(self.__offset)

        if currentByte >> 4 == 0xF:  # Meta-Event
            self.__offset += 1
            currentByte = self.__read_byte(self.__offset)
            if currentByte == 0x51:  # Set Tempo
                self.__offset += 1
                command.data.setTempo.tempo[0] = self.__read_byte(self.__offset)
                self.__offset += 1
                command.data.setTempo.tempo[1] = self.__read_byte(self.__offset)
                self.__offset += 1
                command.data.setTempo.tempo[2] = self.__read_byte(self.__offset)
                self.__offset += 1
                command.type = CommandType.SetTempo
            else:
                command.type = CommandType.EndOfTrack
                self.__offset += 3
        elif currentByte >> 4 == 0xB:  # Controller Change
            command.data.controllerChange.channel = currentByte & 0x0F
            self.__offset += 1
            command.data.controllerChange.controller = self.__read_byte(self.__offset)
            self.__offset += 1
            command.data.controllerChange.value = self.__read_byte(self.__offset)
            self.__offset += 1
            command.type = CommandType.ControllerChange
        elif currentByte >> 4 == 0xC:  # Program Change
            command.data.programChange.channel = currentByte & 0x0F
            self.__offset += 1
            command.data.programChange.programNumber = self.__read_byte(self.__offset)
            self.__offset += 1
            command.type = CommandType.ProgramChange
        elif currentByte >> 4 == 0x8:  # Note Off
            command.data.noteOff.channel = currentByte & 0x0F
            self.__offset += 1
            command.data.noteOff.note = self.__read_byte(self.__offset)
            self.__offset += 1
            command.data.noteOff.velocity = self.__read_byte(self.__offset)
            self.__offset += 1
            command.type = CommandType.NoteOff
        elif currentByte >> 4 == 0x9:  # Note On
            command.data.noteOn.channel = currentByte & 0x0F
            self.__offset += 1
            command.data.noteOn.note = self.__read_byte(self.__offset)
            self.__offset += 1
            command.data.noteOn.velocity = self.__read_byte(self.__offset)
            self.__offset += 1
            command.type = CommandType.NoteOn

        return command

    def setSong(self, songData: bytearray):
        """
        Lädt einen neuen Song in den Player.
        :param songData: Die Song-Daten als bytearray
        """
        self.__offset = 0
        self.__dataStart = songData
        # Set PPQ
        self.__ppq = (self.__read_byte(self.__offset) << 8) + self.__read_byte(self.__offset + 1)
        self.__offset += 2

    def getPPQ(self) -> int:
        """
        Gibt die Pulses per Quarter Note zurück.
        :return: PPQ-Wert
        """
        return self.__ppq
