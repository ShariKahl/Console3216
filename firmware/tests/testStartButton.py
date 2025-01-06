import time
from StartButton import StartButton

def test_start_button():
    StartButton.init()

    try:
        print("Press the start button to test...")
        for _ in range(20):  # Überprüfe den Button 20 Mal
            status = StartButton.getStatus()
            print(f"Button status: {status}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Test interrupted.")
    finally:
        StartButton.cleanup()

test_start_button()
