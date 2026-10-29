import pygame
from classes.aboutplayer.inventory import Inventory
from classes.aboutplayer.inventory_slot import InventorySlot
class BackpackUI:
    def __init__(self, hotbar, backpack, equipment):
        self.hotbar = hotbar
        self.backpack = backpack
        self.equipment = equipment

        self.is_open = False
        self.dragged_item = None
        self.drag_source = None
        
        self.slot_rects =[]
    

    def build_slots(self):
        self.slot_rects.clear()

        #backpack size
        slot_size = 45
        gap = 6

        columns = 9
        rows = 3

        backpack_x = 300
        backpack_y = 180

        for index in range(columns * rows):
            column = index % columns
            row = index // columns

            rect = pygame.Rect(
                backpack_x + column * (slot_size + gap),
                backpack_y + row * (slot_size + gap),
                slot_size,
                slot_size,
            )

            self.slot_rects.append(
                InventorySlot(
                    rect,
                    self.backpack,
                    index,
                    slot_type="item"
                )
            )




    def toggle(self):
        self.is_open = not self.is_open
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_b:
                self.toggle()
                return True
    
        if not self.is_open:
            return False
        

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return self.begin_drag(event.pos)
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                return self.end_drag(event.pos)

        return False

    def begin_drag(self, mouse_pos):
        for slot in self.slot_rects:
            if not slot.rect.collidepoint(mouse_pos):
                continue

            item = slot.get_item()

            if item is None:
                return True
            
            self.dragged_item = item
            self.drag_source = slot
            return True
        return False

    
    def end_drag(self, mouse_pos):
        if self.dragged_item is None:
            return False
        
        target_slot = None

        for slot in self.slot_rects:
            if slot.rect.collidepoint(mouse_pos):
                target_slot = slot
                break
        
        if target_slot is not None:
            self.move_item(self.drag_source, target_slot)

        self.dragged_item = None
        self.drag_source = None
        return True
    
    def move_item(self, source_slot, target_slot):
        source_item = source_slot.get_item()
        target_item = target_slot.get_item()

        if not self.can_place(source_item, target_slot):
            return
        
        if isinstance(source_slot.container, Inventory):
            source_slot.container.set(source_slot.index, target_item)

        if isinstance(target_slot.container, Inventory):
            target_slot.container.set(target_slot.index, source_item)
    
    def can_place(self,item,target_slot):
        if item is None:
            return True
        
        if target_slot.slot_type == "helmet":
            return item.definition.category == "helmet"

        if target_slot.slot_type=="armor":
            return item.definition.category == "armor"
        
        if target_slot.slot_type=="accessory":
            return item.definition.category == "accessory"

        return True  