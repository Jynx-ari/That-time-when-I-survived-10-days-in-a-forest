from .inventory import ITEMS
from .item_types import ItemCategory


class ResourceInventory:
    def __init__(self, inventory):
        self.inventory = inventory
    
    def manage_resource(self, item_id, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
            

        definition = ITEMS.get(item_id)

        if definition is None:
            raise ValueError(f"Unknown item: {item_id}")
            

        if definition.category != ItemCategory.MATERIAL:
            raise ValueError("Item is not a material!!!")
            
        return definition
    
    def add(self, item_id, amount=1):
        definition = self.manage_resource(item_id,amount)
        new_amount = self.resources.get(item_id, 0) + amount

        if new_amount > definition.max_stack:
            raise ValueError(
                f"HEY! {item_id} CAN ONLY STACK UP TO {definition.max_stack}!!"
            )
        self.resources[item_id] = new_amount
    def get_amount(self, item_id):
        return self.resources.get(item_id,0)
    
    def bro_has(self,item_id,amount):
        return self.get_amount(item_id) >= amount
    
    def consume(self,item_id, amount):
        self.manage_resource(item_id,amount)

        if not self.bro_has(item_id, amount):
            return False
        
        self.resources[item_id] -= amount
        if self.resources[item_id] == 0:
            del self.resources[item_id] #ooh what this?
        
        return True