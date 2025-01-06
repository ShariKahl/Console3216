from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Union


class CommandType(Enum):
    """Typen von MIDI-Befehlen."""
    NoteOn = 0
    NoteOff = 1
    ProgramChange = 2
    ControllerChange = 3
    EndOfTrack = 4
    SetTempo = 5


@dataclass
class EmptyEvent:
    """Leeres Ereignis (z. B. End of Track)."""
    pass


@dataclass
class NoteEvent:
    """Daten für Note On/Off."""
    channel: int = 0
    note: int = 0
    velocity: int = 0


@dataclass
class ProgramChangeEvent:
    """Daten für Program Change."""
    channel: int = 0
    programNumber: int = 0


@dataclass
class ControllerChangeEvent:
    """Daten für Controller Change."""
    channel: int = 0
    controller: int = 0
    value: int = 0


@dataclass
class SetTempoEvent:
    """Daten für Set Tempo."""
    tempo: List[int] = field(default_factory=lambda: [0, 0, 0])


@dataclass
class Command:
    """Eine MIDI-Kommandostruktur."""
    deltaTime: int = 0
    type: CommandType = CommandType.NoteOn
    data: Union[NoteEvent, ProgramChangeEvent, ControllerChangeEvent, EmptyEvent, SetTempoEvent, None] = None

def create_note_on_command(channel: int, note: int, velocity: int, deltaTime: int = 0) -> Command:
    """Erzeugt einen Note-On-Befehl."""
    return Command(
        deltaTime=deltaTime,
        type=CommandType.NoteOn,
        data=NoteEvent(channel=channel, note=note, velocity=velocity)
    )


def create_program_change_command(channel: int, programNumber: int, deltaTime: int = 0) -> Command:
    """Erzeugt einen Program-Change-Befehl."""
    return Command(
        deltaTime=deltaTime,
        type=CommandType.ProgramChange,
        data=ProgramChangeEvent(channel=channel, programNumber=programNumber)
    )
