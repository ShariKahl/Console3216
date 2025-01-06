from MIDI_Control_Commands import MIDI_Control_Commands

# MIDI-Setup
MIDI_Control_Commands.setupMidi(port="/dev/serial0")

# Test: Einen Track abspielen
MIDI_Control_Commands.playTrack(trackId=1, tempo=120)

# Test: Tempo ändern
MIDI_Control_Commands.changeTempo(trackId=1, tempo=140)

# Verbindung schließen
MIDI_Control_Commands.closeConnection()
