from enum import Enum
from ctypes import Structure, Union, c_ubyte, c_uint

# TODO C++ Code:
# enum CommandType {
#     NoteOn,
#     NoteOff,
#     ProgramChange,
#     ControllerChange,
#     EndOfTrack,
#     SetTempo,
# };

class CommandType(Enum):
    NoteOn = 0
    NoteOff = 1
    ProgramChange = 2
    ControllerChange = 3
    EndOfTrack = 4
    SetTempo = 5


class EmptyEvent:
    pass

# # TODO C++ Code:
# # struct EmptyEvent {};
# class EmptyEvent(Structure):
#     _fields_ = []


class NoteEvent:
    def __init__(self):
        self.channel: int = 0
        self.note: int = 0
        self.velocity: int = 0

# class NoteEvent(Structure):
#     # TODO In C++ sind alle Variablen unsigned chars, c_uchar existiert nicht
#     _fields_ = [("channel", c_ubyte), ("note", c_ubyte), ("velocity", c_ubyte)]


class ProgramChangeEvent:
    def __init__(self):
        self.channel: int = 0
        self.programNumber: int = 0

# class ProgramChangeEvent(Structure):
#     # TODO In C++ sind alle Variablen unsigned chars, c_uchar existiert nicht
#     _fields_ = [("channel", c_ubyte), ("programNumber", c_ubyte)]


class ControllerChangeEvent:
    def __init__(self):
        self.channel: int = 0
        self.controller: int = 0
        self.value: int = 0

# class ControllerChangeEvent(Structure):
#     # TODO In C++ sind alle Variablen unsigned chars, c_uchar existiert nicht
#     _fields = [("channel", c_ubyte), ("controller", c_ubyte), ("value", c_ubyte)]


class SetTempoEvent:
    def __init__(self):
        self.tempo = [0 for _ in range(3)]

# class SetTempoEvent(Structure):
#     _fields_ = [("tempo", char_array)]


# Externe Union Definition für Command
class DataUnion(Union):
    _fields_ = [("noteOn", NoteEvent),
                ("noteOff", NoteEvent),
                ("programChange", ProgramChangeEvent),
                ("controllerChange", ControllerChangeEvent),
                ("endOfTrack", EmptyEvent),
                ("setTempo", SetTempoEvent)]


# TODO Experimental
class Command:
    def __init__(self):
        self.deltaTime: int = 0
        self.type: CommandType = None
        self.data: DataUnion = DataUnion()

# class Command(Structure):
#     _fields_ = [("deltaTime", c_uint),
#                 ("type", CommandType),
#                 ("data", DataUnion)]

# C++ Source:
# struct Command {
#     unsigned deltaTime;

#     CommandType type;
#     union {
#         NoteEvent noteOn;
#         NoteEvent noteOff;
#         ProgramChangeEvent programChange;
#         ControllerChangeEvent controllerChange;
#         EmptyEvent endOfTrack;
#         SetTempoEvent setTempo;
#     } data;
# };
