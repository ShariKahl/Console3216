import threading
import time
from MidiInterrupt import setupInterrupt, updateInterrupt, interruptLoop, playSound, playSong

# Interrupt-Setup
setupInterrupt()
updateInterrupt(500, 96)  # Beispiel: 500 ms pro Viertelnote, 96 Ticks pro Viertelnote

# Interrupt-Schleife starten
interrupt_thread = threading.Thread(target=interruptLoop, daemon=True)
interrupt_thread.start()

# Test: Sound abspielen
playSound(42)

# Test: Song abspielen
playSong(84)

# Simulation für 10 Sekunden
time.sleep(10)
