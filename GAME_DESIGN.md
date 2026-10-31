# That Time I Got Stranded in a Forest

## Main Game Design Document

> Working title. This document describes the intended game, its rules, and the development direction. Values marked **prototype** are starting points for playtesting and are not final balance decisions.

## 1. Game Overview

**Genre:** Bird's-eye-view 2D action survival with light tower defense and scavenging.

**Setting:** A fictional rural forest inspired by the forested areas around Rizal or Laguna, Philippines. The location is fictional and the game is not intended to represent a specific real place.

**Campaign:** Survive 10 days and 10 night waves.

**Objective:** Keep a radio tower operational until the government can coordinate a rescue from Malacanang.

**Failure:** The radio tower is destroyed. Player death normally starts a recovery process instead of immediately ending the run, provided the tower is still operational.

**Core promise:** Fight directly, make short scavenging trips, use the terrain to your advantage, and spend limited resources to survive increasingly dangerous attacks.

## 2. Design Pillars

1. **The player matters.** Automated defenses and the radio tower support the player but cannot win every wave by themselves.
2. **Resources create trade-offs.** Materials used in a building recipe cannot also be used for other recipes; scrap remains a separate currency for direct purchases, upgrades, repairs, and emergency fuel.
3. **Terrain shapes tactics.** The open central clearing, forest gaps, trails, and outer vegetation create different approaches and retreat routes.
4. **Waves test decisions.** Difficulty should increase through enemy combinations, routes, pressure, and behavior, not only larger health numbers.
5. **Build a complete loop first.** Movement, shooting, survival, scavenging, and wave progression should be enjoyable before complex crafting, equipment, or many enemy types are added.

## 3. World and Map

The world is currently planned as a 9,600 x 6,400 world viewed through a 1,200 x 800 window. The player moves in world coordinates while the camera converts world positions to screen positions.

### Map layout

- **Central clearing:** The radio tower and the player's starting camp. This should be mostly open and large enough for combat and movement.
- **Forest transition:** Tree density gradually increases away from the clearing. Preserve gaps and readable routes instead of creating a solid wall.
- **Forest trails:** Routes for short scavenging trips, retreats, and enemy approaches.
- **Abandoned structures:** Possible locations include a shed, small house, sari-sari store, or farm outbuilding. These can become scavenging locations.
- **Outer perimeter:** Enemy spawn locations distributed around the map.

### Forest presentation

Trees use circular canopies for a readable top-down appearance. Each tree has a square trunk used as a solid collision obstacle. Trunks are hidden during the normal view; when the player enters a canopy, the canopy becomes translucent and the trunk is revealed so the collision remains understandable.

The forest should feel dense near the perimeter without blocking all travel. The player should be able to leave the tower clearing, find supplies, and return before the next wave.

## 4. Core Gameplay Loop

Each day follows this structure:

1. **Preparation:** Explore nearby areas, collect limited loot, repair or upgrade the tower, place defenses, and prepare for the next wave.
2. **Active wave:** Start the night. Enemies spawn around the forest and attack the player and radio tower. The player fights, moves, and responds to breaches.
3. **Daylight:** The 90-second night timer expires. If the player and tower survive, the wave is cleared and remaining enemies are removed.
4. **Next day:** Enter the next preparation phase and increase the challenge.
5. Repeat until Day 10 is survived.

Killing every enemy is not required to clear a wave. Survival until daylight is the wave win condition. Player death or tower destruction ends the run according to the recovery and defeat rules below.

Preparation is the main opportunity for exploration. Loot locations are limited and should not endlessly regenerate during a run unless that rule is changed later. Airdrops are a planned optional event, not part of the first prototype.

## 5. Player

### First playable version

- Bird's-eye-view movement in four or eight directions.
- Collision with tree trunks, rocks, buildings, the tower, and placed structures.
- Mouse-aimed hitscan firearm with a firing cooldown.
- Health and a readable player health display.
- Short exploration trips away from the tower.
- Controls for starting waves and placing structures during preparation.

### Player death and recovery

Player death does not immediately end the run if the tower is still operational.

