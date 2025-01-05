# Console3216: Portierung auf Raspberry Pi 4

## **Projektbeschreibung**
Console3216 ist ein Arduino-basiertes Projekt, das eine Sammlung von Spielen auf einer LED-Matrix darstellt. In dieser Version wird das Projekt auf einen Raspberry Pi 4 portiert, der in Kombination mit einem Adafruit RGB Matrix Bonnet und einer 64x64 RGB-LED-Matrix die Spiellogik und Darstellung übernimmt.

## **Verzeichnisstruktur**

### **application**
Enthält die Spiellogik und Visualisierungsdateien. Einige wichtige Dateien:
- **Main.py**: Hauptprogramm zur Steuerung der Spiele.
- **Pong_game.py, TetrisGame.py, Inv_game.py**: Logik für Pong, Tetris und Space Invaders.
- **SW_Constants.py**: Enthält Konfigurationskonstanten.
- **CurveFeverLogic.py**: Implementiert die Logik für Curve Fever.

### **firmware**
Enthält Hardware-spezifische Komponenten und Treiber.
- **Display.py**: Verwaltet die Darstellung auf der LED-Matrix.
- **Joystick.py**: Implementiert die Steuerung über GPIO.
- **Midi.py, MidiPlayer.py**: MIDI-Unterstützung.
- **MainClock.py**: Zeiterfassungslogik.
- **Sprite.py**: Unterstützt die Erstellung und Darstellung von Sprites.

## **Hardware-Anforderungen**

### **Raspberry Pi 4**
- Betriebssystem: Raspberry Pi OS (32-bit oder 64-bit).
- RGB Matrix Bonnet (Adafruit) zur Steuerung der LED-Matrix.

### **LED-Matrix**
- 64x64 RGB-LED-Matrix kompatibel mit dem Adafruit Bonnet.

### **Zusätzliche Komponenten**
- Joystick und Buttons (über GPIO angeschlossen).
- Optionale MIDI-Hardware.

## **Software-Anforderungen**
### **Abhängigkeiten**
Installiere die folgenden Python-Bibliotheken:
```bash
pip install rgbmatrix
pip install RPi.GPIO
pip install mido
```

### **Adafruit RGB Matrix Bibliothek**
Installiere die Software-Bibliotheken für das Adafruit RGB Matrix Bonnet:
```bash
sudo apt-get update
sudo apt-get install -y build-essential python3-dev libffi-dev
cd ~
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cd rpi-rgb-led-matrix
make build-python PYTHON=$(which python3)
```

## **Installation**
1. Klone das Repository:
   ```bash
   git clone <repository-url>
   cd Console3216
   ```

2. Richte die Schriftarten ein:
   - Erstelle einen Ordner `fonts` im Projektverzeichnis.
   - Füge BDF-Schriftarten (z. B. `6x9.bdf`) in diesen Ordner ein.

3. Schließe die Hardware korrekt an (siehe Schaltplan für das Adafruit Bonnet).

4. Starte das Projekt:
   ```bash
   python3 application/Main.py
   ```

## **Projektarchitektur**

### **Display-Steuerung**
Die Datei `Display.py` verwendet die `rgbmatrix`-Bibliothek zur Steuerung der LED-Matrix. Diese bietet Funktionen für:
- Pixel zeichnen
- Rechtecke und Kreise füllen
- Text anzeigen

### **Spielelogik**
- Jedes Spiel hat eine eigene Datei in `application`. Die Spiele kommunizieren mit der LED-Matrix über die `Display`-Klasse.

### **Joystick-Steuerung**
- Die Datei `Joystick.py` liest GPIO-Signale und ermöglicht die Steuerung der Spiele.

## **Beispielcode**

### **Pixel und Formen zeichnen**
```python
from Display import Display

Display.init()
red = Display.get_color(255, 0, 0)
Display.draw_pixel(10, 10, red)
Display.fill_rect(15, 15, 10, 10, red)
Display.refresh()
```

### **Text anzeigen**
```python
from Display import Display

Display.init()
blue = Display.get_color(0, 0, 255)
Display.draw_text("Hello, World!", 5, 20, blue, font_index=0)
Display.refresh()
```

## **To-Do-Liste**
1. Testen der Joystick-Steuerung auf dem Raspberry Pi.
2. Optimierung der Spielelogik für die LED-Matrix.
3. Integration und Test von MIDI-Funktionen.

## **Autoren**
- **Dein Name**
- **Weitere Mitwirkende**

## **Lizenz**
Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen findest du in der Datei `LICENSE`.

