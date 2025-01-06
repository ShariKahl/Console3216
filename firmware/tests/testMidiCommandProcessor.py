from MidiCommand import Command, CommandType, NoteEvent, ControllerChangeEvent, SetTempoEvent
from MidiCommandProcessor import CTRL_MSB_CHANNEL_VOLUME, processCommand

def test_midi_processor():
    # Test: Note On
    note_on_command = Command(
        deltaTime=0,
        type=CommandType.NoteOn,
        data=NoteEvent(channel=1, note=60, velocity=100)
    )
    processCommand(note_on_command)

    # Test: Controller Change
    controller_change_command = Command(
        deltaTime=0,
        type=CommandType.ControllerChange,
        data=ControllerChangeEvent(channel=1, controller=CTRL_MSB_CHANNEL_VOLUME, value=127)
    )
    processCommand(controller_change_command)

    # Test: Tempo Change
    tempo_command = Command(
        deltaTime=0,
        type=CommandType.SetTempo,
        data=SetTempoEvent(tempo=[0x07, 0xA1, 0x20])  # 500.000 μs per quarter note
    )
    processCommand(tempo_command)

test_midi_processor()