- The player remains at the exact world position where they died.
- Movement, aiming, attacking, and further damage are disabled while recovery is pending.
- The tower sends a visible energy beam to the player's body. The beam is visual feedback, not a shield or weapon.
- **Prototype recovery time:** 10 seconds, measured with elapsed time and `dt`.
- Successful recovery respawns the player at a fixed bunker near the tower with 50% health.
- Tower destruction causes immediate defeat and cancels recovery, even if recovery is in progress.
- Recovery continues through daylight and day transitions.
- A later death may start another recovery cycle if the tower remains operational.
- Temporary post-revival invulnerability is undecided and should only be added if playtesting shows unavoidable repeated deaths.

The bunker is a respawn location, not a permanent invulnerability zone.

### Deferred player systems

Do not add these to the first complete version:

- Hunger, thirst, stamina, or equipment weight.
- Durability on every item.
- Multiple player classes or skill trees.
- Multiplayer.
- A huge explorable world.

## 6. Radio Tower

The radio tower is the campaign objective and a limited defensive asset. Its survival keeps the rescue signal active.

### Health

- The tower has current and maximum health.
- Damage is clamped so health cannot fall below zero.
- Zombies attack when close enough and when their attack cooldown allows it.
- Tower health reaching zero ends the run.
- The primary tower health display is a static HUD bar at the top center.
- **Prototype base health:** 1,500 HP.

### Power and fuel

Fuel is separate from scrap:

- **Scrap** is spendable currency.
- **Fuel** keeps the tower powered during active defense.
- Fuel drains continuously while a zombie wave is active, using `fuel_per_second * dt`.
- Fuel does not drain during preparation unless that rule is changed after playtesting.
- Fuel is clamped at zero.
- When fuel reaches zero, the tower stops attacking and becomes fully vulnerable to enemy damage.
- The run does not end immediately when fuel reaches zero; the player can recover power.
- Fuel can come from junk piles, supply crates, wave rewards, enemy rewards, and other future loot sources.
- The player can deliver fuel to the tower during a wave.
- Scrap can be converted into fuel at the tower during a wave, but the conversion should be inefficient compared with finding fuel directly.

The exact starting fuel, drain rate, loot yields, and conversion rate are balance decisions for playtesting.

### Tower upgrades

Upgrades are purchased with scrap during preparation only.

- Base health: 1,500 HP.
- Each upgrade adds 250 maximum HP.
- Each upgrade also restores 250 current HP, capped at the new maximum.
- Upgrades cannot be purchased during an active wave.
- Maximum level and costs are undecided.
- Upgrade prices should force choices between tower reinforcement, repairs, fuel, and other defenses.

### Future tower pulse

The tower may later emit a pulse at a fixed interval:

- Limited radius.
- Visible effect and cooldown cue.
- One simple effect in the first test: either small damage or a brief slow.
- Useful against small groups, but never strong enough to erase an entire wave.

Power and signal integrity are possible future systems. They should not be added until the basic combat loop is stable.

## 7. Combat

### Player weapon

The first weapon is a mouse-aimed hitscan weapon. A shot resolves immediately along a line from the player toward the mouse cursor's world position. It is not a moving projectile.

**Prototype values:**

- Fire interval: 0.17 seconds.
- Damage: 40 per successful hit.
- Maximum range: 1,500 world units.
- Zombie hit radius: 15 world units.
- Tracer duration: 0.08 seconds.

A shot hits only the first zombie intersected by the shot segment. Tree trunks and the radio tower block shots. A hit should produce a brief tracer, hit flash, damage feedback, and a temporary enemy health bar or indicator.

The player can fire during any phase except defeat. Ammo and reloading are deliberately excluded from the first combat pass, even though ammunition remains a possible later resource.

### Combat rules

- Keep weapon cooldowns separate from zombie attack cooldowns.
- Convert the mouse position from screen coordinates to world coordinates using the current camera and zoom.
- Use finite shot segments rather than infinite lines.
- Compare zombie distance along the shot with the nearest blocking obstacle.
- Remove defeated enemies safely after iteration rather than mutating the active enemy list during iteration.
- Keep visual feedback separate from damage logic so effects cannot apply damage repeatedly every frame.

## 8. Enemies

Every enemy has a primary objective and a combat response.

### Shared behavior

