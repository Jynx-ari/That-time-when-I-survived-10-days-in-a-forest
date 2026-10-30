#Oh god..

from dataclasses import dataclass
from enum import Enum, auto

class Eco(Enum):
    ADD = auto()
    SUB = auto()

@dataclass
class Wallet: #haha im so broke
    pesos: float = 0.0 #why float? to handle centavos i guess? PESOS FROM PH NOT FROM MEXICAN PESO >:(
    scrap_goods: float=0.0 

    def check_pesos(self, amount: float, _type: Eco):
        if amount < 0:
            raise ValueError("Amount cannot be negative :/")
        if _type == Eco.SUB and amount > self.pesos:
            raise ValueError("Uh oh bro is broke LMAO!!")
        
        
    def manage_pesos(self, amount: float, _type: Eco):
        self.check_pesos(amount, _type)

        if _type == Eco.ADD:
            self.pesos += amount
        elif _type == Eco.SUB:
            self.pesos -= amount
    
    
