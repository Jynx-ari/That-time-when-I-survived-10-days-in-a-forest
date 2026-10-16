# That Time I Got Reincarnated as a Signal Operator but the Entire Forest Wants Me Dead --- Game Design and Development Plan

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
- [ ] Tune the outward density bias into a gradual increase toward the distant map edges; the chosen design is a mostly open central field with forest that thickens outward.
- [x] Draw a square radio tower and a smaller square antenna above it.
- [x] Add a camera offset and convert the tower/clearing and tree positions from world coordinates to screen coordinates.
- [x] Add configurable zoom limits and mouse-wheel input that updates the clamped zoom variable.
- [x] Add the player triangle and keyboard movement in world coordinates (WASD and arrow keys).
- [x] Make the camera follow the player while keeping the camera inside world bounds.
- [x] Aim the player triangle toward the mouse cursor, converting screen coordinates to world coordinates using the camera offset.
- [x] Apply the selected zoom level to world-to-screen positions and the sizes of the player, tree canopies, tower, antenna, and central clearing.
- [ ] Draw tree trunks in a separate pass behind the canopies, then make the canopy translucent and reveal the trunk when the player enters it.
- [x] Add player collision with tree trunks and the tower (verified in-game).
- [ ] Tune tree spacing, the central clearing, and the gradual outward density bias.
- [x] Create `classes/round_manager.py` with preparation, active-wave, wave-cleared, Day 10 victory, and defeat transitions (unit tests reported passing).
- [x] Create `classes/game_state.py` to represent defeat/victory and prevent changing an already-ended run (unit tests reported passing).
- [x] Correct the in-game round-control guards: `C` now calls `clear_wave()` during `ACTIVE_WAVE`, and `N` calls `advance_day()` during `WAVE_CLEARED`.
- [ ] Verify the full day/round sequence in-game, including the temporary debug clear action and Day 10 victory.
- [x] Add a Shambler subclass and shared Zombie base class with vector position, health, speed, and damage stats.
- [x] Add a Shambler spawner integrated with SPACE wave start; it attempts to spawn a day-scaled group around the tower while checking world bounds and solid obstacles.
- [ ] Change enemy movement to target the radio tower and only update during an active wave.
- [ ] Implement the 90-second night timer, daylight cleanup, tower/player combat, and run-ending conditions.

Forest generation can be tuned in the game_conf dictionary in main.py: change tree count to control how many trees are attempted, tree scale to control their size, tree minimum distance to control spacing between tree centers, and center clearance size to control the half-width and half-height of the square clearing around the map center. The generator has a limited number of placement attempts, so very high tree counts or spacing values may result in fewer trees than requested. The configured world is 9600 × 6400 (`m_w, m_h = 4800 * 2, 3200 * 2`) and the viewport is 1200 × 800. Tree positions are generated in world coordinates. The camera offset and zoom are applied when converting world positions to screen positions, and zoom also scales the player, tree canopies, tower, antenna, and central clearing. Mouse-wheel input adjusts the clamped zoom setting. Smooth camera movement is implemented using delta-time-based exponential easing, but its feel and edge behavior still need in-game verification. The player's triangular front can be made more pointed as a small visual-polish task.

**Chosen forest layout (still requires visual tuning):** use simple circular canopies suited to a true bird's-eye view. The central area should be a huge, mostly open field around the radio tower, with a distant forest that gradually becomes denser toward the outer map edges. Avoid a tight ring of individual trees and avoid a sudden solid wall. Preserve scattered trees and traversable routes through the transition, with denser vegetation near the perimeter. Each tree should have a perfect square trunk as its solid collision obstacle, but the trunk should be hidden during the normal view so the forest reads as circles. When the player passes under a tree's canopy, make that canopy translucent and reveal the square trunk underneath. Tree positions and drawing use world coordinates with camera offset and zoom. Player movement, zoom-scaled object drawing, camera following, and mouse aiming with zoom conversion are implemented. Smooth camera movement, density tuning, trunk rendering, and canopy transparency remain unverified or unfinished. Player collision with tree trunks and the tower has been implemented and verified in-game.

