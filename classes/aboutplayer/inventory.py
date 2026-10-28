import pygame

from dataclasses import dataclass


size = 72-23

#NOTE: the inventory hud is max at 3 slots but the backpack has 10 i guess? then ill make chests
#NOTE: And make item mapping and inventory mapping

@dataclass(frozen=True) #First time using dis shi, like the frozen=true
class ItemDefinition:
    name: str
    category: str
    color: str
    max_stack: int = 1
    heal_amount: int = 0
    damage_amount: float = 0.0
    ammo_type: str | None = None #Okay this is really helpful
    pellet_count: int=1
    fire_interval: float =0.0
    

@dataclass(frozen=True)
class BuildingDefinition:
    name: str
    category: str
    cost: dict[str, int]
    max_health: int
    damage: float = 0.0
    attack_range: float = 0.0
    fire_interval: float = 0.0
    stun_dur: float =0.0

    
@dataclass
class InventoryItem:
    item_id: str
    amount: int = 1

    @property
    def definition(self) -> ItemDefinition: #I wonder whats this like the: "-> ItemDefinition" mean??
        return ITEMS[self.item_id]

    @property
    def name(self) -> str:
        return self.definition.name

    @property
    def color(self) -> str:
        return self.definition.color

    @property
    def max_stack(self) -> int:
        return self.definition.max_stack

ITEMS = {
    "pistol": ItemDefinition(
        name="Glock 17",
        category="weapon",
        color="#d2372d",
        max_stack=1,
        ammo_type="9mm"
    ),
    "9mm_ammo": ItemDefinition(
        name="9mm Ammo",
        category="ammo",
        color="#d2d237",
        max_stack=16,
        ammo_type="9mm"
    ),
    "12guage_ammo": ItemDefinition(
        name="12-Guage Ammo",
        category="ammo",
        color="#6b3f24",
        max_stack=20,
        ammo_type="12guage"
    ),
    "wood": ItemDefinition(
        name="Wood Scrap",
        category="material",
        color="#8b4513",
        max_stack=64,
    ),
    "metal": ItemDefinition(
        name="Metal Scrap",
        category="material",
        color="#808080",
        max_stack=64,
    ),
    "large_medkit": ItemDefinition(
        name="Large Medkit",
        category="consumable",
        color="#ff0000",
        max_stack=4,
        heal_amount=70,
    ),
    "medium_medkit": ItemDefinition(
        name="Health Pack",
        category="consumable",
        color="#ff0000",
        max_stack=4,
        heal_amount=25,

    ),
    "small_medkit": ItemDefinition(
        name="Bandage",
        category="consumable",
        color="#ff0000",
        max_stack=8,
        heal_amount=10,
    ),

    "shotgun": ItemDefinition(
        name="Pump Shotgun",
        category="weapon",
        color="#6b3f24",
        damage_amount=15.0,
        ammo_type="12guage",
        pellet_count=6,
        fire_interval=135.0,
    ),


}


BUILDINGS = {
    "barricade": BuildingDefinition(
        name="Barricade",
        category="defense",
        cost={"wood": 5, "metal": 2},
        max_health=100,
    ),
    "turret": BuildingDefinition(
        name="Brrt brrt sahur", #POOTIS SENTRY HERE!! -Heavy from TF2
        category="defense",
        cost={"metal": 10, "9mm_ammo": 5, "wood":3 },
        max_health=200,
        damage=6.5,
        attack_range=250.0,
        fire_interval=0.1,
    ),
    "bear_trap": BuildingDefinition(
        name="Bear Trap",
        category="defense",
        cost={"metal":2},
        max_health=1, #One time use
        damage=20.0,        
        stun_dur=3.0,

    ),
}






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