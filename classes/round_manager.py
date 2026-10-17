#uh oh

#yo whats this??
from enum import Enum, auto

class RoundPhase(Enum):
    PREP = auto()
    ACTIVE_WAVE = auto()
    WAVE_CLEARED = auto()
    DEFEAT = auto()
    VICTORY = auto()


class RoundManager:



    def __init__(self, total_days=10, night_dur=90):
        self.total_days = total_days
        self.day = 1
        self.phase = RoundPhase.PREP
        self.night_dur = night_dur #90s | 1min 30s default
        self.night_elapsed = 0.0

    def start_wave(self):
        #gonna  start the current day's wave

        if self.phase != RoundPhase.PREP:
            return False
        
        self.phase = RoundPhase.ACTIVE_WAVE
        self.night_elapsed = 0.0
        return True





    def update(self, dt):
        if self.phase != RoundPhase.ACTIVE_WAVE:
            return
        
        self.night_elapsed += dt

        if self.night_elapsed >= self.night_dur:
            self.night_elapsed = self.night_dur
            self.phase = RoundPhase.WAVE_CLEARED
            return True
        return False
        




    @property #teaching myself more about python classes :0
    def night_remaining(self):
        return max(0.0, self.night_dur - self.night_elapsed)

    
    @property
    def is_morning(self):
        return self.phase != RoundPhase.ACTIVE_WAVE


    def clear_wave(self):
        #Cleaning up!!

        if self.phase != RoundPhase.ACTIVE_WAVE:
            return False
        
        self.phase = RoundPhase.WAVE_CLEARED
        return True
    
    def advance_day(self):
        #New Day basicalyl

        if self.phase!=RoundPhase.WAVE_CLEARED:
            return False
        
        if self.day >= self.total_days:
            self.phase = RoundPhase.VICTORY
            return True
        
        self.day +=1
        self.phase = RoundPhase.PREP
        
        return True

    def end_game(self):
        #Yu lost :)

        if self.phase in (RoundPhase.DEFEAT, RoundPhase.VICTORY):
            return False
        
        self.phase = RoundPhase.DEFEAT
        return True
