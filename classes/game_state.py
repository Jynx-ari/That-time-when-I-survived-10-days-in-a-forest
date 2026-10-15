#STATEE!! RAHHH!!!

class GameState:
    PLAYING="playing"
    DEFEAT="defeat"
    VICTORY="survived"

    def __init__(self):
        self.state = self.PLAYING
        self.reason=None

    ##ooh whats this?

    
    def __checkWin(self):
        if self.state != self.PLAYING:
            return False
        else:
            return True

    def defeat(self, reason):
        if self.__checkWin() == False:
            return False

        self.state = self.DEFEAT
        self.reason = reason
        return True
    
    def win(self):
        if self.__checkWin() == False:
            return False
        
        self.state = self.VICTORY
        self.reason = "You survived!" # - I mean.. obviously? what else??
        return True