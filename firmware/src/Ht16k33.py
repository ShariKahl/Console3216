from time import sleep

HT16K33_DISPLAY_SIZE = 16
HT16k33_CMD_BRIGHTNESS = 0xE0

class Ht16k33:
    def __init__(self) -> None:
        self._i2CAddres: int = 0
        self._dataBuffer: int = [0 for _ in range(HT16K33_DISPLAY_SIZE)]
    
    def init(self, i2CAddress: int):
        self._i2CAddres = i2CAddress
        # TODO C++ Quellcode:
        # delay(100);
        sleep(0.1)

        # TODO C++ Quellcode:
        # Wire.begin();
        # Serial.println("init");
            
        # Wire.beginTransmission(this->i2CAddres);
        # Wire.write(0x21);  // turn on oscillator
        # Wire.endTransmission();

        # Wire.beginTransmission(this->i2CAddres);
        # Wire.write(0x81);  // turn on display
        # Wire.endTransmission();

        # Wire.beginTransmission(this->i2CAddres);
        # Wire.write(0xEF);  // turn on display
        # Wire.endTransmission();

        # Wire.beginTransmission(this->i2CAddres);
        # Wire.write(0xA0);  // turn on display
        # Wire.endTransmission();
        # Aus Wire.h, genaue Funktionalität unklar
        
        self.setBrightness(15)
        pass
    def setBrightness(self, brightness: int):
        if (brightness > 15):
            brightness = 15
        
        # TODO C++ Quellcode:
        # Wire.beginTransmission(this->i2CAddres);
        # Wire.write(HT16K33_CMD_BRIGHTNESS | brightness);
        # Wire.endTransmission();
        # Aus Wire.h, genaue Funktionalität unklar
        pass
    def refresh(self):
        index: int

        # TODO C++ Quellcode:
        # Wire.beginTransmission(this->i2CAddres);
        # Wire.write(0x00); // start at address $00

        # TODO Zeilen im C++ Quellcode auskommentiert
        # Index wird somit nicht verwendet, diese Funktion
        # wird deshalb vermutlich nirgendwo benutzt
        # //   for (index=0; index<HT16K33_DISPLAY_SIZE; index++)
        # //      for (index=0; index<1; index++)
        # {
        #   Wire.write(&this->dataBuffer[index],16);
        # }

        # Wire.endTransmission();
        # Aus Wire.h, genaue Funktionalität unklar
        pass
