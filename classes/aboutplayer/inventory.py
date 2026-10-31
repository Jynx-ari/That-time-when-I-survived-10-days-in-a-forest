import pygame

from dataclasses import dataclass



from .item_types import (
    ItemCategory,
    AmmoType,
    WeaponType,
    EquipmentSlot,
    ConsumableType,

)

from .item_properties import (
    WeaponProperties,
    AmmoProperties,
    HealingProperties,
    EquipmentProperties,
    MaterialProperties,
    ConsumableProperties,

)

from .item_definitions import ItemDefinition





size = 72-23

#NOTE: the inventory hud is max at 3 slots but the backpack has 10 i guess? then ill make chests
#NOTE: And make item mapping and inventory mapping


    
@dataclass
class InventoryItem:
    item_id: str
    amount: int = 1

    def __post_init__(self):
        if self.item_id not in ITEMS:
            raise ValueError(f"Unkown item ID: {self.item_id}")
        if self.amount < 1:
            raise ValueError("The item must be atleast 1 or more")
        if self.amount > self.max_stack:
            raise ValueError(f"{self.item_id} can only stack up to {self.max_stack}!!")

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
    "wood_log": ItemDefinition(
        name="Wooden Log",
        category=ItemCategory.MATERIAL,
        color="#8b4513",
        max_stack=64,
        material=MaterialProperties(
            tags=frozenset({"wood", "log"}),
        )
    ),
    "wood_plank": ItemDefinition(
        name="Wooden Plank",
        category=ItemCategory.MATERIAL,
        color="#c49a6c",
        max_stack=64,
        material=MaterialProperties(
            tags=frozenset({"wood", "plank"})
        )
    ),
    "pistol": ItemDefinition(
        name="Glock 17",
        category=ItemCategory.WEAPON,
        color="#d2372d",
        max_stack=1,
        weapon=WeaponProperties(
            damage=12.5,
            weapon_type=WeaponType.PISTOL,
            ammo_type=AmmoType.N9MM

        )
    ),
    "9mm_ammo": ItemDefinition(
        name="9mm Ammo",
        category=ItemCategory.AMMO,
        color="#d2372d",
        max_stack=16,
        ammo=AmmoProperties(
            ammo_type=AmmoType.N9MM
        )
    ),
    "12gauge_ammo": ItemDefinition(
        name="12-Gauge Ammo",
        category=ItemCategory.AMMO,
        color="#6b3f24",
        max_stack=20,
        ammo=AmmoProperties(
            ammo_type=AmmoType.T12_GAUGE,
        ),
    ),
    "wood": ItemDefinition(
        name="Wood Scrap",
        category=ItemCategory.MATERIAL,
        color="#8b4513",
        max_stack=64,
        material=MaterialProperties(
            tags=frozenset({"wood"}),
        ),
    ),

    "metal": ItemDefinition(
        name="Metal Scrap",
        category=ItemCategory.MATERIAL,
        color="#808080",
        max_stack=64,
        material=MaterialProperties(
            tags=frozenset({"metal"}),
        ),
    ),

    "large_medkit": ItemDefinition(
        name="Large Medkit",
        category=ItemCategory.CONSUMABLE,
        color="#ff0000",
        max_stack=4,
        healing=HealingProperties(heal_amount=70),
        consumable=ConsumableProperties(
            consumable_type=ConsumableType.HEALING,
        ),
    ),

    "medium_medkit": ItemDefinition(
        name="Health Pack",
        category=ItemCategory.CONSUMABLE,
        color="#ff0000",
        max_stack=4,
        healing=HealingProperties(heal_amount=25),
        consumable=ConsumableProperties(
            consumable_type=ConsumableType.HEALING,
        ),
    ),

    "small_medkit": ItemDefinition(
        name="Bandage",
        category=ItemCategory.CONSUMABLE,
        color="#ff0000",
        max_stack=8,
        healing=HealingProperties(heal_amount=10),
        consumable=ConsumableProperties(
            consumable_type=ConsumableType.HEALING,
        ),
    ),

    "shotgun": ItemDefinition(
        name="Pump Shotgun",
        category=ItemCategory.WEAPON,
        color="#6b3f24",
        weapon=WeaponProperties(
            damage=15.0,
            weapon_type=WeaponType.SHOTGUN,
            ammo_type=AmmoType.T12_GAUGE,
            pellet_count=6,
            fire_interval=0.135,
        ),
    ),

    "helmet": ItemDefinition(
        name="Hard Hat",
        category=ItemCategory.EQUIPMENT,
        color="#556b2f",
        max_stack=1,
        equipment=EquipmentProperties(
            slot=EquipmentSlot.HELMET,
        ),
    ),

}



class InventorySlot:
    def __init__(self,rect,container,index,slot_type="item"):
        self.rect = pygame.Rect(rect)
        self.container = container
        self.index = index
        self.slot_type = slot_type
    
    def get_item(self):
        if isinstance(self.container, Inventory):
            return self.container.get(self.index)
        
        return self.container[self.index]
    
    def set_item(self, item):
        if isinstance(self.container, Inventory):
            self.container.set(self.index, item)
        else:
            self.container[self.index] = item


class Inventory:
    def __init__(self, slot_count=3):
        self.slots = [None] * slot_count
        self.selected_index = None

        self.slot_size = (size, size)
        self.slot_gap = 5
        self.outer_padding = 5
        
        self.background_color = "#595959"
        self.slot_color = "#909090"
        self.selected_color = "#f4e8c1"
        self.text_color = "#111111"
    

    def get(self, index):
        return self.slots[index]
    
    def set(self, index, item):
        self.slots[index] = item
    
    def swap(self, first_index, second_index):
        self.slots[first_index], self.slots[second_index] = (
            self.slots[second_index],
            self.slots[first_index],
        )


    def selected_is_weapon(self):
        item = self.get_selected_item()
        return(
            item is not None
            and item.definition.weapon is not None
        )

    def set_item(self, index, item):
        if 0<=index<len(self.slots):
            self.slots[index] = item
    
    def select(self, index):
        if 0 <= index < len(self.slots):
            if self.selected_index == index:
                self.selected_index = None
            else:
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
        if self.selected_index is None:
            return None
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
                item_font = pygame.font.Font(None, 12)
                item_text = item_font.render(
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