from MidiPlayer import Player
import threading
import time

# Globale Variablen
songPlayer: Player = Player()
soundEffectPlayer: Player = Player()
isPlayingSound: bool = False

# Timer-Konfiguration
TICK_INTERVAL = 0.02  # Standardwert in Sekunden, z. B. 20 ms

# Lock für Thread-Sicherheit
lock = threading.Lock()

def setupInterrupt():
    """
    Initialisiert die Timer-Simulation für den MIDI-Interrupt.
    """
    print("Interrupt system initialized.")

def calcTimer(mspq: int, ppq: int) -> float:
    """
    Berechnet das Timer-Intervall basierend auf mspq (Millisekunden pro Viertelnote)
    und ppq (Ticks pro Viertelnote).
    :param mspq: Millisekunden pro Viertelnote
    :param ppq: Ticks pro Viertelnote
    :return: Timer-Intervall in Sekunden
    """
    tick_duration = (mspq / ppq) / 1000.0  # Dauer eines Ticks in Sekunden
    print(f"Calculated tick duration: {tick_duration:.6f} seconds")
    return tick_duration

def updateInterrupt(mspq: int, ppq: int):
    """
    Aktualisiert den Timer basierend auf neuen mspq und ppq-Werten.
    :param mspq: Millisekunden pro Viertelnote
    :param ppq: Ticks pro Viertelnote
    """
    global TICK_INTERVAL
    TICK_INTERVAL = calcTimer(mspq, ppq)
    print(f"Updated interrupt interval to {TICK_INTERVAL:.6f} seconds.")

def interruptLoop():
    """
    Simuliert die Haupt-Interrupt-Schleife.
    """
    global isPlayingSound

    while True:
        time.sleep(TICK_INTERVAL)  # Warte auf den nächsten "Interrupt"

        with lock:  # Thread-sichere Verarbeitung
            if isPlayingSound:
                if soundEffectPlayer.advanceTick():
                    isPlayingSound = False
            else:
                songPlayer.advanceTick()

            # Debugging-Ausgabe
            print("Interrupt executed")

def playSound(data: int):
    """
    Startet das Abspielen eines Sounds.
    :param data: Sound-Daten
    """
    global isPlayingSound
    with lock:
        soundEffectPlayer.setSong(data)
        isPlayingSound = True
        print(f"Playing sound with data: {data}")

def playSong(data: int):
    """
    Startet das Abspielen eines Songs.
    :param data: Song-Daten
    """
    with lock:
        songPlayer.setSong(data)
        print(f"Playing song with data: {data}")
