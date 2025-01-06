import serial

MIDI_COMMAND_NOTE_OFF = 0x80
MIDI_COMMAND_NOTE_ON = 0x90
MIDI_COMMAND_CONTROL_CHANGE = 0xB0
MIDI_COMMAND_PROGRAM_CHANGE = 0xC0


class Midi:
    __serial_connection = None  # Serielle Verbindung

    @classmethod
    def init(cls, port: str = "/dev/serial0", baudrate: int = 31250):
        """
        Initialisiert die MIDI-Kommunikation.
        :param port: Der serielle Port (standardmäßig "/dev/serial0" für UART).
        :param baudrate: Die Baudrate für MIDI (standardmäßig 31250).
        """
        try:
            cls.__serial_connection = serial.Serial(
                port=port,
                baudrate=baudrate,
                bytesize=serial.EIGHTBITS,
                stopbits=serial.STOPBITS_ONE,
                parity=serial.PARITY_NONE
            )
            print(f"MIDI serial connection initialized on {port} at {baudrate} baud.")
        except serial.SerialException as e:
            print(f"Failed to initialize MIDI serial connection: {e}")

    @classmethod
    def noteOn(cls, channel: int, note: int, velocity: int):
        """
        Sendet einen NOTE ON MIDI-Befehl.
        :param channel: Der MIDI-Kanal (0-15).
        :param note: Die Note (0-127).
        :param velocity: Die Anschlagsstärke (0-127).
        """
        cls.__send_message(MIDI_COMMAND_NOTE_ON | (channel & 0x0F), note & 0x7F, velocity & 0x7F)

    @classmethod
    def noteOff(cls, channel: int, note: int):
        """
        Sendet einen NOTE OFF MIDI-Befehl.
        :param channel: Der MIDI-Kanal (0-15).
        :param note: Die Note (0-127).
        """
        cls.__send_message(MIDI_COMMAND_NOTE_OFF | (channel & 0x0F), note & 0x7F, 0)

    @classmethod
    def controlChange(cls, channel: int, control: int, value: int):
        """
        Sendet einen CONTROL CHANGE MIDI-Befehl.
        :param channel: Der MIDI-Kanal (0-15).
        :param control: Der Steuerungsparameter (0-127).
        :param value: Der Wert (0-127).
        """
        cls.__send_message(MIDI_COMMAND_CONTROL_CHANGE | (channel & 0x0F), control & 0x7F, value & 0x7F)

    @classmethod
    def programChange(cls, channel: int, preset: int):
        """
        Sendet einen PROGRAM CHANGE MIDI-Befehl.
        :param channel: Der MIDI-Kanal (0-15).
        :param preset: Der Programmwechselwert (0-127).
        """
        cls.__send_message(MIDI_COMMAND_PROGRAM_CHANGE | (channel & 0x0F), preset & 0x7F)

    @classmethod
    def __send_message(cls, command: int, data1: int, data2: int = None):
        """
        Sendet eine MIDI-Nachricht über die serielle Verbindung.
        :param command: Der MIDI-Befehl.
        :param data1: Das erste Datenbyte.
        :param data2: (optional) Das zweite Datenbyte.
        """
        if cls.__serial_connection is None or not cls.__serial_connection.is_open:
            print("Error: Serial connection is not open.")
            return

        message = bytearray([command, data1])
        if data2 is not None:
            message.append(data2)

        try:
            cls.__serial_connection.write(message)
            print(f"Sent MIDI message: {list(message)}")
        except serial.SerialException as e:
            print(f"Failed to send MIDI message: {e}")

    @classmethod
    def close(cls):
        """Schließt die serielle Verbindung."""
        if cls.__serial_connection and cls.__serial_connection.is_open:
            cls.__serial_connection.close()
            print("MIDI serial connection closed.")
