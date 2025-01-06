from Midi import Midi

# MIDI-Setup
Midi.init(port="/dev/serial0")

# Test: Note ON und Note OFF
Midi.noteOn(channel=0, note=60, velocity=100)  # Note C4 mit Velocity 100
Midi.noteOff(channel=0, note=60)  # Note C4 aus

# Test: Control Change
Midi.controlChange(channel=0, control=7, value=127)  # Volume auf Maximum

# Test: Program Change
Midi.programChange(channel=0, preset=10)  # Wechsel auf Programm 10

# Verbindung schließen
Midi.close()
