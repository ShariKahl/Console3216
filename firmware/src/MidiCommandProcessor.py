from MidiCommand import *
from Sound import *

# TODO Comment aus C++ Source
# The "high resolution continuous controller" Commands use 14 bits of precision.
# The 14 bits are split into the value fields of two different commands.
# However we just skip the least significant values (LSB) and only handle the
# most significant (MSB) since the extra precision isn't useful on out device.
CTRL_MSB_CHANNEL_VOLUME = 7
CTRL_MSB_PAN = 10
CTRL_LSB_CHANNEL_VOLUME = 39
CTRL_LSB_PAN = 42
CTRL_ALL_SOUND_OFF = 120
CTRL_ALL_NOTES_OFF = 123


# TODO In C++ als static Funktion deklariert
def processControllerChange(channel: int, controller: int, value: int):
    # TODO In C++ switch/case
    if controller == CTRL_MSB_CHANNEL_VOLUME:
        Sound.setVolumeCh(value, channel)
    elif controller == CTRL_MSB_PAN:
        Sound.setPanoramaCh(value, channel)
    
        # TODO Comment aus C++ Source
        # Not handled, see comment above.
        # case CTRL_LSB_CHANNEL_VOLUME:
        # case CTRL_LSB_PAN:
    elif controller in [CTRL_ALL_NOTES_OFF, CTRL_ALL_NOTES_OFF]:
        Sound.stopSounds()
        Sound.stopSoundEffects()
    pass

def processCommand(command: Command):
    # TODO In C++ switch/case
    if command.type == CommandType.NoteOn:
        Sound.playSound(command.data.noteOn.note, command.data.noteOn.channel)
    elif command.type == CommandType.NoteOff:
        Sound.stopSound(command.data.noteOn.note, command.data.noteOn.channel)
    elif command.type == CommandType.ProgramChange:
        # TODO Comment aus C++ Source:
        # Daniel: setPreset?
        pass
    elif command.type == CommandType.ControllerChange:
        processControllerChange(command.data.controllerChange.channel,
                                command.data.controllerChange.controller,
                                command.data.controllerChange.value)
    pass
