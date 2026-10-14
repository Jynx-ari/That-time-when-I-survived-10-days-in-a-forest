# That time when I survived 10 days in a forest --- Game Design and Development Plan

> Alpha Working title. This document records the current direction and a
> practical plan for building the first playable version. Values marked
> **prototype** are starting points for testing, not final balance
> decisions.

## Current implementation status

This section tracks what has actually been implemented in the repository, separately from the full design plan.

**Mandatory project workflow:** Before suggesting or changing code, check the current GitHub files. After an implementation or design item is actually completed and verified, update this status checklist in the same work session. Never tick off a feature that is only planned or has not been checked.

- [x] Pygame window and main game loop.
- [x] Configurable forest tree count in `main.py` (`tree count`).
- [x] Random tree positions generated once when the run starts.
- [x] Minimum spacing check between generated trees (`tree minimum distance`).
- [x] Configurable tree scale, clamped to the range 0.0–1.0 (`tree scale`).
- [x] Configurable square central clearance around the radio tower (`center clearance size`); the square check is in place, with visual tuning still possible.
- [ ] Tune the existing outward density bias into a gradual increase toward the distant map edges; the chosen design is a huge, mostly open central field with a forest that thickens outward.
- [x] Separate trunk and leaves drawing passes, so trunks are drawn behind all canopies.
- [ ] Give each tree a square trunk hidden in the normal overhead view; when the player enters its canopy, make the canopy translucent and reveal the trunk so the player can see their position and collision obstacle.
- [x] Draw a square radio tower and a smaller square antenna above it.
- [ ] Add the player triangle and keyboard movement.
- [ ] Add player collision with trees and the tower.

Forest generation can be tuned in the `game_conf` dictionary in `main.py`: change `tree count` to control how many trees are attempted, `tree scale` to control their size, `tree minimum distance` to control spacing between tree centers, and `center clearance size` to control the half-width and half-height of the square clearing around the map center. The generator has a limited number of placement attempts, so very high tree counts or spacing values may result in fewer trees than requested. The configured world is 2400 × 1600 and the viewport is 1200 × 800. The latest code now samples tree positions and calculates edge distance using the world dimensions, but the clearing center is still calculated from the viewport dimensions and trees are drawn directly in world coordinates with no camera offset. The world-coordinate transition is therefore incomplete; fix the center calculation and introduce a camera before treating large-world rendering as working.

**Chosen forest layout (not implemented/visually verified yet):** use simple circular canopies suited to a true bird's-eye view. The central area should be a huge, mostly open field around the radio tower, with a distant forest that gradually becomes denser toward the outer map edges. Avoid a tight ring of individual trees and avoid a sudden solid wall. Preserve scattered trees and traversable routes through the transition, with denser vegetation near the perimeter. Each tree should have a perfect square trunk as its solid collision obstacle, but the trunk should be hidden during the normal view so the forest reads as circles. When the player passes under a tree's canopy, make that canopy translucent and reveal the square trunk underneath. The generator should use world dimensions for placement and density calculations; rendering must convert world coordinates to screen coordinates through a camera offset. Do not mark these behaviors complete until coded and visually tested.

The tower and antenna are currently visual placeholders; tower health, power, signal integrity, and pulse behavior are not implemented yet.

## 1. High concept

**Genre:** Bird's-eye-view 2D action-survival with light tower-defense and
scavenging\
**Setting:** A fictional wilderness somewhere inspired by the forested
rural areas around Rizal and Laguna, Philippines. The exact location is
deliberately fictional.\
**Campaign:** 10 days / 10 waves\
**Primary objective:** Keep a radio tower operational long enough for
the government in Malacañang to coordinate a rescue.\
**Failure:** The player dies or the tower is destroyed.\
**Core promise:** The player fights directly, while terrain, scavenged
resources, placed defenses, and the tower's limited pulse help them
survive increasingly difficult attacks.

## 2. Design pillars

1.  **The player matters.** Automated defenses support the player but
    cannot win a wave by themselves.
2.  **Every resource has a trade-off.** Scrap spent on a turret cannot
    also be spent on repairs or traps.
3.  **The terrain shapes tactics.** Dense forest, trails, and an open
    central clearing create different approaches and defensive choices.
4.  **Waves test decisions, not just damage numbers.** Later waves
    combine known enemy behaviors in more demanding ways.
