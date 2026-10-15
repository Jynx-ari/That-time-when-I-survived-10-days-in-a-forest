#uh oh

class RoundManager:
    PREP = "preparation"
    ACTIVE_WAVE = "active_wave"
    WAVE_CLEARED = "wave_cleared"

    def __init__(self, total_days=10, clear_reward=30):
        self.total_days = total_days 
        self.clear_reward = clear_reward

        self.day = 1
        self.phase = self.PREP
        self.reward_claimed = False

    def start_wave(self):
        #gonna  start the current day's wave

        if self.phase != self.PREP:
            return False
        
        self.phase = self.ACTIVE_WAVE
        self.reward_claimed = False
        return True
    
    def clear_wave(self):
        #Cleaning up!!

        if self.phase != self.ACTIVE_WAVE:
            return 0
        
        self.phase = self.WAVE_CLEARED

        if self.reward_claimed:
            return 0
        
        self.reward_claimed = True
        return self.clear_reward
    
    def advance_day(self):
        #New Day basicalyl

        if self.phase!=self.WAVE_CLEARED:
            return False
        
        if self.day >= self.total_days:
            return False
        
        self.day +=1
        self.phase = self.PREP
        self.reward_claimed = False
        return True