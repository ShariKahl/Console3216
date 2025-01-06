import Sprite


def test_sprite():
    sprite = Sprite(10, 10, 4, 4)
    
    # Test: Aktivierung
    sprite.activate()
    print("Sprite activated:", sprite.isActive())
    
    # Test: Position setzen und bewegen
    sprite.setPosition(20, 20)
    print(f"Sprite position: ({sprite.getXPos()}, {sprite.getYPos()})")
    sprite.move(-5, -5)
    print(f"Sprite moved to: ({sprite.getXPos()}, {sprite.getYPos()})")
    
    # Test: Zeichnen
    sprite.draw()
    
    # Test: Spiegelung
    sprite.mirrorY()

test_sprite()
