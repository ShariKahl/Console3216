# Application.ino

# Import von Modulen
import Microcontroller
import Display
import CoinDetection
import Joystick
import Console
import Pong_game
import Inv_game
import Curve_Game
import SW_Game
import TetrisGame

# Globale Variablen
totalCoinValue: int = 0
currentCoinValue: int = 0

# Instanzen der globalen Objekte
console: Console.Console = None
display: Display.Display = None

def ca_coinDetected(coinType: CoinDetection.coin):
    """
    Wird aufgerufen, wenn ein Münzeinwurf erkannt wurde.
    """
    global totalCoinValue, currentCoinValue
    coinValueMapping = {
        CoinDetection.coin.cent5: 5,
        CoinDetection.coin.cent10: 10,
        CoinDetection.coin.cent20: 20
    }
    if coinType in coinValueMapping:
        totalCoinValue += coinValueMapping[coinType]
        currentCoinValue += coinValueMapping[coinType]
        print(f"Münze erkannt: {coinValueMapping[coinType]} Cent. Total: {totalCoinValue} Cent.")

def checkCoinValues():
    """
    Prüft die aktuellen Münzwerte und aktualisiert den Zustand.
    """
    global currentCoinValue
    if currentCoinValue > 0:
        print(f"Spiel verfügbar! Münzwert: {currentCoinValue}")
        # Beispielaktion: Spiel starten, falls genug Münzen vorhanden.
        currentCoinValue -= 1  # Verbrauch einer Münze für ein Spiel
    else:
        print("Bitte Münzen einwerfen.")

def checkScoreAndPlaySound():
    """
    Prüft den aktuellen Punktestand und spielt gegebenenfalls einen Sound ab.
    """
    # Beispiel für eine Soundaktion basierend auf Punktestand
    if totalCoinValue % 10 == 0:  # Beispielbedingung
        print("Special Sound gespielt!")
        # Sound.playSoundEffect(...) (nicht implementiert)

def main():
    """
    Hauptprogramm der Anwendung.
    """
    global console, display

    # Setup-Phase
    print("Initialisierung...")
    Microcontroller.init()
    Display.init()
    CoinDetection.init()
    
    console = Console.Console()
    console.init()

    # Initialisierung der Spiele
    print("Spiele werden geladen...")
    games = [
        Pong_game.Pong(console.getJoystick(0), console.getJoystick(1)),
        Inv_game.Invaders(console.getJoystick(0), console.getJoystick(1)),
        Curve_Game.Curve(console.getJoystick(0), console.getJoystick(1)),
        SW_Game.Space_Wars(console.getJoystick(0), console.getJoystick(1)),
        TetrisGame.TetrisGame(console.getJoystick(0), console.getJoystick(1))
    ]

    for game in games:
        console.addGame(game)

    # Haupt-Loop
    print("Hauptschleife gestartet...")
    while True:
        console.process()
        checkCoinValues()
        checkScoreAndPlaySound()
        # Hier könnten weitere periodische Aktionen eingefügt werden.

if __name__ == "__main__":
    main()
