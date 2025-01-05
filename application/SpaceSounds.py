import Sound

SHIP_SHOT_SOUND = 55
SHIP_MOVE_SOUND = 56
SHIP_GOT_HIT_SOUND = 57
# TODO Fixed typo in C++ source: SHOT_COLISION_SOUND
SHOT_COLLISION_SOUND = 4
# Comment from source:
# 35,36

class SpaceSounds:
    # TODO C++ Source body empty
    def initialize(self):
        pass

    def playSoundShipShot(self):
        Sound.Sound.playSoundDura(SHIP_SHOT_SOUND, 9, 100)
        pass

    def playSoundShipMove(self):
        Sound.Sound.playSoundDura(SHIP_MOVE_SOUND, 9, 100)
        pass

    def playSoundShipHasBeenHit(self):
        Sound.Sound.playSoundDura(SHIP_GOT_HIT_SOUND, 9, 100)
        pass

    def playSoundProjectileCollision(self):
        # TODO C++ Source code commented out:
        # Sound::playSound(36, 9,100);
        # Sound.Sound.playSound(36, 9, 100)
        pass
