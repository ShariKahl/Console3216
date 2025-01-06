import serial
from ctypes import Union, c_int16, c_int8, Structure

class halfValue(Structure):
    _fields_ = [("secondByte", c_int8), ("firstByte", c_int8)]

class byteConverter(Union):
    _fields_ = [("value", c_int16), ("h", halfValue)]

class MIDI_Control_Commands:
    __SERIAL_BAUD = 31250  # Standard-Baudrate für MIDI-Kommunikation
    __COMMAND_CODE_PLAY_TRACK = 0x01
    __COMMAND_CODE_CHANGE_TEMPO = 0x02
    __COMMAND_CODE_PAUSE_TRACK = 0x03
    __COMMAND_CODE_STOP_TRACK = 0x04
    __COMMAND_CODE_RESUME_TRACK = 0x05
    __COMMAND_CODE_RESTART_TRACK = 0x06

    __serial_connection = None  # Serielle Verbindung

    @classmethod
    def setupMidi(cls, port: str = "/dev/serial0"):
        """
        Initialisiert die MIDI-Kommunikation.
        :param port: Serieller Port, standardmäßig "/dev/serial0" für UART.
        """
        try:
            cls.__serial_connection = serial.Serial(
                port=port,
                baudrate=cls.__SERIAL_BAUD,
                bytesize=serial.EIGHTBITS,
                stopbits=serial.STOPBITS_ONE,
                parity=serial.PARITY_NONE
            )
            print(f"MIDI serial connection initialized on {port} at {cls.__SERIAL_BAUD} baud.")
        except serial.SerialException as e:
            print(f"Failed to initialize MIDI serial connection: {e}")

    @classmethod
    def __serialWriteData(cls, command: int, trackId: int, tempo: int = -1):
        """
        Sendet MIDI-Daten über die serielle Verbindung.
        :param command: Befehlscode
        :param trackId: ID des Tracks
        :param tempo: (optional) Tempo
        """
        if cls.__serial_connection is None or not cls.__serial_connection.is_open:
            print("Error: Serial connection is not open.")
            return -1

        byteConv = byteConverter()
        byteConv.value = trackId

        firstByteTrackId = byteConv.h.firstByte
        secondByteTrackId = byteConv.h.secondByte

        if tempo != -1:
            byteConv.value = tempo
            firstByteTempo = byteConv.h.firstByte
            secondByteTempo = byteConv.h.secondByte

            data = bytearray([
                command,
                firstByteTrackId & 0xFF,
                secondByteTrackId & 0xFF,
                firstByteTempo & 0xFF,
                secondByteTempo & 0xFF
            ])
        else:
            data = bytearray([
                command,
                firstByteTrackId & 0xFF,
                secondByteTrackId & 0xFF
            ])

        try:
            cls.__serial_connection.write(data)
            print(f"Sent MIDI data: {data}")
        except serial.SerialException as e:
            print(f"Failed to send MIDI data: {e}")
            return -1

        return 0

    @classmethod
    def playTrack(cls, trackId: int, tempo: int) -> int:
        return cls.__serialWriteData(cls.__COMMAND_CODE_PLAY_TRACK, trackId, tempo)

    @classmethod
    def changeTempo(cls, trackId: int, tempo: int) -> int:
        return cls.__serialWriteData(cls.__COMMAND_CODE_CHANGE_TEMPO, trackId, tempo)

    @classmethod
    def pauseTrack(cls, trackId: int) -> int:
        return cls.__serialWriteData(cls.__COMMAND_CODE_PAUSE_TRACK, trackId)

    @classmethod
    def stopTrack(cls, trackId: int) -> int:
        return cls.__serialWriteData(cls.__COMMAND_CODE_STOP_TRACK, trackId)

    @classmethod
    def resumeTrack(cls, trackId: int) -> int:
        return cls.__serialWriteData(cls.__COMMAND_CODE_RESUME_TRACK, trackId)

    @classmethod
    def restartTrack(cls, trackId: int) -> int:
        return cls.__serialWriteData(cls.__COMMAND_CODE_RESTART_TRACK, trackId)

    @classmethod
    def closeConnection(cls):
        """Schließt die serielle Verbindung."""
        if cls.__serial_connection and cls.__serial_connection.is_open:
            cls.__serial_connection.close()
            print("MIDI serial connection closed.")
