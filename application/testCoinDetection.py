import time
from CoinDetection import CoinDetection


def test_coin_detection():
    coin_detector = CoinDetection(coin_pin=18, led_pin=23)

    try:
        print("Test läuft... Drücken Sie eine Taste, um zu beenden.")
        while True:
            result = coin_detector.cd_coinDetection()
            if result != CoinDetection.Coin.UNKNOWN:
                print(f"Erkannte Münze: {result}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Test beendet.")
    finally:
        coin_detector.cleanup()

test_coin_detection()
