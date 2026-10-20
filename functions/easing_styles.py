#easing styles like in roblox lol

from enum import Enum, auto

class EasingDirection(Enum):
    IN = auto()
    OUT = auto()
    IN_OUT = auto()

class EasingStyle(Enum):
    #for now:
    LINEAR = auto()
    QUAD = auto()

def clamp01(val):
    return max(0.0, min(1.0, val))

def linear(t, direction=EasingDirection.IN):
    t = clamp01(t)

    return t

def quad(t, direction=EasingDirection.IN):
    t = clamp01(t)
    if direction == EasingDirection.IN:
      
        return t ** 2
    
    if direction == EasingDirection.OUT:
        return 1 - (1-t)**2
    
    if direction == EasingDirection.IN_OUT:
        if t <0.5:
            return 2*t**2
        
        return 1-((-2 * t + 2) ** 2) / 2
    
    raise ValueError(f"UNKOWN EASING DIRECTION: {direction}")

        