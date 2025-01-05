# Application.ino

# #include "Arduino.h"

# #include "Microcontroller.h"
import Microcontroller
# #include "display.h"
import Display
# #include "CoinDetection.h"
import CoinDetection
# #include "Joystick.h"
import Joystick

# #include <Wire.h>
# #include <console.h>
# #include <Adafruit_GFX.h>
# #include <gfxfont.h>

import Game

# TODO
# #include <console.h>
import Console

# #include "inc/pong_game.h"
import Pong_game

# #include "inc/inv_game.h"
import Inv_game

# #include "inc/curve_game.h"
import Curve_Game

# #include "inc/sw_game.h"
import SW_Game

# #include "inc/TetrisGame.h"
import TetrisGame

# #include "Midi.h"
# #include "MidiInterrupt.h"

totalCoinValue: int = 0
currentCoinValue: int = 0

# TODO
console: Console.Console = None

# TODO C++: Display* display;
display: Display.Display = None

# TODO Arduino specific code, now handled by main()
def setup():
    pass

# TODO Arduino specific code, now handled by main()
def loop():
    pass

# TODO No definition in C++ source
# TODO Coindetection from firmware, not same folder
def ca_coinDetected(coinType: CoinDetection.coin):
    pass

# TODO No definition in C++ source
def checkCoinValues():
    pass

# TODO No definition in C++ source
def checkScoreAndPlaySound():
    pass

def main():
    # TODO BEGIN setup()

    # Serial.begin(115200)
    # Midi.init()
    # MIDI.setupInterrupt()
    console.init()

    # TODO Pong
    game: Game.Game = Pong_game.Pong(console.getJoystick(0), console.getJoystick(1))
    console.addGame(game)

    # TODO Invaders
    game = Inv_game.Invaders(console.getJoystick(0), console.getJoystick(1))
    console.addGame(game)

    # TODO Curve
    game = Curve_Game.Curve(console.getJoystick(0), console.getJoystick(1))
    console.addGame(game)

    # TODO Space_Wars
    game = SW_Game.Space_Wars(console.getJoystick(0), console.getJoystick(1))
    console.addGame(game)

    # TODO Tetris
    game = TetrisGame.TetrisGame(console.getJoystick(0), console.getJoystick(1))
    console.addGame(game)
    # TODO END setup()

    # TODO BEGIN loop()
    while True:
        console.process()
        # MIDI.interruptLoop()
    # TODO END loop()

if __name__ == "__main__":
    main()
