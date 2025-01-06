# Konfiguration der maximalen Anzahl von Projektilen
MAXPROJECTILE: int = 5

# Spielfeldgrenzen
FIELD_LEFT_BORDER: int = 0
FIELD_RIGHT_BORDER: int = 31

# Tick-Konfigurationen (Bewegung und Schießen)
TICK_MOVE_PROJECTILES_DEFAULT: int = 3  # Anzahl der Ticks zwischen Projektilbewegungen
TICK_SHOT_PROJECTILE_DEFAULT: int = 3  # Anzahl der Ticks zwischen Schüssen

# Spielzustände
STATE_PLAY: int = 0          # Spiel läuft
STATE_DEMO: int = 1          # Demo-Modus
STATE_SHOW_WINNER: int = 2   # Gewinneranzeige

# Schiffeinstellungen
SHIP_LEFT: int = 0
SHIP_RIGHT: int = 1
SHIP_TICK_MOVE: int = 5      # Ticks für Schiffsbewegung
SHIP_TICK_SHOT: int = 15     # Ticks für Schussbereitschaft

# Schiffsausrichtung
SHIP_ORIENTATION_LEFT: int = 0
SHIP_ORIENTATION_RIGHT: int = 1

# Spielfeldgrenzen für das linke Schiff
SHIP_LEFT_LEFT_BORDER: int = 0
SHIP_LEFT_RIGHT_BORDER: int = 14
SHIP_LEFT_UPPER_BORDER: int = 0
SHIP_LEFT_BOTTOM_BORDER: int = 15

# Spielfeldgrenzen für das rechte Schiff
SHIP_RIGHT_LEFT_BORDER: int = 17
SHIP_RIGHT_RIGHT_BORDER: int = 31
SHIP_RIGHT_UPPER_BORDER: int = 0
SHIP_RIGHT_BOTTOM_BORDER: int = 15

# Allgemeine Spielfeldgrenzen
BORDER_BOTTOM: int = 15
BORDER_TOP: int = 0
