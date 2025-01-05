import random

import CurveFeverPlayer

RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3

SLOW = 4
REGULAR = 2
FAST = 1

MAX_BOOST = 100
MIN_GAP_DURATION = 2
MAX_GAP_DURATION = 4
MIN_TAIL_DURATION = 4
MAX_TAIL_DURATION = 8

NO_ITEM = 0
ITEM_SLOW = 1
ITEM_WALL = 2
ITEM_CLEAR = 3
ITEM_DURATION = 20


# TODO C++: typedef uint8_t Item;
# class Item:
#     pass
Item = int


# TODO C++: typedef struct {...} Position;
class Position:
    def __init__(self):
        self.x: int = 0
        self.y: int = 0


class Player:
    # TODO C++ Source:
    # Outside of scope: uint8_t Player::width = 0;
    #                   uint8_t Player::height = 0;

    # C++: static uint8_t width;
    width: int = 0
    # C++: static uint8_t height;
    height: int = 0

    def __init__(self):
        self.__name: int = 0
        self.__speed: int = REGULAR
        self.__item: Item = NO_ITEM
        self.__itemActive: bool = False
        self.__itemDuration: int = ITEM_DURATION
        self.__position: Position = None
        self.__boost: int = MAX_BOOST
        self.__direction: int = UP
        self.__creatingGap: bool = True
        self.__gapDuration: int = 0

    def __movePlayer(self) -> bool:
        validMove = True
        # TODO C++ Source was switch/case
        # TODO Accessing class variables:
        # self.width works, but type(self).width is preferred
        if self.__direction == RIGHT:
            self.__position.x += 1
            if self.__position.x >= type(self).width:
                self.__position.x = 0
                validMove = False
        elif self.__direction == UP:
            self.__position.y -= 1
            if self.__position.y >= type(self).height:
                self.__position.y = type(self).height - 1
                validMove = False
        elif self.__direction == LEFT:
            self.__position.x -= 1
            if self.__position.x >= type(self).width:
                self.__position.x = type(self).width - 1
                validMove = False
        else:
            self.__position.y += 1
            if self.__position.y >= type(self).height:
                self.__position.y = 0
                validMove = False
        
        return validMove or (self.isItemActive() and self.getItem() == ITEM_WALL)

    @classmethod
    def setBounds(cls, width: int, height: int):
        cls.width = width
        cls.height = height
        pass

    def setName(self, name: int):
        self.__name = name
        pass

    def getName(self) -> int:
        return self.__name

    def setPosition(self, x: int, y: int):
        self.__position.x = x
        self.__position.y = y
        pass

    def getPosition(self) -> Position:
        return self.__position

    def setDirection(self, direction: int):
        if (self.__direction == UP or self.__direction == DOWN) ^ (direction == UP or direction == DOWN):
            self.__direction = direction
        pass

    def getDirection(self) -> int:
        return self.__direction

    def setItem(self, item: Item):
        if self.__item == NO_ITEM or item == NO_ITEM:
            self.__item == item
            self.__itemDuration = ITEM_DURATION
        pass

    def getItem(self) -> Item:
        return self.__item
    
    def getSpeed(self) -> int:
        return self.__speed

    def activateBoost(self):
        if self.__boost > 0 and not self.isItemActive():
            self.__speed = FAST
        pass

    def deactivateBoost(self):
        if self.getSpeed() == FAST:
            self.__speed = REGULAR
        pass

    def resetBoost(self):
        self.__boost = MAX_BOOST
        pass

    def getBoost(self) -> int:
        return self.__boost

    def isItemActive(self) -> bool:
        return self.__itemActive

    def activateItem(self):
        if not self.isItemActive() and self.__item != NO_ITEM:
            self.deactivateBoost()
            self.__itemActive = True
            if self.getItem() == ITEM_SLOW:
                self.__speed = SLOW
            elif self.getItem() == ITEM_CLEAR:
                self.__itemDuration = 1
        pass

    def getItemDuration(self) -> int:
        return self.__itemDuration

    def isCreatingGap(self) -> bool:
        return self.__creatingGap

    def isFasterThan(self, other: CurveFeverPlayer.Player) -> bool:
        faster: bool = (self.__speed == FAST and other.__speed != FAST) or (self.__speed == REGULAR and other.__speed == SLOW)
        # TODO C++ definition has no return
        return faster

    def reset(self):
        self.setPosition(0, 0)
        self.resetBoost()
        self.setItem(NO_ITEM)
        self.__direction = UP
        self.__speed = REGULAR
        pass

    def update(self) -> bool:
        if self.getSpeed() == FAST:
            self.__boost -= 1
            if self.getBoost() == 0:
                self.deactivateBoost()
        
        if self.isItemActive():
            self.__itemDuration -= 1
            if self.getItemDuration() == 0:
                self.__itemActive = False
                self.__item = NO_ITEM
                self.__speed = REGULAR
        
        if self.__gapDuration == 0:
            if self.__creatingGap:
                self.__gapDuration = random.randrange(MIN_TAIL_DURATION, MAX_TAIL_DURATION + 1)
            else:
                self.__gapDuration = random.randrange(MIN_GAP_DURATION, MAX_GAP_DURATION + 1)
            self.__creatingGap = not self.__creatingGap
        else:
            self.__gapDuration -= 1
        
        return self.__movePlayer()
