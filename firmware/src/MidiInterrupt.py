from MidiPlayer import *


songPlayer: Player = Player()
soundEffectPlayer: Player = Player()
isPlayingSound: bool = False

def setupInterrupt():
    noInterrupts()
    TCCR4A = 0
    TCCR4B = 0
    TCNT4 = 34286
    TCCR4B |= (1 << CS12)
    TCCR4B |= (1 << CS10)  # Prescaler 256
    TIMSK4 |= (1 << TOIE4) #Timeoverflow  Interrupt aktivieren
    interrupts()

    # TODO Comment aus C++ Source
    # for testing purposes
    # pinMode(LED_BUILTIN, OUTPUT);
    # TODO pyserial
    # Serial.begin(9600);
    pass

def calcTimer(mspq: int, ppq: int) -> int:
    # TODO Comment aus C++ Source
    # mspq wenn kein wert angegeben, dann 120BPM -> 500 mspq
    # ppq pro lied/abschnitt variable
    
    tick: float = (mspq / ppq) / 1000.0
    hzfrq: float = 1.0 / tick
    retCount: int = 65536 - 16000000 / 256 / hzfrq # 16Mhz Clock mit 256 Prescaler
    
    # TODO Debug Code aus C++ Source
    # #ifdef MIDI_DEBUG
    #     Serial.print(retCount);
    #     Serial.print("\n");
    # #endif
    
    return retCount

def updateInterrupt(mspq: int, ppq: int):
    mask: int = 1 < TOIE4
    mask = ~mask
    TIMSK4 &= mask
    TCNT4 = calcTimer(mspq, ppq)
    TIMSK4 |= (1 << TOIE4)
    pass

# TODO
# ISR(TIMER4_OVF_vect)
# {
#     if(isPlayingSound) {
#         if(soundEffectPlayer.advanceTick()) {
#             isPlayingSound = false;
#         }
#     } else {
#         songPlayer.advanceTick();
#     }
#     //Player::process();//process muss updateInterrupt aufrufen, bei tempo change, sonst immer bei neuer Note diese abspielen

#     //testing purposes
# #ifdef MIDI_DEBUG
#     Serial.print("test\n");
# #endif
# }

def interruptLoop():
    # TODO Debug Code aus C++ Source
    # #ifdef MIDI_DEBUG
    #     Serial.print("uff\n");

    #     updateInterrupt(500, 1);
    #     delay(3000);
    #     updateInterrupt(1000, 1);
    #     delay(3000);
    # #endif
    pass

# TODO Comment aus C++ Source
# Diese drei Methoden gehören eigentlich in eine eigene Klasse und sind das was wir nach außen geben
def playSound(data: int):
    songPlayer.setSong(data)
    pass

def playSong(data: int):
    soundEffectPlayer.setSong(data)
    isPlayingSound = True
    pass