5.  **Keep the first version finishable.** Build one complete, testable
    loop before adding inventory complexity, elaborate crafting, or more
    enemy types.

## 3. Setting and map

The game world is a forest clearing in a fictional Philippine rural
region. The world is configured as 2400 × 1600 while the visible window is
1200 × 800. The chosen layout is a huge, mostly open central field around
the tower, with tree density increasing gradually toward a distant outer
forest. A camera is required to view and navigate the larger world. Avoid
a tight ring around the clearing or an evenly random distribution.

### Functional areas

-   **Central clearing:** radio tower and the player's starting camp.
-   **Forest trails and gaps:** narrow routes through the transition zone and outer forest that support short exploration trips, retreat routes, and enemy approach paths. Preserve some traversable gaps rather than sealing the perimeter completely.
-   **Abandoned rural structures:** possible scavenging sites such as a
    shed, small house, sari-sari store, or farm outbuilding.
-   **Forest obstacles:** circular canopies viewed from directly above, with a perfect square trunk beneath each canopy as the solid collision obstacle. Trunks are hidden in the normal view. When the player enters a canopy, that canopy becomes translucent and the square trunk is revealed, keeping the player visible and making the collision obstacle readable. Vegetation density gradually increases from the clearing toward the perimeter, with gaps that support exploration.
-   **Outer perimeter:** enemy spawn points distributed around the map.

The world should be compact enough to finish and test, but large enough for the player to leave the tower's broad clearing and explore toward the distant forest. Use simple circular canopies with hidden square trunks that become visible beneath translucent leaves when the player enters a canopy, plus a few rocks, fences, and abandoned structures or loot locations. The outer forest should feel dense without blocking all travel: preserve readable routes and small gaps that let the player leave the tower's clearing, find supplies, and return. The layout should give the player several meaningful locations to explore and defend.

## 4. Core gameplay loop

1.  **Preparation phase:** search nearby loot spots, collect supplies,
    reload, repair, buy or place defenses.
2.  **Wave phase:** enemies enter from the forest and attempt to reach
    the radio tower. The player fights and reacts to breaches.
3.  **Resolution:** if the player and tower survive, the wave ends and
    rewards are granted.
4.  **Next day:** start the next preparation phase and increase the
    challenge.
5.  Repeat through Day 10. Survive the final assault to complete the
    campaign.

Preparation is the main opportunity for short exploration and scavenging. Exploration must be small but meaningful: the player leaves the tower's clearing, follows gaps through the gradual vegetation transition, visits limited loot locations, and weighs how far to travel before returning for the next wave. Keep the first map compact and avoid turning exploration into a huge open world. Scavenging locations contain limited loot and do not endlessly regenerate during a run unless a later design decision changes that rule. As a later event, an airdrop can land away from the tower and offer a tempting higher-value cache; it should be optional and risky to reach, not a required detour in the first prototype.

## 5. Player mechanics

### First playable version

-   Bird's-eye view movement in four or eight directions.
-   Collision against trees, rocks, buildings, tower, and placed
    structures.
-   A basic firearm with aim direction and a firing cooldown.
-   Health; reaching zero ends the run.
-   A small, simple HUD displaying player health, tower health, current
    day/wave, scrap, and ammunition.
-   Intermission controls for starting the next wave and placing a
    structure.

### Keep out of the first version

-   Complex equipment weight, hunger, thirst, stamina, durability on
    every item, or a large grid inventory.
-   Multiple player classes or skill trees.
-   Multiplayer.
-   A huge explorable map.

These could be considered only after the core loop is fun.

## 6. Radio tower mechanics

The tower is both the campaign objective and a modest defensive asset.

### Initial implementation: radio-powered pulse

-   The tower has health.
-   At a fixed interval, it emits a pulse that affects enemies within a
    limited radius.
-   For the first prototype, choose one simple pulse effect: deal a
    small amount of damage **or** briefly slow enemies. Do not implement
    both until testing shows it is needed.
-   The pulse has a visible radius or effect so players understand its
    range and cooldown.
-   The pulse should help with small groups, not erase a whole wave.
-   Enemies that reach the tower can damage it.
-   Tower health reaching zero ends the run.

### Future systems, deliberately deferred

The broader concept includes **health, power, and signal integrity**.
For the first version, implement health only. Later, power could limit
pulse use or require fuel, and signal integrity could represent
transmission quality and require equipment repairs. Do not add those
systems until the basic combat loop is stable.

