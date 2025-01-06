from MidiCommand import create_note_on_command, create_program_change_command


def test_midi_commands():
    # Note-On-Befehl erstellen
    note_on = create_note_on_command(channel=1, note=60, velocity=100, deltaTime=120)
    print(note_on)

    # Program-Change-Befehl erstellen
    program_change = create_program_change_command(channel=1, programNumber=5, deltaTime=240)
    print(program_change)

test_midi_commands()