1. Move toward and attack the radio tower.
2. Respect solid obstacles while navigating.
3. Pursue the player when the player enters detection range.
4. Return to the tower objective after a limited pursuit period if the player escapes.
5. Attack the tower on a defined cooldown after reaching it.
6. Respond to barricades according to enemy type.

### Enemy roster

| Enemy | Role | Planned behavior |
| --- | --- | --- |
| Shambler | Basic pressure | Slow, low-complexity enemy that mainly advances toward the tower. |
| Runner | Player pressure | Faster enemy more likely to pursue the player. |
| Brute | Anti-fortification | Slow, durable enemy that can damage barricades blocking its route. |
| Bomber | Area pressure | Later enemy that detonates near a target or defense. |

Start with Shamblers only. Add other enemy types after movement, combat, tower damage, and defenses are reliable.

### Barricades and pathing

- Ordinary enemies should route around blocking barricades when a route exists.
- Heavy enemies can deliberately attack and destroy barricades.
- Barricades have health and disappear when destroyed.
- Ordinary enemies must have a tested fallback behavior when no route can be found so they do not remain stuck forever.

## 9. Building and Defenses

The player selects a structure and places it at a valid location. Placement is instant in the first version.

A valid location must:

- Be inside the playable map.
- Not overlap the player, tower, obstacles, enemies, or another structure.
- Follow any later minimum-spacing rule.
- Have all ingredients required by the structure's crafting recipe in the player's inventory.

Check the recipe before placement, but consume its ingredients only after placement succeeds. A failed or cancelled placement must not remove materials. Building recipes consume item stacks; they do **not** directly deduct scrap.

### Initial structures

| Structure | Crafting recipe | Scrap-equivalent material value | Function |
| --- | --- | ---: | --- |
| Wooden or bamboo barricade | 5 wooden planks | 15 scrap value (5 × 3) | Blocks or redirects ordinary enemies; can be destroyed by heavy enemies. |
| Spike trap | To be defined | Undecided | Damages enemies that cross it; uses or cooldown to be decided later. |
| Scrap turret | To be defined | Undecided | Automatically attacks enemies within a limited range. |

The wooden barricade is the first defined example: one wooden plank has a reference value of 3 scrap, and the recipe requires 5 planks. Its calculated material value is therefore 15 scrap. The player supplies **5 wooden planks**, not 15 scrap. Do not treat the calculated value as a purchase price.

Start with barricades, then add one structure at a time. Recipes for the spike trap and scrap turret remain undecided; do not infer them from their names or their previous prototype scrap prices.

## 10. Resources and Scavenging

The game distinguishes between **scrap currency** and **items/materials**. An item's scrap value is a reference valuation; it is not automatically a currency balance or a crafting cost.

### Scrap currency

Scrap is a spendable currency used for direct transactions that explicitly require it, such as tower upgrades during preparation, repairs if their eventual design uses a direct scrap payment, and inefficient emergency fuel conversion at the tower.

Crafting a building from a recipe does not spend scrap unless a future recipe explicitly introduces scrap as an ingredient. The current wooden barricade recipe does not.

**Prototype economy:**

- Starting scrap: 20.
- Basic enemy reward: 2 scrap.
- Wave-clear reward: 30 scrap.
- Junk-pile reward: approximately 5-15 scrap.

These values should be tested to determine whether a player can afford useful direct purchases without making every resource decision trivial.

### Item and material value

Item definitions may include a scrap_value field. This records the item's reference value in scrap-equivalent terms.

- Wooden plank: scrap_value = 3.
- Wooden barricade recipe: 5 wooden planks.
- Calculated material value: 5 × 3 = 15 scrap-equivalent value.

This calculation is informational. It does not mean that the player pays 15 scrap, receives 15 scrap when crafting, or can automatically sell the planks for 3 scrap each. Selling, trading, or converting items into scrap would be separate mechanics and are not established by this rule.

Crafting consumes the specified item quantities. For the wooden barricade, the player must have 5 wooden planks; after successful placement, those 5 planks are removed from inventory. If placement fails, the planks remain.

The source of wooden planks and other materials is still to be decided. They may come from scavenging, another crafting recipe, dismantling, or a combination later; do not assume a source until it is designed.

