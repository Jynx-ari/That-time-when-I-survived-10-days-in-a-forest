import pygame
from classes.aboutplayer.inventory import Inventory,InventorySlot

from classes.aboutplayer.item_types import EquipmentSlot

class BackpackUI:
    def __init__(self, hotbar, backpack, equipment):
        self.hotbar = hotbar
        self.backpack = backpack
        self.equipment = equipment

        self.is_open = False
        self.dragged_item = None
        self.drag_source = None
        
        self.slot_rects =[]
        self.panel_rect = pygame.Rect(0,0,0,0)

    def build_slots(self,screen):
        #HOLY REWRITE!!

        self.slot_rects.clear()

        slot_size = self.hotbar.slot_size[0]
        gap = self.hotbar.slot_gap

        columns = 9
        rows = 3

        equip_gap = 30
        hotbar_gap = 20 
        padding = 20
        y_offset = 20 #NOTE: the bigger the lower

        grid_width = columns * slot_size + (columns - 1) * gap
        grid_height = rows * slot_size + (rows-1) * gap

        total_w = grid_width + equip_gap + slot_size
        total_h = grid_height + hotbar_gap + slot_size

        start_x = (screen.get_width() - total_w) // 2
        start_y = (screen.get_height()-total_h)//2
        self.panel_rect = pygame.Rect(
            start_x - padding,
            start_y - padding,
            total_w + padding * 2,
            total_h + padding * 2,
        )

        for index in range(columns * rows):
            column = index % columns
            row = index // columns

            rect = pygame.Rect(
                start_x + column * (slot_size + gap),
                start_y + row * (slot_size + gap),
                slot_size,
                slot_size,
            )

            self.slot_rects.append(
                InventorySlot(rect,self.backpack, index, slot_type="item")
            )
        
        equipment_x = start_x + grid_width + equip_gap

        equipment_types = (
            EquipmentSlot.HELMET,
            EquipmentSlot.ARMOR,
            EquipmentSlot.ACCESSORY
        )

        for equipment_index, slot_type in enumerate(equipment_types):
            rect = pygame.Rect(
                equipment_x,
                start_y + equipment_index * (slot_size + gap),
                slot_size,
                slot_size
            )
            self.slot_rects.append(
                InventorySlot(rect, self.equipment, slot_type, slot_type=slot_type)
            )
        
        hotbar_count = len(self.hotbar.slots)
        hotbar_width = hotbar_count * slot_size + (hotbar_count - 1) * gap
        hotbar_x = start_x + (grid_width - hotbar_width) // 2
        hotbar_y = start_y + grid_height + hotbar_gap

        for i in range(hotbar_count):
            rect = pygame.Rect(
                hotbar_x + i * (slot_size + gap),
                hotbar_y,
                slot_size,
                slot_size
            )
            self.slot_rects.append(
                InventorySlot(rect, self.hotbar, i,slot_type="item")
            )


    def toggle(self):
        self.is_open = not self.is_open
        self.dragged_item = None
        self.drag_source = None
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_b:
                self.toggle()
                return True
            if event.key == pygame.K_ESCAPE and self.is_open:
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
        if source_slot is target_slot:
            return
        
        source_item = source_slot.get_item()
        target_item = target_slot.get_item()

        if not self.can_place(source_item, target_slot):
            return
        if not self.can_place(target_item, source_slot):
            return
        

        if (
            source_item is not None
            and target_item is not None
            and source_item.item_id == target_item.item_id
        ):
            #STACK!
            space = target_item.max_stack - target_item.amount
            moved = min(space, source_item.amount)
            if moved>0:
                target_item.amount += moved
                source_item.amount -= moved

                if source_item.amount <=0:
                    source_slot.set_item(None)
                return
        
        source_slot.set_item(target_item)
        target_slot.set_item(source_item)
    
    def can_place(self,item,target_slot):
        if item is None:
            return True
        if isinstance(target_slot.slot_type, EquipmentSlot):
            equipment = item.definition.equipment
            return(equipment is not None and equipment.slot == target_slot.slot_type)
        return True
    def draw(self,screen):
        if not self.is_open:
            return
        
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0,0,0,140))
        screen.blit(overlay, (0,0))

        pygame.draw.rect(screen, "#595959", self.panel_rect, border_radius=10)

        label_font = pygame.font.Font(None, 14)

        for slot in self.slot_rects:
            pygame.draw.rect(screen, "#909090", slot.rect, border_radius=6)

            if slot.container is self.hotbar and slot.index == self.hotbar.selected_index:
                pygame.draw.rect(screen, "#f4e8c1", slot.rect, width=3, border_radius=6)
            
            item = slot.get_item()

            if item is None:
                if slot.slot_type != "item":

                    label_txt = (
                        slot.slot_type.value
                        if isinstance(slot.slot_type, EquipmentSlot)
                        else slot.slot_type
                    )

                    label = label_font.render(label_txt, True, "#111111")

                    screen.blit(label, label.get_rect(center=slot.rect.center))
                
                continue

            if slot is self.drag_source and self.dragged_item is not None: #If dragging:
                continue
                
            self.draw_item(screen, item, slot.rect)
        
        if self.dragged_item is not None:
            held = pygame.Rect((0,0), self.drag_source.rect.size)
            held.center = pygame.mouse.get_pos()
            self.draw_item(screen, self.dragged_item, held)

    def draw_item(self,screen,item,rect):
        inner = rect.inflate(-10,-10)
        pygame.draw.rect(screen,item.color,inner,border_radius=4)

        font = pygame.font.Font(None,12)

        screen.set_clip(rect) #clip the texts!

        shadow = font.render(item.name, True, "#000000")
        screen.blit(shadow, shadow.get_rect(center=(inner.centerx + 1, inner.centery + 1)))
        name = font.render(item.name, True, "#ffffff")
        screen.blit(name,name.get_rect(center=inner.center))
        screen.set_clip(None)
        if item.amount > 1:
            amount = font.render(str(item.amount), True, "#111111")
            screen.blit(amount,amount.get_rect(bottomright=(rect.right-4,rect.bottom-3)))