The tower and antenna are currently visual placeholders; tower health, power, signal integrity, pulse behavior, player health, and player shooting are not implemented yet. The round manager and game-state modules exist, and the user reported that their five tests pass; the full in-game sequence still needs verification. Enemy scaffolding is now integrated: `classes/zom/zombie.py` imports Pygame, stores position as a `pygame.Vector2`, stores health/speed/damage stats, and moves using the supplied delta time. `Shambler` passes its configured stats to the base class. `functions/zombie_spawner.py` creates day-scaled Shambler groups around the tower, checks world bounds and obstacle overlap, and is called when SPACE starts a wave. Current limitation: `main.py` updates zombies toward `player.pos` every frame, even outside `ACTIVE_WAVE`; tower-targeting behavior and phase-gated movement are not implemented. The current `C` key remains a debug way to clear a wave, and the 90-second night/daylight lifecycle is planned but not implemented.

### Performance baseline

**Initial startup benchmark (reported from a local run, before optimization):**

| Measurement | Result |
|---|---:|
| Forest generation | 2.77 seconds |
| Trees generated | 5,000 |
| Obstacle creation | 0.01 seconds |

**After spatial-grid optimization (reported from a local run):**

| Measurement | Result |
|---|---:|
| Forest generation | 0.09 seconds |
| Trees generated | 5,000 |
| Obstacle creation | 0.03 seconds |

The forest generator now uses a spatial grid keyed by cell coordinates. Each candidate checks only its own cell and the eight neighboring cells for trees that violate the minimum-spacing rule, rather than scanning every previously accepted tree. With the reported measurements, forest generation fell from 2.77 seconds to 0.09 seconds (about 30.8× faster, or 96.8% less time), while still generating all 5,000 trees. Obstacle creation increased from 0.01 to 0.03 seconds in these individual runs; this small difference may be normal run-to-run variation and should be remeasured if it becomes important.

These are single-run measurements and may vary by machine or run. Use the same measurement method for future comparisons.

## 1. High concept

**Genre:** Bird's-eye-view 2D action-survival with light tower-defense and
scavenging\
**Setting:** A fictional wilderness somewhere inspired by the forested
rural areas around Rizal or Laguna, Philippines. The exact location is
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
region. The world is currently configured as 9600 × 6400 while the visible window is
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
2.  **Night / active wave:** enemies spawn from the forest and attack
    the player and/or radio tower. The player fights and reacts to
    breaches while trying to survive for 90 seconds of real time.
3.  **Daylight / resolution:** if the player and tower survive until the
    90-second night timer expires, the wave is considered survived and
    every remaining zombie dies immediately. Killing every enemy is
    not required to finish a wave; survival until daylight is the
    win condition. Wave-clear rewards can be granted here later.
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

Each day is one 90-second night wave and one preparation period.
The 90 seconds are real-world playing time, measured with frame delta
time (`dt`) rather than frame counts. When the timer expires, daylight
arrives: if the player and tower are still alive, the wave is survived
and all remaining zombies are removed. Killing all enemies early does
not finish the wave. Player death or tower destruction ends the run
immediately, even if the night timer has not expired. Difficulty should
rise through combinations of enemy count, spawn directions, enemy
speed/type, and pressure on defenses---not only by inflating health.

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
-   **Wave manager:** track the day, phase, and 90-second night timer;
    start waves and transition to daylight when time expires. The main
    loop removes remaining zombies on a successful daylight transition.
    Enemy count reaching zero does not end the wave.
-   **Economy:** scrap checks and transaction logic.
-   **Placement validation:** check location and resources before
    creating a structure.
