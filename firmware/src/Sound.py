
from Midi import *

CHANNEL_1 = 0
CHANNEL_2 = 1
CHANNEL_3 = 2
CHANNEL_DRUM = 9

SOUNDEFFECTS_LENGTH = 3

CONTROL_CHANNEL_VOLUME = 7
CONTROL_CHANNEL_BALANCE = 10

CONTROL_CHANNEL_VELOCITY = 64

class Sound:
    # Kommentare aus dem C++ Quellcode herauskopiert:

    # faengt bei 1 an zu zaehlen, 0 ist reserviert, siehe alarmSound[]
    __steps: int = 1
    # 3 Elemente: Einen fuer jeden Voice-Channel, alarmSound[] = 0 -> dauerhafter Ton, bzw. kein Endzeitpunkt
    __alarmSound = [0 for _ in range(3)]
    # 3 Elemente: 3 gleichzeitig abspielbare SoundEffects auf der 3x-Polyfonen Drum-Map
    __alarmSoundEffect = [0 for _ in range(3)]
    # Hier werden die Sounds passend zu den Voice-Channels gespeichert, d.h. sound[0] wird auf CHANNEL_1 gespielt
    __sound = [0 for _ in range(3)]
    # Hier werden die SoundEffects auf der Drum-Map gespeichert
    # WICHTIG: Diese sind sortiert, zuletzt hinzugefuegte SoundEffects haben immer den kleineren Index.
    # BSP: [Neuester][Mittlerer][Aeltester]
    __soundEffects = [0 for _ in range(SOUNDEFFECTS_LENGTH)]

    # Private Funktion, um die zeitliche Hierarchie im SoundEffect-Array
    # zu erhalten und um einen SoundEffect nach dem Stoppen aus dem Array zu loeschen
    @classmethod
    def __sortSoundEffects(cls, idx: int):
        for i in range(idx, SOUNDEFFECTS_LENGTH - 1):
            cls.__soundEffects[i] = cls.__soundEffects[i + 1]
            cls.__alarmSoundEffect[i] = cls.__soundEffects[i + 1]
        
        # letzte Stelle im Array "freiraeumen"
        cls.__soundEffects[SOUNDEFFECTS_LENGTH - 1] = 0
        cls.__alarmSoundEffect[SOUNDEFFECTS_LENGTH - 1] = 0
        pass

    @classmethod
    def init(cls):
        Midi.init()
        cls.__steps = 1
        pass

    @classmethod
    def reset(cls):
        pass

    @classmethod
    def setPreset(cls, index: int):
        if index > 127:
            return
        
        Midi.programChange(CHANNEL_1, index)
        Midi.programChange(CHANNEL_2, index)
        Midi.programChange(CHANNEL_3, index)
        pass

    # TODO In C++ setPreset() überladen
    @classmethod
    def setPresetCh(cls, index: int, channel: int):
        if index > 127:
            return
        
        Midi.programChange(channel, index)
        pass

    @classmethod
    def setVolume(cls, volume: int):
        cls.setVolumeCh(volume, CHANNEL_1)
        cls.setVolumeCh(volume, CHANNEL_2)
        cls.setVolumeCh(volume, CHANNEL_3)
        cls.setVolumeCh(volume, CHANNEL_DRUM)
        pass

    # TODO In C++ setVolume() überladen
    @classmethod
    def setVolumeCh(cls, volume: int, channel: int):
        Midi.controlChange(channel, CONTROL_CHANNEL_VOLUME, volume)
        pass

    @classmethod
    def setPanorama(cls, panorama: int):
        cls.setPanoramaCh(panorama, CHANNEL_1)
        cls.setPanoramaCh(panorama, CHANNEL_2)
        cls.setPanoramaCh(panorama, CHANNEL_3)
        pass

    # TODO In C++ setPanorama() überladen
    @classmethod
    def setPanoramaCh(cls, panorama: int, channel: int):
        if (channel > 2):
            return
        
        Midi.controlChange(channel, CONTROL_CHANNEL_BALANCE, panorama)
        pass

    @classmethod
    def playSound(cls, note: int, channel: int):
        Midi.noteOff(channel, cls.__sound[channel])
        Midi.noteOn(channel, note, CONTROL_CHANNEL_VELOCITY)
        cls.__sound[channel] = note
        pass

    # TODO In C++ playSound() überladen
    @classmethod
    def playSoundDura(cls, note: int, channel: int, duration: int):
        Midi.noteOff(channel, cls.__sound[channel])
        cls.playSound(note, channel)
        cls.__alarmSound[channel] = cls.__steps + duration
        cls.__sound[channel] = note
        pass

    @classmethod
    def stopSound(cls, note: int, channel: int):
        Midi.noteOff(channel, note)
        cls.__alarmSound[channel] = 0
        pass

    @classmethod
    def stopSounds(cls):
        for i in range(CHANNEL_1, CHANNEL_3 + 1):
            cls.stopSound(cls.__sound[i], i)
        pass

    @classmethod
    def playSoundEffect(cls, soundEffect: int):
        cls.playSoundEffectDura(soundEffect, 0)
        pass

    @classmethod
    
    # TODO In C++ playSoundEffect() überladen
    def playSoundEffectDura(cls, soundEffect: int, duration: int):
        # Duplikate filtern
        for i in range(0, SOUNDEFFECTS_LENGTH):
            if cls.__soundEffects[i] == soundEffect:
                return
        Midi.noteOn(CHANNEL_DRUM, soundEffect, CONTROL_CHANNEL_VELOCITY)

        # Verschiebung der Sound Effekte und deren Alarmzeiten
        for i in range(SOUNDEFFECTS_LENGTH - 1, 0, -1):
            cls.__soundEffects[i] = cls.__soundEffects[i - 1]
            cls.__alarmSoundEffect[i] = cls.__alarmSoundEffect[i - 1]
        
        cls.__soundEffects[0] = soundEffect
        cls.__alarmSoundEffect[0] = duration
        pass

    @classmethod
    def stopSoundEffect(cls, soundEffect: int):
        idx = 255

        # Index herausfinden
        for i in range(0, SOUNDEFFECTS_LENGTH):
            if cls.__soundEffects[i] == soundEffect:
                idx = i
                break
        
        if idx == 255:
            return
        
        Midi.noteOff(CHANNEL_DRUM, soundEffect)

        # Dies sorgt dafür, dass ein SoundEffect geloescht werden kann
        cls.__sortSoundEffects(idx)
        pass

    @classmethod
    def stopSoundEffects(cls):
        for i in range(0, SOUNDEFFECTS_LENGTH):
            if cls.__soundEffects[i] != 0:
                Midi.noteOff(CHANNEL_DRUM, cls.__soundEffects[i])
                cls.__soundEffects[i] = 0
                cls.__alarmSoundEffect[i] = 0
        pass

    @classmethod
    def step(cls):
        for i in range(CHANNEL_1, CHANNEL_3 + 1):
            if cls.__alarmSound[i] == cls.__steps:
                cls.__alarmSound[i] = 0
                cls.stopSound(cls.__sound[i], i)
                # TODO C++ Quellcode:
                # Serial.println("Sound gestoppt");
        
        for i in range(0, SOUNDEFFECTS_LENGTH):
            if cls.__alarmSoundEffect[i] == cls.__steps:
                cls.__alarmSoundEffect[i] = 0
                cls.stopSoundEffect(cls.__soundEffects[i])
                # TODO C++ Quellcode:
                # Serial.println("Soundeffekt gestoppt");

        cls.__steps += 1
        # TODO C++ Quellcode:
        # Serial.println("steps++");
        pass
