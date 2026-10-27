import pygame

from dataclasses import dataclass

@dataclass
class InventoryItem:
    name:str
    amount:int=1
    color: str="#8f8f8f"

size = 72-23

#NOTE: the inventory hud is max at 3 slots but the backpack has 10 i guess? then ill make chests
#NOTE: And make item mapping and inventory mapping

class Inventory:
    def __init__(self, slot_count=3):
        self.slots = [None] * slot_count
        self.selected_index = 0

        self.slot_size = (size, size)
        self.slot_gap = 5
        self.outer_padding = 5
        
        self.background_color = "#595959"
        self.slot_color = "#909090"
        self.selected_color = "#f4e8c1"
        self.text_color = "#111111"

    
    def set_item(self, index, item):
        if 0<= index<len(self.slots):
            self.slots[index] = item
    
    def select(self, index):
        if 0 <= index < len(self.slots):
            self.selected_index = index

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            number_keys = {
                pygame.K_1: 0,
                pygame.K_2: 1,
                pygame.K_3: 2,
            }

            if event.key in number_keys:
                self.select(number_keys[event.key])
        
        # elif event.type == pygame.MOUSEWHEEL:
        #     direction = -1 if event.y > 0 else 1
        #     self.select(
        #         (self.selected_index + direction) % len(self.slots) #O MAH GAHH MODULOOO!!
        #     )
    
    def get_selected_item(self):
        return self.slots[self.selected_index]

    def draw(self, screen): ## the only thing i hate when making UI and if i dont know how to draw is i have to DEAL WITH MATH
        slot_width, slot_height = self.slot_size # I mean yeah.. simple math BUT ITS ALOT!

        total_width = (
            self.outer_padding * 2
            + len(self.slots) * slot_width
            + (len(self.slots)-1) * self.slot_gap
        )

        total_height = slot_height + self.outer_padding * 2

        outer_rect = pygame.Rect(
            (screen.get_width() - total_width) // 2,
            screen.get_height() - total_height - 20,
            total_width,
            total_height,
        )

        pygame.draw.rect(
            screen,
            self.background_color,
            outer_rect,
            border_radius=8,
        )

        font = pygame.font.Font(None, 14)

        for index, item in enumerate(self.slots):
            x = (
                outer_rect.x
                + self.outer_padding
                + index * (slot_width + self.slot_gap)
            )

            y = outer_rect.y + self.outer_padding
            slot_rect = pygame.Rect(x,y,slot_width,slot_height)
            pygame.draw.rect(
                screen,
                self.slot_color,
                slot_rect,
                border_radius=6,
            )

            if index == self.selected_index:
                pygame.draw.rect(
                    screen,
                    self.selected_color,
                    slot_rect,
                    width=3,
                    border_radius=6,
                )

            number_text = font.render(
                str(index + 1),
                True,
                self.text_color
            )
            number_rect = number_text.get_rect(
                topleft=(
                    slot_rect.left + 7,
                    slot_rect.top + 5,
                )
            )
            screen.blit(number_text, number_rect)
            
            if item is not None:
                item_font = pygame.font.Font(None, 11)
                item_text = font.render(
                    item.name,
                    True,
                    self.text_color
                )
                item_rect = item_text.get_rect(
                    center=(
                        slot_rect.centerx,
                        slot_rect.centery + 3,
                    )
                )
                screen.blit(
                    item_text, item_rect
                )
                amount_text = font.render(
                    str(item.amount),
                    True,
                    self.text_color,
                )
                
                amount_rect = amount_text.get_rect(
                    bottomright=(
                        slot_rect.right - 6,
                        slot_rect.bottom - 5,
                    )
                )

                screen.blit(amount_text, amount_rect)