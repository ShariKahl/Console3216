import Sound

SHIP_SHOT_SOUND = 55
SHIP_MOVE_SOUND = 56
SHIP_GOT_HIT_SOUND = 57
SHOT_COLLISION_SOUND = 36  # Fixed typo and updated the sound ID based on C++ comments

class SpaceSounds:
    @staticmethod
    def initialize():
        """Initialize sound settings if needed."""
        pass  # Placeholder for any initialization logic

    @staticmethod
    def playSoundShipShot():
        """Play the sound when the ship shoots."""
        Sound.Sound.playSoundDura(SHIP_SHOT_SOUND, 9, 100)

    @staticmethod
    def playSoundShipMove():
        """Play the sound when the ship moves."""
        Sound.Sound.playSoundDura(SHIP_MOVE_SOUND, 9, 100)

    @staticmethod
    def playSoundShipHasBeenHit():
        """Play the sound when the ship has been hit."""
        Sound.Sound.playSoundDura(SHIP_GOT_HIT_SOUND, 9, 100)

    @staticmethod
    def playSoundProjectileCollision():
        """Play the sound when a projectile collides."""
        Sound.Sound.playSoundDura(SHOT_COLLISION_SOUND, 9, 100)