-   **Game states:** preparation, active wave, wave cleared/transition, defeat, victory. Keep the round/day transition rules in `classes/round_manager.py`; the main loop should read the manager's state rather than duplicating transition logic in `main.py`.

Use delta time (`dt`) for movement and cooldowns so behavior does not
depend on frame rate. Keep gameplay rules separate from drawing where
practical.

## 13. Development roadmap

Build and test each milestone before moving on.

### Milestone 1 --- World, camera, and playable arena

-   Keep the map (currently 9600 × 6400) and viewport (1200 × 800) as separate coordinate spaces.
-   Draw world objects through the camera's world-to-screen conversion.
-   [x] Add the player triangle and keyboard movement using world coordinates.
-   [x] Make the camera follow the player and clamp to the map boundaries.
-   [x] Aim the player triangle toward the mouse cursor.
-   [x] Implement zoom-scaled world positions and object sizes; keep zoom configurable and clamped, and convert mouse aiming correctly at every zoom level.
-   [ ] Verify smooth camera follow in-game, including direction changes, zoom while moving, and map edges; tune easing if needed. The delta-time-based easing implementation is present.
-   [ ] Draw tree trunks in a separate pass behind canopies; when the player enters a canopy, make it translucent and reveal its square trunk.
-   [x] Add collision with the tower and tree trunks using world-space hitboxes (implemented and verified in-game).
-   [ ] Tune tree spacing, the central clearing, and the gradual outward density.
-   **Recommended next session:** implement the 90-second night timer in `classes/round_manager.py`, decrement it with `dt` only during `ACTIVE_WAVE`, and transition to `WAVE_CLEARED` once it expires. Connect that transition in `main.py` to remove remaining zombies at daylight. Keep the round manager responsible for timing/state and let `main.py` manage the zombie list. Temporarily test with a 5-second duration, then restore 90 seconds. After the timer lifecycle works, change Shambler movement to target the tower and run only during an active wave; then add tower health and timed enemy attacks. Tree/trunk layering and canopy transparency still need visual verification.
-   **Done when:** the player moves around the world, aims toward the mouse, the camera follows without leaving the map, zoom visibly changes magnification within its limits, and the player cannot walk through solid obstacles.

### Before Milestone 2 --- Day/round system foundation

Implement this before adding any enemies, so enemy spawning can later plug into an existing wave lifecycle.

-   [x] Create `classes/round_manager.py` to track the current day and phase, start a wave, record a cleared wave exactly once, and advance to the next preparation phase.
-   [ ] Add a 90-second night timer that transitions to `WAVE_CLEARED` at daylight; successful survival, not killing all enemies, completes the wave.
-   [ ] Remove all surviving zombies when daylight clears the wave; player death or tower destruction must override the timer and end the run.
-   [x] Use explicit phases in `classes/round_manager.py`: `PREP`, `ACTIVE_WAVE`, and `WAVE_CLEARED`, with `DEFEAT` and `VICTORY` states. `classes/game_state.py` separately represents the run-ending result.
-   [x] Let the player start a wave deliberately from preparation; no countdown is required yet. The SPACE key is wired in `main.py`.
-   [x] Wire a temporary debug input to clear a wave while in `ACTIVE_WAVE` (`C` key guard is now correct in `main.py`).
-   [ ] Connect wave-clear rewards later, and verify victory only after Day 10 has been cleared. The manager's transition tests reportedly pass; the in-game flow still needs verification.
-   [x] Add a minimal HUD display for the day and current phase. In-game transitions still need verification.
-   [x] Add tests for valid/invalid transitions, clearing a wave once, advancing days, and reaching Day 10 victory; the user reported five tests passing. [ ] Verify the transitions through the actual game controls before connecting enemy behavior.
-   **Done when:** the player can move around during preparation, start a wave, clear it through the temporary test action, advance through the day sequence, and reach victory after Day 10 without duplicate rewards or broken state transitions. This milestone is not fully complete until the in-game key guards are corrected and the sequence is verified.