## 7. Enemy behavior

Every enemy has a primary objective and a combat response.

### Shared behavior

1.  The enemy's primary goal is to reach and attack the radio tower.
2.  It navigates toward the tower while respecting solid obstacles.
3.  If the player enters its detection range, it may switch to attacking
    or pursuing the player.
4.  If the player escapes, the enemy can pursue for a short grace
    period, then return to its tower objective.
5.  On reaching the tower, it attacks at a defined interval.
6.  If it encounters a barricade, its response depends on its type.

### Barricade interaction --- established design

-   **Ordinary enemies:** try to find another route around a blocking
    barricade where a route is available.
-   **Heavy enemies:** can deliberately attack and destroy blocking
    barricades.
-   Barricades have health and disappear when destroyed.
-   If a route cannot be found, ordinary enemies should not get stuck
    forever. A simple fallback behavior must be defined and tested.

### Enemy roster (add gradually)

  -----------------------------------------------------------------------
  Type                    Role                    First-pass behavior
  ----------------------- ----------------------- -----------------------
  Shambler                Basic pressure          Slow, low complexity,
                                                  mainly advances toward
                                                  the tower

  Runner                  Player pressure         Faster and more likely
                                                  to pursue the player

  Brute                   Anti-fortification      Slow, durable, damages
                                                  barricades blocking its
                                                  route

  Bomber                  Area pressure           Later addition;
                                                  detonates near a target
                                                  or defense
  -----------------------------------------------------------------------

Start with **Shamblers only**. Add a Brute after movement, combat, tower
damage, and barricade interaction work. Do not implement all four at
once.

## 8. Building and defenses

### Placement system

The player selects a structure, then places it at a valid location in
the world. Placement is instant in the first version.

A location is valid only if: - It is inside the playable map. - It does
not overlap the player, tower, obstacles, enemies, or another
structure. - It respects any minimum spacing rules introduced later. -
The player has enough scrap.

Show a placement preview or clear valid/invalid indicator if practical.
Deduct scrap only when placement succeeds.

### Initial structures

  ------------------------------------------------------------------------
  Structure                           Prototype cost Function
  --------------------- ---------------------------- ---------------------
  Wooden/bamboo                             15 scrap Blocks or redirects
  barricade                                          ordinary enemies; can
                                                     be destroyed by heavy
                                                     enemies

  Spike trap                                20 scrap Damages enemies that
                                                     cross it; limited
                                                     uses or a cooldown
                                                     can be decided later

  Scrap turret                              40 scrap Automatically attacks
                                                     enemies within a
                                                     limited range
  ------------------------------------------------------------------------

These costs are placeholders. Start with barricades only, then add one
structure at a time.

## 9. Resources and scavenging

### Primary currency: scrap

Scrap pays for structures and selected supplies. It is earned through
enemy rewards, wave completion, and scavenging.

### Consumables

-   **Ammunition:** needed to keep the player's weapon firing.
-   **Medical supplies:** restore player health.
-   **Repair materials or scrap:** repair the tower or structures if
    repair costs are included.

Avoid introducing too many resource types at the beginning. The first
playable version can use **scrap and ammunition** only, with player
health represented by a simple health bar.

### Loot sources

-   Junk piles: small amounts of scrap.
-   Supply crates: ammunition or scrap.
-   Abandoned shed or house: a larger, limited loot cache.
-   Enemy drops: small scrap rewards if appropriate.
-   Wave-clear reward: a predictable amount of scrap.
-   **Airdrops (later feature):** occasional supply drops placed away from the tower, with a visible landing marker or signal. They can contain a more valuable mix of scrap, ammunition, or medical supplies, creating a choice between staying near the tower and exploring farther from safety. Airdrops are planned, not part of the first playable build.

Scavenging should create choices about what to afford before the next
wave. Loot locations should be limited and easy to understand, not
random coins scattered everywhere.

### Example starting economy (for testing)

-   Starting scrap: 20.
-   Each basic enemy defeated: 2 scrap.
-   Wave-clear reward: 30 scrap.
-   Junk piles: approximately 5--15 scrap.

These numbers are not final. Test whether a player can afford one useful
defense after Wave 1 without being able to buy everything.

## 10. Campaign structure: 10 days

