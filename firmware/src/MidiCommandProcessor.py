from MidiCommand import Command, CommandType
from Sound import Sound

# MIDI-Controller-Kommandos
CTRL_MSB_CHANNEL_VOLUME = 7
CTRL_MSB_PAN = 10
CTRL_LSB_CHANNEL_VOLUME = 39
CTRL_LSB_PAN = 42
CTRL_ALL_SOUND_OFF = 120
CTRL_ALL_NOTES_OFF = 123


def processControllerChange(channel: int, controller: int, value: int):
    """
    Verarbeitet Controller-Change-Befehle.
    :param channel: MIDI-Kanal
    :param controller: Controller-Nummer
    :param value: Wert des Controllers
    """
    if controller == CTRL_MSB_CHANNEL_VOLUME:
        print(f"Setting channel volume: channel={channel}, value={value}")
        Sound.setVolumeCh(value, channel)
    elif controller == CTRL_MSB_PAN:
        print(f"Setting panorama: channel={channel}, value={value}")
        Sound.setPanoramaCh(value, channel)
    elif controller in [CTRL_ALL_SOUND_OFF, CTRL_ALL_NOTES_OFF]:
        print("Stopping all sounds and effects.")
        Sound.stopSounds()
        Sound.stopSoundEffects()
    else:
        print(f"Unhandled controller: {controller} (channel={channel}, value={value})")


def processCommand(command: Command):
    """
    Verarbeitet einen MIDI-Befehl.
    :param command: Der zu verarbeitende MIDI-Befehl
    """
    if command.type == CommandType.NoteOn:
        note_event = command.data
        print(f"Note On: channel={note_event.channel}, note={note_event.note}, velocity={note_event.velocity}")
        Sound.playSound(note_event.note, note_event.channel)
    elif command.type == CommandType.NoteOff:
        note_event = command.data
        print(f"Note Off: channel={note_event.channel}, note={note_event.note}")
        Sound.stopSound(note_event.note, note_event.channel)
    elif command.type == CommandType.ProgramChange:
        program_event = command.data
        print(f"Program Change: channel={program_event.channel}, program={program_event.programNumber}")
        # Hier könnte eine Funktion wie `Sound.setPreset()` aufgerufen werden.
    elif command.type == CommandType.ControllerChange:
        controller_event = command.data
        print(f"Controller Change: channel={controller_event.channel}, controller={controller_event.controller}, value={controller_event.value}")
        processControllerChange(controller_event.channel, controller_event.controller, controller_event.value)
    elif command.type == CommandType.SetTempo:
        tempo_event = command.data
        tempo = (tempo_event.tempo[0] << 16) | (tempo_event.tempo[1] << 8) | tempo_event.tempo[2]
        print(f"Set Tempo: {tempo} μs per quarter note")
        Sound.setTempo(tempo)
    else:
        print(f"Unknown command type: {command.type}")