### Fuel

Fuel is a separate numeric resource used by the tower. Preferred fuel sources should be physical scavenging locations such as junk piles and supply crates. Wave rewards and other loot can provide smaller reserves. Scrap-to-fuel conversion is an emergency option with a poor exchange rate.

### Loot sources

- **Junk piles:** Scrap currency, materials, and/or fuel.
- **Supply crates:** Fuel and item supplies; ammunition may be included when that system is active.
- **Abandoned structures:** Larger limited caches of items and resources.
- **Enemy drops:** Small scrap rewards or item drops if appropriate.
- **Wave-clear rewards:** Predictable scrap and possible fuel or items.
- **Airdrops:** Later optional event with a visible landing marker and a higher-value cache away from the tower.

Loot locations should be limited and easy to understand. Each loot spot should have a position, contents, and collected state. Collection should use an explicit proximity and interaction action, and a collected spot must not reward the player twice.

Keep the first economy slice small. Scrap and fuel remain the initial numeric resources; add only the item materials needed for the first recipe when the inventory/crafting milestone is reached. Ammunition, medical supplies, and more complex consumables can follow later.

## 11. Campaign Progression

Each day contains one preparation phase and one 90-second night wave. The timer uses real elapsed time and `dt`, not frame counts. When daylight arrives, the player and tower must still be alive for the wave to count as survived.

| Day | Purpose and planned introduction |
| ---: | --- |
| 1 | Tutorial-scale attack. Teach movement, shooting, tower health, and basic defense. |
| 2 | Larger group. Introduce scavenging, scrap, and simple rewards. |
| 3 | Introduce barricade placement and route control. |
| 4 | Introduce a Brute that can break barricades. |
| 5 | Mid-campaign test with multiple approach directions. |
| 6 | Introduce Runners to pressure the player. |
| 7 | Combine enemy types and make positioning more important. |
| 8 | Larger attack. Test repairs, fuel, and resource decisions. |
| 9 | Penultimate assault that targets weak parts of the player's setup. |
| 10 | Final siege. Survive until rescue coordination completes. |

This is a pacing outline, not a locked enemy-count table. Increase difficulty through enemy combinations, spawn directions, speed, route quality, and pressure on defenses, not only by inflating health.

## 12. User Interface

The initial HUD should remain small and readable. It should show:

- Player health.
- Tower health.
- Current day and wave phase.
- Scrap count.
- Fuel count and tower powered/vulnerable status.
- Ammunition when ammunition becomes an active system.
- Selected build item and required recipe ingredients during placement; show calculated scrap-equivalent material value only as reference information, not as a price.
- Short status messages for wave start, wave clear, tower critical state, defeat, and victory.

The tower pulse should have a visible effect and a clear cooldown cue. Avoid a full inventory screen until there are enough distinct items to justify one.

## 13. Technical Direction

The project uses Python and Pygame. The current codebase is split into modules as the prototype grows.

### Main loop responsibilities

1. Read input.
2. Update the active game state using `dt`.
3. Resolve movement, collisions, combat, resources, and interactions.
4. Draw the world and HUD.

Keep gameplay rules separate from drawing where practical. The HUD should read state and must not mutate inventory, health, or wave data.

### Main systems

- **Game loop:** Input, update, resolve, draw.
- **World objects:** Player, tower, enemies, obstacles, structures, and loot spots.
- **Collision:** Simple rectangles and circles initially.
- **Enemy movement:** Direct movement and obstacle avoidance first; reliable grid or flow-field pathfinding as the map and barricades require it.
- **Combat:** Cooldowns, hitscan or projectiles, health, damage, feedback, and defeat/removal.
- **Tower pulse:** Timer, radius check, and one limited effect.
- **Round manager:** Preparation, active wave, wave-cleared, defeat, and victory transitions.
- **Economy:** Scrap/fuel balances, item inventory, recipe validation, and guarded transactions.
- **Placement validation:** Location and recipe-ingredient checks before creating structures; consume ingredients only after successful placement.
- **Camera:** World-to-screen conversion, following, bounds, and zoom.

