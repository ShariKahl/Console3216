class Ticks:
    def __init__(self, duration: int):
        """
        Initialisiert ein Ticks-Objekt mit der angegebenen Dauer.
        :param duration: Dauer der Ticks
        """
        self.duration = duration

    def get_duration(self) -> int:
        """
        Gibt die Dauer der Ticks zurück.
        :return: Die Dauer in Ticks
        """
        return self.duration

    def set_duration(self, duration: int):
        """
        Setzt die Dauer der Ticks.
        :param duration: Neue Dauer in Ticks
        """
        self.duration = duration

    def __repr__(self) -> str:
        """
        Gibt eine String-Repräsentation des Ticks-Objekts zurück.
        :return: String-Repräsentation
        """
        return f"Ticks(duration={self.duration})"