Each day is one wave and one preparation period. Difficulty should rise
through combinations of enemy count, spawn directions, enemy speed/type,
and pressure on defenses---not only by inflating health.

  -----------------------------------------------------------------------
                                       Day Purpose / planned introduction
  ---------------------------------------- ------------------------------
                                         1 Tutorial-scale attack; learn
                                           movement, shooting, tower
                                           health, and pulse

                                         2 Slightly larger group;
                                           introduce scavenging and scrap
                                           rewards

                                         3 Introduce barricade placement
                                           and route control

                                         4 Introduce a Brute that can
                                           break barricades

                                         5 Mid-campaign test with
                                           multiple approach directions

                                         6 Introduce Runners to pressure
                                           the player

                                         7 Combine enemy types and make
                                           positioning more important

                                         8 Larger attack; test repairs
                                           and resource decisions

                                         9 Penultimate assault; challenge
                                           weak parts of the player's
                                           setup

                                        10 Final siege; survive until
                                           rescue coordination completes
  -----------------------------------------------------------------------

This is a pacing outline, not a locked enemy-count table. Balance the
actual number of enemies after the first playable build.

## 11. User interface

Keep the initial HUD small and legible:

-   Player health.
-   Tower health.
-   Current day and wave status.
-   Scrap count.
-   Ammunition.
-   Selected build item and its cost during placement.
-   Short status message for wave start, wave clear, tower critical,
    defeat, and victory.

The pulse should have a visible effect and a clear cooldown cue. Avoid a
large inventory screen until there is enough equipment to justify one.

## 12. Technical approach

**Suggested technology:** Python + Pygame, using a single `main.py` at
first. Split into modules once the prototype grows.

Possible later structure:

``` text
wilderness_survival/
├── main.py
├── settings.py
├── player.py
├── enemy.py
├── tower.py
├── structures.py
├── waves.py
├── economy.py
├── ui.py
└── assets/
    ├── images/
    ├── sounds/
    └── fonts/
```

### Main technical systems

-   **Game loop:** read input, update game state, resolve collisions and
    combat, draw the frame.
-   **World objects:** player, tower, enemies, obstacles, structures,
    loot spots.
-   **Collision:** use simple rectangles/circles initially.
-   **Enemy movement:** begin with direct movement and basic obstacle
    avoidance on a deliberately simple map. Add grid-based A\*
    pathfinding when the map and barricades require reliable
    route-finding.
-   **Combat:** weapon cooldowns, projectiles or hitscan-style shots,
    health, damage, and defeat/removal.
-   **Tower pulse:** timer, radius check, and one effect.
-   **Wave manager:** track enemies spawned and alive; start and finish
    waves; issue rewards.
-   **Economy:** scrap checks and transaction logic.
-   **Placement validation:** check location and resources before
    creating a structure.
-   **Game states:** menu, preparation, active wave, defeat, victory.

Use delta time (`dt`) for movement and cooldowns so behavior does not
depend on frame rate. Keep gameplay rules separate from drawing where
practical.

## 13. Development roadmap

Build and test each milestone before moving on.

### Milestone 1 --- Playable arena

-   Create the Pygame window and game loop.
-   Draw a grassy clearing with simple forest obstacles.
-   Add player movement and collision.
-   Draw the radio tower in the center.
-   **Done when:** the player can move around the map without walking
    through solid objects.

### Milestone 2 --- One enemy

-   Spawn one Shambler.
-   Move it toward the tower.
-   Add collision and tower attack behavior.
-   Add tower health and defeat state.
-   **Done when:** the enemy can reach and damage the tower, and tower
    destruction ends the run.

### Milestone 3 --- Player combat

-   Add the player's weapon and firing cooldown.
-   Add enemy health, damage, death, and scrap rewards.
-   Add player health and player-death defeat.
-   **Done when:** the player can defeat enemies and can also lose.

### Milestone 4 --- Tower pulse

-   Add pulse cooldown and radius.
-   Show a visible pulse effect.
-   Apply a small damage effect or a short slow.
-   **Done when:** the tower helps in combat without defeating every
    enemy by itself.

### Milestone 5 --- Wave manager

-   Add preparation and active-wave states.
-   Spawn a small fixed Wave 1.
-   Detect when the wave is cleared.
-   Give the clear reward and allow the next wave to begin.
-   **Done when:** a full wave can start, end, and restart reliably.

### Milestone 6 --- Scrap and scavenging

