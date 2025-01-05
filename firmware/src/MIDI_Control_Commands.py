
# TODO Nicht sicher, ob es auch ohne die C Union geht
from ctypes import Union, c_int16, c_int8, Structure


class halfValue(Structure):
        _fields_ = [("secondByte", c_int8),
                    ("firstByte", c_int8)]

# TODO Eventuell kommen wir auch ohne aus
# C++ Code:
# union byteConverter {
#     uint16_t value;
#     struct {
#         int8_t secondByte;
#         int8_t firstByte;
#     };
# };

# TODO Muss getestet werden
class byteConverter(Union):
    _anonymous_ = ("h",)
    _fields_ = [("value", c_int16),
                ("h", halfValue)]


class MIDI_Control_Commands:
    __SERIAL_BAUD = 74880
    __COMMAND_CODE_PLAY_TRACK = 0x01
    __COMMAND_CODE_CHANGE_TEMPO = 0x02
    __COMMAND_CODE_PAUSE_TRACK = 0x03
    __COMMAND_CODE_STOP_TRACK = 0x04
    __COMMAND_CODE_RESUME_TRACK = 0x05
    __COMMAND_CODE_RESTART_TRACK = 0x06

    def __init__(self) -> None:
        pass

    # Hilfsmethode
    @classmethod
    def __serialWriteData(cls, command: int, trackId: int, tempo: int = -1):
        byteConv: byteConverter = byteConverter()
        byteConv.value = trackId

        firstByteTrackId = byteConv.firstByte
        secondByteTrackId = byteConv.secondByte

        if tempo != -1:
            byteConv.value = tempo
            firstByteTempo = byteConv.firstByte
            secondByteTempo = byteConv.secondByte

            data = [
                command,
                firstByteTrackId,
                secondByteTrackId,
                firstByteTempo,
                secondByteTempo
            ]
        else:
            data = [
                command,
                firstByteTrackId,
                secondByteTrackId
            ]
        
        # TODO C++ Quellcode:
        # TODO pyserial
        # MIDI_SERIAL.write(data, 5);
        # MIDI_SERIAL ist Serial aus Arduino Code

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
    def setupMidi(cls):
        # TODO C++ Quellcode:
        # MIDI_SERIAL.begin(MIDI_Control_Commands::SERIAL_BAUD);
        pass