Use `dt` for movement, cooldowns, timers, fuel drain, and recovery. Keep the existing round manager as the source of truth for day and phase transitions rather than duplicating transition rules in `main.py`.

### Inventory ownership

Inventory belongs to the current run/application context. It should not be placed inside `Player`, `Tree`, `Obstacle`, or the phase-only round manager.

The first inventory model should be a compact resource ledger with guarded operations such as:

- Add or spend scrap/fuel through guarded resource operations.
- Add, remove, and count item stacks for scavenging and crafting.
- Check recipe ingredients and consume them only after a successful craft/placement.
- Prevent negative balances.
- Return success or the actual change so callers cannot silently overspend.

Persistence is not part of the current milestone. If saving is added later, serialize versioned plain data rather than live Pygame objects.

## 14. Development Roadmap

### Milestone 1: World and camera

- Playable world and camera conversion.
- Player movement, aiming, zoom, and map bounds.
- Tree and tower collision.
- Forest density and canopy/trunk presentation.

### Milestone 2: Day and wave foundation

- Preparation, active wave, and wave-cleared phases.
- 90-second night timer.
- Daylight cleanup of remaining enemies.
- Day progression through Day 10.
- Defeat and victory state handling.

### Milestone 3: One enemy and tower danger

- Zombie base class and Shambler.
- Day-scaled spawning.
- Obstacle-aware movement toward the tower.
- Tower attacks, cooldowns, health, and defeat.

### Milestone 4: Player combat

- Mouse-aimed hitscan weapon.
- Range and cooldown.
- Zombie hit testing and obstacle blocking.
- Damage feedback and safe enemy removal.
- Player death and tower-powered recovery.

### Milestone 5: Tower pulse

- Pulse cooldown and radius.
- One limited effect.
- Readable visual feedback.

### Milestone 6: Scrap, fuel, and scavenging

- Scrap and fuel resources with HUD readout.
- Item-stack inventory for recipe ingredients, including wooden planks when the crafting slice begins.
- Keep item scrap_value separate from the scrap currency balance.
- Limited loot spots and explicit collection.
- Wave, enemy, and loot rewards.
- Continuous active-wave fuel drain.
- Fuel delivery and inefficient scrap conversion at the tower.
- Tower unpowered/vulnerable behavior.

### Milestone 7: Barricades and pathing

- Placement preview and validation.
- Recipe-backed barricades: require 5 wooden planks and consume them only after successful placement.
- Show required ingredients and their quantities; do not deduct the calculated 15-scrap material value.
- Enemy routing around barricades.
- Brute interaction later.

### Milestone 8: Complete campaign slice

- Clear defeat, victory, and restart flow.
- Day 1 and Day 2 tuning.
- Complete player-facing HUD.
- A new player can start a run, understand the objective, and finish or lose a wave.

### Milestone 9: Ten-day expansion

- Configure all ten waves.
- Add enemy variety gradually.
- Add spike traps and turrets one at a time.
- Tune the economy and difficulty.

### Milestone 10: Polish

- Replace placeholders with consistent pixel-art assets.
- Add sound effects, hit feedback, pulse visuals, and readable UI.
- Test performance, edge cases, and restart behavior.

## 15. Scope Protection

The first complete target is:

> Move around the clearing, aim at a Shambler, shoot it with an immediate hitscan attack, survive enemies attacking the tower, recover from player death while the tower remains operational, and reach daylight.

After that, add waves and progression, then scavenging and resources, then placement and reliable pathfinding.

Do not add the following until the core loop is enjoyable:

- Complex inventory grids.
- Large crafting trees (the first simple five-plank barricade recipe remains in scope).
- Multiple weapons and ammo management.
- Signal integrity systems.
- Procedural maps.
- Multiplayer.
- Elaborate narrative scenes.
- Many enemy types at once.
- Airdrops as a required objective.

## 16. Open Design Questions

- Final title, story details, and the exact reason the wilderness is dangerous.
- Final weapon balance and whether later weapons use ammunition and reloading.
- Whether the tower pulse damages or slows enemies.
- Starting fuel, fuel drain rate, loot yields, and scrap-to-fuel conversion rate.
- Final tower upgrade costs and maximum level.
- Enemy counts and final tower balance.
- Whether scavenging sites ever restock.
- Final asset resolution and sound direction.
- Whether the tower can be damaged while unpowered during preparation. Recommended: no; preparation should be a recovery window.
- Exact interaction key for scavenging and tower fuel delivery.
- Whether fuel is represented as numeric units or discrete canister items. Recommended: numeric units first.
- Airdrop frequency, warning, landing presentation, contents, and event timing.

