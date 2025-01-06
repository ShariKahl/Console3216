from MidiPlayer import Player
from MidiSong import Song

def test_player():
    player = Player()
    song_data = 42  # Beispiel-Songdaten

    # Neuen Song setzen
    player.setSong(song_data)

    # Simuliere Ticks
    for _ in range(10):
        finished = player.advanceTick()
        if finished:
            print("Track finished.")

test_player()
