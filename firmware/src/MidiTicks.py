
# TODO C++ Source:
# struct Ticks {
#     Ticks(unsigned duration) : duration(duration) {}

#     unsigned duration;
# };

class Ticks:
    duration: int = 0
    def __init__(self, duration: int):
        type(self).duration = duration
