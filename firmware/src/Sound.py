from Midi import *

# Kanäle
CHANNEL_1 = 0
CHANNEL_2 = 1
CHANNEL_3 = 2
CHANNEL_DRUM = 9

# Konstanten
SOUNDEFFECTS_LENGTH = 3
CONTROL_CHANNEL_VOLUME = 7
CONTROL_CHANNEL_BALANCE = 10
CONTROL_CHANNEL_VELOCITY = 64


class Sound:
    __steps: int = 1
    __alarmSound = [0] * 3
    __alarmSoundEffect = [0] * SOUNDEFFECTS_LENGTH
    __sound = [0] * 3
    __soundEffects = [0] * SOUNDEFFECTS_LENGTH

    @classmethod
    def __sortSoundEffects(cls, idx: int):
        """
        Sortiert die Soundeffekte im Array nach der zeitlichen Hierarchie und entfernt das angegebene Element.
        :param idx: Index des zu entfernenden Elements
        """
        for i in range(idx, SOUNDEFFECTS_LENGTH - 1):
            cls.__soundEffects[i] = cls.__soundEffects[i + 1]
            cls.__alarmSoundEffect[i] = cls.__alarmSoundEffect[i + 1]

        # Letzte Position freimachen
        cls.__soundEffects[-1] = 0
        cls.__alarmSoundEffect[-1] = 0
        print(f"Sound effect at index {idx} removed and sorted.")

    @classmethod
    def init(cls):
        """
        Initialisiert die MIDI-Schnittstelle und die Sound-Datenstrukturen.
        """
        Midi.init()
        cls.__steps = 1
        cls.__alarmSound = [0] * 3
        cls.__alarmSoundEffect = [0] * SOUNDEFFECTS_LENGTH
        cls.__sound = [0] * 3
        cls.__soundEffects = [0] * SOUNDEFFECTS_LENGTH
        print("Sound system initialized.")

    @classmethod
    def reset(cls):
        """
        Setzt alle Sounds und Soundeffekte zurück.
        """
        cls.stopSounds()
        cls.stopSoundEffects()
        cls.__steps = 1
        print("Sound system reset.")

    @classmethod
    def setPreset(cls, index: int):
        if index > 127:
            print("Invalid preset index.")
            return

        for channel in [CHANNEL_1, CHANNEL_2, CHANNEL_3]:
            Midi.programChange(channel, index)
        print(f"Preset {index} set on all channels.")

    @classmethod
    def setPresetCh(cls, index: int, channel: int):
        if index > 127:
            print("Invalid preset index.")
            return

        Midi.programChange(channel, index)
        print(f"Preset {index} set on channel {channel}.")

    @classmethod
    def setVolume(cls, volume: int):
        for channel in [CHANNEL_1, CHANNEL_2, CHANNEL_3, CHANNEL_DRUM]:
            cls.setVolumeCh(volume, channel)
        print(f"Volume set to {volume} on all channels.")

    @classmethod
    def setVolumeCh(cls, volume: int, channel: int):
        Midi.controlChange(channel, CONTROL_CHANNEL_VOLUME, volume)
        print(f"Volume set to {volume} on channel {channel}.")

    @classmethod
    def playSound(cls, note: int, channel: int):
        Midi.noteOff(channel, cls.__sound[channel])
        Midi.noteOn(channel, note, CONTROL_CHANNEL_VELOCITY)
        cls.__sound[channel] = note
        print(f"Playing note {note} on channel {channel}.")

    @classmethod
    def playSoundDura(cls, note: int, channel: int, duration: int):
        cls.playSound(note, channel)
        cls.__alarmSound[channel] = cls.__steps + duration
        print(f"Playing note {note} on channel {channel} for {duration} steps.")

    @classmethod
    def stopSound(cls, note: int, channel: int):
        Midi.noteOff(channel, note)
        cls.__alarmSound[channel] = 0
        print(f"Stopped note {note} on channel {channel}.")

    @classmethod
    def stopSounds(cls):
        for channel in range(CHANNEL_1, CHANNEL_3 + 1):
            cls.stopSound(cls.__sound[channel], channel)
        print("All sounds stopped.")

    @classmethod
    def playSoundEffect(cls, soundEffect: int):
        cls.playSoundEffectDura(soundEffect, 0)

    @classmethod
    def playSoundEffectDura(cls, soundEffect: int, duration: int):
        if soundEffect in cls.__soundEffects:
            print(f"Sound effect {soundEffect} already playing.")
            return

        Midi.noteOn(CHANNEL_DRUM, soundEffect, CONTROL_CHANNEL_VELOCITY)
        for i in range(SOUNDEFFECTS_LENGTH - 1, 0, -1):
            cls.__soundEffects[i] = cls.__soundEffects[i - 1]
            cls.__alarmSoundEffect[i] = cls.__alarmSoundEffect[i - 1]

        cls.__soundEffects[0] = soundEffect
        cls.__alarmSoundEffect[0] = duration
        print(f"Playing sound effect {soundEffect} for {duration} steps.")

    @classmethod
    def stopSoundEffect(cls, soundEffect: int):
        if soundEffect not in cls.__soundEffects:
            print(f"Sound effect {soundEffect} not found.")
            return

        idx = cls.__soundEffects.index(soundEffect)
        Midi.noteOff(CHANNEL_DRUM, soundEffect)
        cls.__sortSoundEffects(idx)
        print(f"Sound effect {soundEffect} stopped.")

    @classmethod
    def stopSoundEffects(cls):
        for effect in cls.__soundEffects:
            if effect != 0:
                Midi.noteOff(CHANNEL_DRUM, effect)
        cls.__soundEffects = [0] * SOUNDEFFECTS_LENGTH
        cls.__alarmSoundEffect = [0] * SOUNDEFFECTS_LENGTH
        print("All sound effects stopped.")

    @classmethod
    def step(cls):
        for i in range(CHANNEL_1, CHANNEL_3 + 1):
            if cls.__alarmSound[i] == cls.__steps:
                cls.stopSound(cls.__sound[i], i)

        for i in range(SOUNDEFFECTS_LENGTH):
            if cls.__alarmSoundEffect[i] == cls.__steps:
                cls.stopSoundEffect(cls.__soundEffects[i])

        cls.__steps += 1
        print(f"Advanced to step {cls.__steps}.")
