from MidiSong import *
from MidiTimingManager import *
from MidiCommand import *
from MidiCommandProcessor import *

class Player:
    def __init__(self):
        # TODO C++ Source:
        # char* nextSong = nullptr;
        self.__nextSong: int = 0
        self.__song: Song = Song()
        self.__timing: TimingManager = TimingManager()
        pass
    
    def advanceTick(self) -> bool:
        self.__timing.advanceTick()
        
        if self.__timing.isBeatEnd() and self.__nextSong != 0: # TODO nextSong != nullptr
            self.__song.setSong(self.__nextSong)
            self.__timing.setPPQ(self.__song.getPPQ())
            self.__nextSong = 0 # TODO nullptr
        
        finishedPlayingTrack: bool = False
        
        while self.__timing.isCommandReady():
            cmd: Command = self.__song.nextCommand()
            
            # TODO In C++ switch/case
            if cmd.type == CommandType.SetTempo:
                # Comment aus C++ Source:
                # tempo in micro seconds
                tempo: int = (int(cmd.data.setTempo.tempo[0]) << 16) | (int(cmd.data.setTempo.tempo[1]) << 8) | int(cmd.data.setTempo.tempo[2])
                self.__timing.setMSPQ(tempo)
            elif cmd.type == CommandType.EndOfTrack:
                self.__song.reset()
                finishedPlayingTrack = True
            else:
                processCommand(cmd)
            
            self.__timing.setDelayUntilNextCommand(cmd.deltaTime)
        
        return finishedPlayingTrack
    
    def setSong(self, data):
        self.__nextSong = data
        pass
    
    
    