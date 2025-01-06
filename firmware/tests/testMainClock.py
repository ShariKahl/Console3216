from MainClock import mainClock
import time

# Timer starten
mainClock.startTimer()

try:
    for _ in range(50):  # Überprüfe 50 Ticks
        if mainClock.isTick():
            print(f"Tick! Systemzeit: {mainClock.getSystemTime()} ms")
        time.sleep(0.02)  # Simulation der Verarbeitung zwischen Ticks
finally:
    mainClock.stopTimer()  # Timer sicher beenden
