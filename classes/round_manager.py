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



    def __init__(self, total_days=10):
        self.total_days = total_days
        self.day = 1
        self.phase = RoundPhase.PREP

    def start_wave(self):
        #gonna  start the current day's wave

        if self.phase != RoundPhase.PREP:
            return False
        
        self.phase = RoundPhase.ACTIVE_WAVE
        
        return True
    
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
        