-   Add scrap display and limited loot spots.
-   Allow the player to collect a loot spot once.
-   Add enemy and wave rewards.
-   Make the player travel a short distance from the tower to reach at least some loot, so the forest layout supports small exploration decisions.
-   **Done when:** the player can collect and spend scrap across waves and at least one loot spot encourages a short trip beyond the central clearing.

### Milestone 7 --- Barricade placement and pathing

-   Add a placement preview and validity checks.
-   Place a barricade for scrap.
-   Make ordinary enemies route around it.
-   Add the Brute's ability to damage blocking barricades later.
-   **Done when:** barricades create a meaningful route choice and
    enemies do not become permanently stuck.

### Milestone 8 --- First complete campaign slice

-   Add the remaining basic UI.
-   Tune Day 1 and Day 2.
-   Add a restart flow and clear defeat/victory screens.
-   **Done when:** a player unfamiliar with the code can start a run,
    understand the objective, and finish or lose a wave.

### Milestone 9 --- Expand to 10 days

-   Configure all ten waves.
-   Add enemy variety gradually.
-   Add spike traps and scrap turrets one at a time.
-   Tune the economy and difficulty.
-   **Done when:** all ten waves can be completed and the campaign
    reaches a clear ending.

### Milestone 10 --- Polish

-   Replace placeholders with consistent pixel-art assets.
-   Add sound effects, hit feedback, pulse visuals, and readable UI.
-   Test performance, edge cases, and restart behavior.
-   **Done when:** the game is understandable and stable, not merely
    feature-rich.

## 14. Scope protection

Do **not** build the whole design at once. The first meaningful target
is:

> Move around a clearing, shoot one enemy, watch it approach and damage
> the tower, and use the tower's pulse to help defeat it.

Then add waves. Then scrap. Then placement. Then reliable pathfinding
and more enemies.

Postpone power consumption, signal integrity, advanced crafting, complex
inventory, procedural maps, multiple weapons, elaborate narrative
scenes, and extra enemy types until the core loop is enjoyable.

## 15. First playable prototype acceptance checklist

-   [ ] Player moves and collides with obstacles.
-   [x] A configurable forest of randomly generated trees is drawn with spacing, a clear central area, and separate trunk/canopy layers.
-   [x] A square radio tower and square antenna are drawn as visual placeholders.
-   [ ] One enemy can navigate toward the tower.
-   [ ] Player can damage and defeat the enemy.
-   [ ] Enemy can damage the tower.
-   [ ] Tower pulse has a cooldown and limited range.
-   [ ] Player death and tower destruction both end the run.
-   [ ] A wave starts and ends correctly.
-   [ ] The player can receive and spend scrap.
-   [ ] A barricade can be placed at a valid location.
-   [ ] The game can restart after defeat.

## 16. Open design questions

These can remain undecided while the prototype is built:

-   Exact title, story details, and why the wilderness is dangerous.
-   Exact weapons, ammo capacity, and reload behavior.
-   Whether pulse damages or slows enemies (test one first).
-   Whether power and signal integrity are implemented after the first
    version.
-   Final costs, loot quantities, enemy counts, and tower stats.
-   Whether scavenging sites ever restock.
-   Final asset resolution and sound design. Current visual direction: bird's-eye view with circular canopies and no visible trunks in the normal view; each tree has a square trunk that is revealed when its canopy becomes translucent around the player.
-   Airdrop frequency, warning/landing presentation, contents, and whether drops arrive on fixed days or as random events.

## 17. Reference and inspiration

**Reference:** [Defend Bunker from Zombies on Roblox](https://www.roblox.com/games/134361906638337/Defend-Bunker-from-Zombies). Its public description highlights building, fortifying, and upgrading a base, rescuing and training survivors, and exploring for resources and rare loot. We can learn from the broad loop of leaving a defended base to gather resources, then returning to prepare for escalating attacks. For this game, adapt that idea to a solo 10-day rescue countdown: short scavenging trips, limited loot locations, scrap-funded defenses, and optional airdrops that tempt the player to travel farther. Airdrops are our planned idea, not a claim that the reference game has that exact mechanic. This project remains a distinct, single-player bird's-eye-view wilderness survival game centered on a radio tower; do not copy the reference game's specific assets or progression systems.

**Design principle:** finish a small, coherent survival loop first.
Expand only when the current version is fun enough to justify the next
system.
