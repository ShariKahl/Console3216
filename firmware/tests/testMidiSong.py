from MidiCommand import CommandType
from MidiSong import Song

# Beispiel-Songdaten (als bytearray)
song_data = bytearray([
    0x00, 0x60,  # PPQ
    0x90, 0x3C, 0x64,  # Note On (Channel 0, Note 60, Velocity 100)
    0x00, 0x80, 0x3C, 0x00,  # Note Off (Channel 0, Note 60, Velocity 0)
    0xFF, 0x51, 0x03, 0x07, 0xA1, 0x20  # Set Tempo (500,000 µs per quarter note)
])

# Song laden und testen
song = Song()
song.setSong(song_data)

print(f"PPQ: {song.getPPQ()}")
while True:
    command = song.nextCommand()
    print(command)
    if command.type == CommandType.EndOfTrack:
        break
