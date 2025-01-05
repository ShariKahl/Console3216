
class TimingManager:
    def __init__(self, orig = None): # TODO orig = Typ TimingManager
        self.__ticksSinceLastCommand: int = 0
        self.__ppq: int = 1
        self.__mspq: int = 1
        self.__delayUntilNext: int = 0
        pass
    
    def advanceTick(self):
        self.__ticksSinceLastCommand += 1
        pass
    
    def isCommandReady(self) -> bool:
        return self.__ticksSinceLastCommand >= self.__delayUntilNext
    
    def setDelayUntilNextCommand(self, duration: int):
        self.__delayUntilNext = duration
        self.__reset()
        pass
    
    def isBeatEnd(self) -> bool:
        return self.__ticksSinceLastCommand % self.__ppq == 0
    
    def setPPQ(self, ppq: int):
        if ppq < 1:
            ppq = 1
        self.__ppq = ppq
        # TODO
        updateInterrupt(self.__mspq, self.__ppq)
        pass
    
    def setMSPQ(self, mspq: int):
        if mspq < 1:
            mspq = 1
        self.__mspq = mspq
        
        # TODO
        updateInterrupt(self.__mspq, self.__ppq)
        pass
    
    def __reset(self):
        self.__ticksSinceLastCommand = 0
        pass
