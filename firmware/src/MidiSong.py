from MidiCommand import *


class Song:
    def __init(self):
        self.__myMask: int = 1 << 7
        self.__dataStart: int = 0 # nullptr
        self.__offset: int = 0
        self.__ppq: int = 0
        pass
    
    # TODO Dummy Definition
    def pgm_read_byte_near(self):
        pass
    
    def __findDeltaTime(self):
        # TODO Arduino Code:
        # Makro Definition aus "hardware/tools/avr/avr/include/avr/pgmspace.h"
        # #define pgm_read_byte_near(address_short) __LPM((uint16_t)(address_short))
        # https://garretlab.web.fc2.com/en/arduino/inside/hardware/tools/avr/avr/include/avr/pgmspace.h/pgm_read_byte_near.html
        currentByte: int = self.pgm_read_byte_near(self.__dataStart + self.__offset)
        deltaTime: int = 0
        
        if currentByte & self.__myMask != 0:
            while currentByte & self.__myMask != 0:
                currentByte &= 0b01111111 # 0x7F
                deltaTime = (deltaTime << 7) + currentByte
                self.__offset += 1
                currentByte = self.pgm_read_byte_near(self.__dataStart + self.__offset)
            
        deltaTime = (deltaTime << 7) + currentByte
        return deltaTime
    
    def reset(self):
        self.setSong(self.__dataStart)
        pass
    
    def nextCommand(self) -> Command:
        command: Command = Command()
        command.deltaTime = self.__findDeltaTime()
        currentByte: int = self.pgm_read_byte_near(self.__dataStart + self.__offset)
        
        # TODO In C++ switch/case
        if currentByte >> 4 == 0xF:
            self.__offset += 1
            currentByte = self.pgm_read_byte_near(self.__dataStart + self.__offset)
            if currentByte == 0b01010001:
                self.__offset += 2
                command.data.setTempo.tempo[0] = self.pgm_read_byte_near(self.__dataStart + self.__offset)
                self.__offset += 1
                command.data.setTempo.tempo[1] = self.pgm_read_byte_near(self.__dataStart + self.__offset)
                self.__offset += 1
                command.data.setTempo.tempo[2] = self.pgm_read_byte_near(self.__dataStart + self.__offset)
                self.__offset += 1
                command.type = CommandType.SetTempo
            else:
                command.type = CommandType.EndOfTrack
                self.__offset += 3
        elif currentByte >> 4 == 0xB:
            command.data.controllerChange.channel = currentByte & 0b00001111
            self.__offset += 1
            currentByte = self.pgm_read_byte_near(self.__dataStart + self.__offset)
            command.data.controllerChange.controller = currentByte
            self.__offset += 1
            currentByte = self.pgm_read_byte_near(self.__dataStart + self.__offset)
            command.data.controllerChange.value = currentByte
            self.__offset += 1
            command.type = CommandType.ControllerChange
        elif currentByte >> 4 == 0xC:
            command.data.programChange.channel = currentByte & 0b00001111
            self.__offset += 1
            currentByte = self.pgm_read_byte_near(self.__dataStart + self.__offset)
            command.data.programChange.programNumber = currentByte
            self.__offset += 1
            command.type = CommandType.ProgramChange
        elif currentByte >> 4 == 0x8:
            command.data.noteOff.channel = currentByte & 0b00001111
            self.__offset += 1
            currentByte = self.pgm_read_byte_near(self.__dataStart + self.__offset)
            command.data.noteOff.note = currentByte
            self.__offset += 1
            currentByte = self.pgm_read_byte_near(self.__dataStart + self.__offset)
            command.data.noteOff.velocity = currentByte
            self.__offset += 1
            command.type = CommandType.NoteOff
        elif currentByte >> 4 == 0x9:
            command.data.noteOn.channel = currentByte & 0b00001111
            self.__offset += 1
            currentByte = self.pgm_read_byte_near(self.__dataStart + self.__offset)
            command.data.noteOn.note = currentByte
            self.__offset += 1
            currentByte = self.pgm_read_byte_near(self.__dataStart + self.__offset)
            command.data.noteOn.velocity = currentByte
            self.__offset += 1
            command.type = CommandType.NoteOn
        
        return command
    
    def setSong(self, songData: int):
        self.__offset = 0
        self.__dataStart = songData
        # Set PPQ
        self.__ppq = 0
        self.__ppq += (self.pgm_read_byte_near(self.__dataStart + (self.__offset)) << 8)
        self.__offset += 1
        self.__ppq += self.pgm_read_byte_near(self.__dataStart + (self.__offset))
        self.__offset += 1
        pass
    
    def getPPQ(self) -> int:
        return 1
    