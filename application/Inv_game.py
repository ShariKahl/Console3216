import random
import Game
import Inv_pilot
import Inv_ufo
import Inv_projectile
import Inv_alien
import Inv_squad
import Joystick
import NumericDisplay
import Display

PADLE_SOUND_EFFECT_LEFT = 35
PADLE_SOUND_EFFECT_RIGHT = 36

PILOT_DEFAULT_X_POSITION = 16
PILOT_DEFAULT_Y_POSITION = 15

POINTS_UFO = 100
UFO_APPEARANCE_PROBABILITY = 50


class Invaders(Game.Game):
    def __init__(self, leftJoystick: Joystick.Joystick, rightJoystick: Joystick.Joystick):
        super().__init__(leftJoystick, rightJoystick, "INV")

        self._pilot: Inv_pilot.Pilot = Inv_pilot.Pilot()
        self._pilotProjectile: Inv_projectile.Projectile = Inv_projectile.Projectile()
        self._invadersProjectile: Inv_projectile.Projectile = Inv_projectile.Projectile()
        self._ufo: Inv_ufo.Ufo = Inv_ufo.Ufo()
        self._squad: Inv_squad.Squad = Inv_squad.Squad()

        self._player1Points: int = 0
        self._movePrescaler: int = 0
        self._active: bool = False

        # Initialisierung des Piloten mit dem linken Joystick
        self._pilot.init(leftJoystick)
        self._restart()

        # Richtung für Projektile setzen
        self._pilotProjectile.setDirection(False)
        self._invadersProjectile.setDirection(True)

    def play(self):
        action: int = self._pilot.checkActions()

        if not self._pilotProjectile.isActive():
            if action in [Inv_pilot.PILOT_TRIGGER_UP, Inv_pilot.PILOT_TRIGGER_BODY]:
                self._pilotProjectile.activate()
                self._pilotProjectile.setPosition(self._pilot.getXPos(), self._pilot.getYPos())

        self._ufo.move()
        self._pilotProjectile.move()

        # Kollision mit UFO prüfen
        if self._pilotProjectile.getYPos() == 0 and self._pilotProjectile.isActive():
            if self._ufo.checkCollision(self._pilotProjectile.getXPos()):
                self._ufo.deActivate()
                self._ufo.explode()
                self._player1Points += POINTS_UFO

        # Neues UFO aktivieren
        if not self._ufo.isActive() and random.randrange(UFO_APPEARANCE_PROBABILITY) == 5:
            self._ufo.setPosition(0, 0)
            self._ufo.activate()

        # Kollision mit Aliens prüfen
        if self._pilotProjectile.isActive():
            points = self._squad.checkCollision(self._pilotProjectile.getXPos(), self._pilotProjectile.getYPos())
            if points != 0:
                self._player1Points += points
                self._pilotProjectile.deActivate()

        self._squad.move()
        NumericDisplay.NumericDisplay.displayValue(NumericDisplay.DISPLAY_LEFT, self._player1Points)

    def draw(self):
        textColor: int = Display.Display.getColorFrom333(0, 2, 5)
        Display.Display.clearDisplay()
        Display.Display.drawText(self._name, 4, 4, textColor, 1)

        self._drawField()

        NumericDisplay.NumericDisplay.displayTime(NumericDisplay.DISPLAY_MIDDLE, self._time / 1000)

        self._pilot.draw()
        self._ufo.draw()
        self._pilotProjectile.draw()
        self._invadersProjectile.draw()
        self._squad.draw()

        Display.Display.refresh()

    def prepareDemo(self):
        self._player1Type = Game.PLAYER_TYPE_AI_0
        self._player2Type = Game.PLAYER_TYPE_AI_0

    def playDemo(self):
        self.play()
        self.draw()

    def playGame(self):
        self.play()
        self.draw()

    def process(self):
        super().process()

    def _movePlayer(self):
        pass  # Bewegung der Spielerlogik, falls benötigt

    def _drawField(self):
        pass  # Spielfeldzeichnung, falls benötigt

    def _checkBoundarys(self) -> int:
        pass  # Grenzen überprüfen, falls benötigt

    def _checkCollision(self) -> bool:
        collision: bool = False
        return collision

    def _prepareSquad(self):
        self._squad.prepareSquad()

    def _restart(self):
        self._pilot.setPosition(PILOT_DEFAULT_X_POSITION, PILOT_DEFAULT_Y_POSITION)
        self._pilotProjectile.deActivate()
        self._invadersProjectile.deActivate()

        self._squad.prepareSquad()

        self._player1Points = 0
        self._timeStart()
