from Sine import Sine

def test_sine():
    print("Testing Sine and Cosine calculations...")
    angles = [-128, -64, -32, 0, 32, 64, 96, 128]
    for angle in angles:
        sine_value = Sine.getSineValue(angle)
        cosine_value = Sine.getCosineValue(angle)
        print(f"Angle: {angle}, Sine: {sine_value}, Cosine: {cosine_value}")

test_sine()