### Milestone 2 --- One enemy and the night/day lifecycle

-   [x] Create the shared `Zombie` base class with vector position, health, speed, and damage values.
-   [x] Create `Shambler` using its own configured stats.
-   [x] Spawn a day-scaled group of Shamblers when SPACE starts a wave; avoid world bounds and existing solid obstacles.
-   [ ] Implement a 90-second night timer, with `dt`-based timing.
-   [ ] At daylight, clear every remaining zombie and set `WAVE_CLEARED`; do not require all enemies to be killed.
-   [ ] Make Shamblers move toward the tower only during `ACTIVE_WAVE`.
-   [ ] Add tower health, proximity-based enemy attacks, attack cooldowns, and defeat when tower health reaches zero.
-   **Done when:** a night starts, lasts 90 seconds, and ends at daylight if the player and tower survive; zombies damage the tower if they reach it, and tower destruction ends the run.

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

### Milestone 5 --- Wave progression and rewards

-   Use the existing preparation and active-wave states.
-   Use the 90-second timer to end a wave at daylight.
-   Remove remaining enemies at daylight; enemy count reaching zero is not a win condition.
-   Give the clear reward and allow the next preparation phase to begin.
-   **Done when:** a full night can start, end at daylight, and progress to the next day reliably.

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

-   [x] Player moves and collides with tree trunks and the radio tower (verified in-game).
-   [x] Player triangle aims toward the mouse cursor, including while the camera follows the player.
-   [x] A configurable forest of randomly generated tree canopies is drawn.
-   [ ] Tree trunks are rendered behind canopies and revealed with canopy transparency when the player enters a canopy.
-   [x] A square radio tower and square antenna are drawn as visual placeholders.
-   [x] The camera offset is applied to world positions for the tree canopies and tower/clearing.
-   [ ] The camera follows the player smoothly and respects map boundaries (implementation is present; in-game verification is still needed).
-   [x] Zoom visibly scales world positions and the sizes of the player, tree canopies, tower, antenna, and clearing.
-   [ ] Camera follow eases smoothly toward the player instead of snapping (implementation is present; in-game behavior still needs verification).
-   [ ] Enemies move toward the tower during the active wave.
-   [ ] Player can damage and defeat enemies.
-   [ ] Enemies can damage the tower.
-   [ ] Tower pulse has a cooldown and limited range.
-   [ ] Player death and tower destruction both end the run.
-   [ ] A night lasts 90 seconds and ends at daylight if the player and tower survive.
-   [ ] All surviving zombies disappear at daylight; killing every zombie is not required to clear a wave.
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
-   Night duration is set to 90 seconds of real-world time for the prototype. The wave ends when daylight arrives if the player and tower survive; all remaining zombies die at daylight. Killing all enemies is not required. This timing and cleanup behavior are design decisions and are not yet implemented.
-   Airdrop frequency, warning/landing presentation, contents, and whether drops arrive on fixed days or as random events.

## 17. Reference and inspiration

**Reference:** [Defend Bunker from Zombies on Roblox](https://www.roblox.com/games/134361906638337/Defend-Bunker-from-Zombies). Its public description highlights building, fortifying, and upgrading a base, rescuing and training survivors, and exploring for resources and rare loot. We can learn from the broad loop of leaving a defended base to gather resources, then returning to prepare for escalating attacks. For this game, adapt that idea to a solo 10-day rescue countdown: short scavenging trips, limited loot locations, scrap-funded defenses, and optional airdrops that tempt the player to travel farther. Airdrops are our planned idea, not a claim that the reference game has that exact mechanic. This project remains a distinct, single-player bird's-eye-view wilderness survival game centered on a radio tower; do not copy the reference game's specific assets or progression systems.

**Design principle:** finish a small, coherent survival loop first.
Expand only when the current version is fun enough to justify the next
system.
