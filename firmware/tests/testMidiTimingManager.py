from MidiTimingManager import TimingManager

def test_timing_manager():
    manager = TimingManager()

    # Setze PPQ und MSPQ
    manager.setPPQ(96)
    manager.setMSPQ(500)

    # Simuliere Ticks
    for _ in range(100):
        manager.advanceTick()
        if manager.isCommandReady():
            print("Command is ready.")
            manager.setDelayUntilNextCommand(10)

        if manager.isBeatEnd():
            print("Beat end reached.")

test_timing_manager()
