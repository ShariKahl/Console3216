
MIDI_COMMAND_NOTE_OFF = 0x80
MIDI_COMMAND_NOTE_ON = 0x90
MIDI_COMMAND_CONTROL_CHANGE = 0xB0
MIDI_COMMAND_PROGRAMM_CHANGE = 0xC0

class Midi:
    @classmethod
    def init(cls):
        # TODO C++ Quellcode:
        # Serial2.begin(31250);
        # Aus Arduino.h
        pass

    @classmethod
    def noteOn(cls, channel: int, note: int, velocity: int):
        # TODO C++ Quellcode:
        # Serial2.write(MIDI_COMMAND_NOTE_ON | channel);
        # Serial2.write(0x7F & note);
        # Serial2.write(0x7F & velocity);
        # Aus Arduino.h
        pass

    @classmethod
    def noteOff(cls, channel: int, note: int):
        # TODO C++ Quellcode:
        # Serial2.write(MIDI_COMMAND_NOTE_OFF | channel);
        # Serial2.write(0x7F & note);
        # Serial2.write(0x0);
        # Aus Arduino.h
        pass

    @classmethod
    def controlChange(channel: int, control: int, value: int):
        # TODO C++ Quellcode:
        # Serial2.write(MIDI_COMMAND_CONTROL_CHANGE | channel);
        # Serial2.write(control);
        # Serial2.write(value);
        # Aus Arduino.h
        pass

    @classmethod
    def programChange(channel: int, preset: int):
        # TODO C++ Quellcode:
        # Serial2.write(MIDI_COMMAND_PROGRAMM_CHANGE | channel);
        # Serial2.write(preset);
        # Aus Arduino.h
        pass
