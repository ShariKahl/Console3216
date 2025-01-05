
import RPi.GPIO as GPIO

from Microcontroller import *

JOYSTICK_STATUS_NOT_PRESSED = 0
JOYSTICK_STATUS_PRESSED = 1
JOYSTICK_STATUS_HOLD = 2

JOYSTICK_SWITCH_LEFT = 0
JOYSTICK_SWITCH_UP = (JOYSTICK_SWITCH_LEFT + 1 )
JOYSTICK_SWITCH_RIGHT = (JOYSTICK_SWITCH_UP	 + 1 )
JOYSTICK_SWITCH_DOWN = (JOYSTICK_SWITCH_RIGHT + 1 ) 
JOYSTICK_SWITCH_BUTTON_TOP = (JOYSTICK_SWITCH_DOWN + 1 )
JOYSTICK_SWITCH_BUTTON_BODY = (JOYSTICK_SWITCH_BUTTON_TOP + 1 )

JOYSTICK_SWITCHES_COUNT = (JOYSTICK_SWITCH_BUTTON_BODY + 1)


class JoystickPins_t:
    def __init__(self) -> None:
        self.left: int = 0
        self.up: int = 0
        self.right: int = 0
        self.down: int = 0
        self.buttonTop: int = 0
        self.buttonBody: int = 0


class JoystickEdge_t:
    def __init__(self) -> None:
        # TODO In C++ Quellcode auf 2 Bits begrenzt
        # typedef struct {
        # 	uint16_t left:2;
        # 	uint16_t up:2;
        # 	uint16_t right:2;
        # 	uint16_t down:2;
        # 	uint16_t buttonTop:2;
        # 	uint16_t buttonBody:2;
        # } JoystickEdge_t;
        self.left: int = 0
        self.up: int = 0
        self.right: int = 0
        self.down: int = 0
        self.buttonTop: int = 0
        self.buttonBody: int = 0


class Joystick:
    def __init__(self) -> None:
        self.__pins: JoystickPins_t = JoystickPins_t()
        self.__edges: JoystickEdge_t = JoystickPins_t()

        self.__value: int = 0
    
    # TODO Parameter pins ein Pointer
    # C++:
    # void init(JoystickPins_t * pins);
    def init(self, pins: JoystickPins_t):
        self.__pins = pins

        # BCM Pinmodus verwenden
        GPIO.setmode(GPIO.BCM)

        # TODO C++ Quellcode:
        # pinMode(this->pins.left, INPUT_PULLUP);
        # pinMode(this->pins.up, INPUT_PULLUP);
        # pinMode(this->pins.right, INPUT_PULLUP);
        # pinMode(this->pins.down, INPUT_PULLUP);
        # pinMode(this->pins.buttonTop, INPUT_PULLUP);
        # pinMode(this->pins.buttonBody, INPUT_PULLUP);

        GPIO.setup(self.__pins.left, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.__pins.up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.__pins.right, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.__pins.down, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.__pins.buttonTop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.__pins.buttonBody, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        pass

    def isLeft(self) -> bool:
        if GPIO.input(self.__pins.left) == GPIO.LOW:
            return True
        
        return False
    def isUp(self) -> bool:
        if GPIO.input(self.__pins.up) == GPIO.LOW:
            return True
        
        return False
    def isRight(self) -> bool:
        if GPIO.input(self.__pins.right) == GPIO.LOW:
            return True
        
        return False
    def isDown(self) -> bool:
        if GPIO.input(self.__pins.down) == GPIO.LOW:
            return True
        
        return False
    def isButtonTop(self) -> bool:
        if GPIO.input(self.__pins.buttonTop) == GPIO.LOW:
            return True
        
        return False
    def isButtonBody(self) -> bool:
        if GPIO.input(self.__pins.buttonBody) == GPIO.LOW:
            return True
        
        return False

    def process(self):
        # C++ Quellcode:
        # uint8_t actualSwitch;
        # for (actualSwitch = 0; actualSwitch < JOYSTICK_SWITCHES_COUNT; actualSwitch++) 
        # {
        # 	this->checkEdge(actualSwitch);
        # }
        for actualSwitch in range(0, JOYSTICK_SWITCHES_COUNT):
            self.checkEdge(actualSwitch)
        pass

    def getSwitchStatus(self, switchId: int) -> bool:
        if switchId == JOYSTICK_SWITCH_LEFT:
            return self.isLeft()
        elif switchId == JOYSTICK_SWITCH_RIGHT:
            return self.isRight()
        elif switchId == JOYSTICK_SWITCH_UP:
            return self.isUp()
        elif switchId == JOYSTICK_SWITCH_DOWN:
            return self.isDown()
        elif switchId == JOYSTICK_SWITCH_BUTTON_TOP:
            return self.isButtonTop()
        elif switchId == JOYSTICK_SWITCH_BUTTON_BODY:
            return self.isButtonBody()
        else:
            return False
    def checkEdge(self, edge: int):
        status: int = self.getControlStatus(edge)

        if self.getSwitchStatus(edge):
            if status == JOYSTICK_STATUS_NOT_PRESSED:
                self.setControlStatus(edge, JOYSTICK_STATUS_PRESSED)
            elif status == JOYSTICK_STATUS_PRESSED:
                self.setControlStatus(edge, JOYSTICK_STATUS_HOLD)
        else:
            self.setControlStatus(edge, JOYSTICK_STATUS_NOT_PRESSED)
        pass

    def getControlStatus(self, switchId: int) -> int:
        if switchId == JOYSTICK_SWITCH_LEFT:
            return self.__edges.left
        elif switchId == JOYSTICK_SWITCH_RIGHT:
            return self.__edges.right
        elif switchId == JOYSTICK_SWITCH_UP:
            return self.__edges.up
        elif switchId == JOYSTICK_SWITCH_DOWN:
            return self.__edges.down
        elif switchId == JOYSTICK_SWITCH_BUTTON_TOP:
            return self.__edges.buttonTop
        elif switchId == JOYSTICK_SWITCH_BUTTON_BODY:
            return self.__edges.buttonBody
        else:
            return JOYSTICK_STATUS_NOT_PRESSED
    def setControlStatus(self, switchId: int, status: int):
        if switchId == JOYSTICK_SWITCH_LEFT:
            self.__edges.left = status
        elif switchId == JOYSTICK_SWITCH_RIGHT:
            self.__edges.right = status
        elif switchId == JOYSTICK_SWITCH_UP:
            self.__edges.up = status
        elif switchId == JOYSTICK_SWITCH_DOWN:
            self.__edges.down = status
        elif switchId == JOYSTICK_SWITCH_BUTTON_TOP:
            self.__edges.buttonTop = status
        elif switchId == JOYSTICK_SWITCH_BUTTON_BODY:
            self.__edges.buttonBody = status
        pass
