from MidiSong import Song
from MidiTimingManager import TimingManager
from MidiCommand import Command, CommandType
from MidiCommandProcessor import processCommand


class Player:
    def __init__(self):
        """
        Initialisiert den MIDI-Player.
        """
        self.__nextSong: int = None  # Nächster Song (ersetzt nullptr durch None)
        self.__song: Song = Song()
        self.__timing: TimingManager = TimingManager()

    def advanceTick(self) -> bool:
        """
        Führt einen Tick fort und verarbeitet MIDI-Kommandos.
        :return: True, wenn das aktuelle Track-Ende erreicht wurde.
        """
        self.__timing.advanceTick()

        # Wenn ein neuer Song bereit ist und das Beat-Ende erreicht wurde
        if self.__timing.isBeatEnd() and self.__nextSong is not None:
            print(f"Setting new song: {self.__nextSong}")
            self.__song.setSong(self.__nextSong)
            self.__timing.setPPQ(self.__song.getPPQ())
            self.__nextSong = None

        finishedPlayingTrack: bool = False

        # Verarbeite alle bereitstehenden Kommandos
        while self.__timing.isCommandReady():
            cmd: Command = self.__song.nextCommand()
            print(f"Processing command: {cmd.type}")

            if cmd.type == CommandType.SetTempo:
                # Tempo in Mikrosekunden
                tempo: int = (cmd.data.tempo[0] << 16) | (cmd.data.tempo[1] << 8) | cmd.data.tempo[2]
                print(f"Setting tempo: {tempo} μs per quarter note")
                self.__timing.setMSPQ(tempo)
            elif cmd.type == CommandType.EndOfTrack:
                print("End of track reached. Resetting song.")
                self.__song.reset()
                finishedPlayingTrack = True
            else:
                processCommand(cmd)

            # Verzögerung bis zum nächsten Kommando setzen
            self.__timing.setDelayUntilNextCommand(cmd.deltaTime)

        return finishedPlayingTrack

    def setSong(self, data: int):
        """
        Setzt einen neuen Song, der nach dem aktuellen abgespielt wird.
        :param data: Song-Daten
        """
        print(f"Queueing next song: {data}")
        self.__nextSong = data