## 17. Current Prototype Status

The following systems exist in the source at varying levels of completion:

- Pygame window and main game loop.
- Configurable forest generation with tree spacing and central clearance.
- World-coordinate player movement, camera follow, zoom, mouse aiming, and tree/tower collision.
- Round manager with preparation, active wave, wave-cleared, defeat, and victory states.
- 90-second night timer and daylight cleanup of remaining zombies.
- Zombie base class, Shambler, and day-scaled spawning.
- Tower health, zombie-to-tower attacks, tower health HUD, and defeat checks.
- Hitscan combat scaffolding with range, cooldown, obstacle blocking, tracer, hit flash, damage feedback, and enemy health display.

The following still require implementation, integration, or in-game verification:

- Reliable enemy obstacle routing and stuck-case handling.
- Full in-game day and victory sequence verification.
- Player recovery and bunker respawn.
- Scrap, fuel, inventory, loot, and reward systems.
- Tower upgrades and tower pulse.
- Barricades and placement validation.
- Canopy transparency and trunk reveal behavior.
- Restart flow and complete defeat/victory screens.
- Final balance, audio, assets, and performance verification.

Source-level completion should not be treated as final until the behavior has been played in-game and tested at different camera positions, zoom levels, wave phases, and edge cases.

## 18. Reference and Inspiration

A broad inspiration is the loop of leaving a defended base to gather resources, returning to fortify it, and surviving increasingly difficult attacks. The project remains a distinct single-player bird's-eye-view wilderness survival game centered on a radio tower. Do not copy another game's assets, characters, or specific progression systems.

The guiding principle is simple: finish a small, coherent survival loop first, then expand only when the current version is fun enough to justify the next system.





# Item and Building Data Model Notes

The game uses data-driven definitions: define an item or building once, then refer to it by its ID. Keep carried items, resource balances, and buildable structures as distinct concepts.

**1. Item definitions describe carried items**

An item definition contains its identity and properties. Material items may have a scrap_value field:

```python
@dataclass(frozen=True)
class ItemDefinition:
    name: str
    scrap_value: int = 0
    # Other item properties remain separate and optional.
```

For example, a wooden plank has a reference value of 3 scrap. This is a valuation field, not a price that is automatically charged or paid.

**2. Inventory stacks store item IDs and quantities**

```python
InventoryItem("wooden_plank", amount=5)
```

The item's name, properties, and scrap value come from its definition. The inventory stores the actual quantity available to the player.

**3. Crafting recipes specify ingredients**

```python
@dataclass(frozen=True)
class CraftingRecipe:
    ingredients: dict[str, int]
```

A recipe lists item IDs and the quantities required. Crafting checks that the inventory has every ingredient and consumes those ingredients only when the operation succeeds.

**4. Building definitions reference recipes, not direct scrap costs**

```python
@dataclass(frozen=True)
class BuildingDefinition:
    name: str
    category: BuildingCategory
    recipe: CraftingRecipe
    max_health: int
```

The wooden barricade example is:

```python
WOODEN_BARRICADE_RECIPE = CraftingRecipe(
    ingredients={"wooden_plank": 5}
)
```

With wooden planks valued at 3 scrap each, the recipe has a calculated material value of 15 scrap. The player still provides 5 wooden planks; the game does not deduct 15 scrap. Recipes for other structures are not defined yet.

**5. Keep the systems separate**

- Item inventory stores carried item stacks and crafting materials.
- Scrap and fuel are separate resource balances.
- scrap_value describes an item's reference value only.
- Crafting recipes describe which items and quantities are consumed.
- Building definitions describe constructable objects and their recipes.
- The Inventory HUD and backpack remain separate presentation/storage concerns.

Do not reintroduce a generic building cost field that treats every recipe as a scrap price. Use a recipe/ingredient field for material requirements.
