from .inventory import ITEMS, InventoryItem
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
        
        remaining = amount

        available = 0
        for item in self.inventory.slots:
            if item is None:
                available += definition.max_stack
            elif item.item_id == item_id:
                available += item.max_stack - item.amount
        
        if available < amount:
            return False
        
        for item in self.inventory.slots:
            if item is not None and item.item_id == item_id:
                space = item.max_stack - item.amount
                added = min(space, remaining)
                item.amount += added
                remaining -= added
        
        for index, item in enumerate(self.inventory.slots):
            if item is None:
                added = min(definition.max_stack, remaining)

                self.inventory.set(
                    index, InventoryItem(item_id, added)
                )

                remaining -= added

                if remaining ==0:
                    return True
        
        return True



    def get_amount(self, item_id):
        total = 0
        
        for item in self.inventory.slots:
            if item is not None and item.item_id == item_id:
                total += item.amount

        return total
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