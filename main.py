import time
import pygame
import sys
import random
from pathlib import Path

###   CLASSES

from classes.tree import gen_Tree
from classes.aboutplayer.camera import Camera
from classes.aboutplayer.player import Player
from classes.obstacle import Obstacle
from classes.round_manager import RoundManager, RoundPhase
#from classes.zom.shambler import Shambler
from classes.spatial_grid import SpatialGrid
from classes.pathfinding import (
    build_world_flow_field,
    next_cell_toward_goal,
)
from classes.tower import Tower
from classes.combat.hitscan_weapon import HitscanWeapon
from classes.proximity_prompt import ProximityPrompt

from classes.square_wipe_transition import squarewipetransition
from classes.screen_state import ScreenState

from classes.aboutplayer.inventory import Inventory, InventoryItem





#----------------------------------------


### SCREENS

from screens.main_menu import MainMenu




#----------------------------------------------


###    FUNCTIONS

from functions.center import draw_center
from functions.zombie_spawner import spawn_shamblers

#not really a "function" but a class but still.. i wanna put it here >:(
from functions.easing_styles import (
    EasingStyle, EasingDirection
)

from functions.tween_service import (
    TweenInfo,TweenService
)







##-- GAME CONFIG --##   
w, h = 1200, 800

# Map config
m_w,m_h = 4800 * 2, 3200 * 2

game_conf = {
    "grass": "#365F1A",
    "exittap": 3,
    "fps": 60,
    "camera speed": 5,
    "zoom": 1.0,
    "min_zoom": 0.5,
    "max_zoom": 2.0,
    "zoom_speed": 0.1,
   

    # Forest generation settings
    "tree count": 5000,  # How many trees to try to generate
    "tree scale": 0.9,  # 0.0 to 1.0; larger values make trees bigger
    "tree minimum distance": 15,  # Minimum distance between tree centers
    "tree center exclusion radius": 800,  # Keep this area around the map center clear

    "tower color": "#96a09b",
    "antenna color": "#d2372d",

    "center clearance size": 600,
    "dirt_size": 1200,
    "debug paths": False,

    "zombie_min_spawn": 800,
    "zombie_max_spawn": 1200,

    "workbench": {
        "width": 20,
        "height":12,
        "color": pygame.Color(222,184,135),
        "pos from tower offset": (-150,-123),
        "size": 3
    },




}




exittap: int = 0



def resource_path(relative_p):
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent
    
    return base_path / relative_p




def draw_defeat(screen, font):
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((0,0,0,170))
    screen.blit(overlay, (0,0))
    defeat_text = font.render("You ded lol", True, (255, 80, 80))
    restart_text = font.render("Press ESC thrice to quit :D", True, (255, 255, 255))

    screen.blit(
        defeat_text,
        defeat_text.get_rect(center=(w//2, h//2-25)
        )
    )
    screen.blit(
        restart_text,
        restart_text.get_rect(center=(w//2, h//2 + 25))
    )


def draw_zombies_paths(
    screen,
    zombies,
    camera,
    zoom,
    flowfield,
    cell_size,
    max_steps=80,
):
    for zombie in zombies:
        path_points = [zombie.pos.copy()]
        current_cell = (
            int(zombie.pos.x // cell_size),
            int(zombie.pos.y // cell_size),
        )
        for _ in range(max_steps):
            next_cell = next_cell_toward_goal(
                flowfield,
                current_cell,
            )
            if next_cell is None:
                x,y = current_cell
                distance = flowfield[y][x]

                # print(
                #     f"The path for some reason ended at cell: {current_cell}"
                #     f"its distance is: {distance}"
                # )
                break
            
            n_x,n_y = next_cell

            next_world_pos = pygame.Vector2(
                n_x*cell_size + cell_size /2,
                n_y * cell_size + cell_size / 2
            )

            path_points.append(next_world_pos)
            current_cell = next_cell
        screen_points= [
            camera.syncworld_to_screen(point,zoom)
            for point in path_points
        ]

        if len(screen_points) >= 2:
            pygame.draw.lines(
                screen,
                "#66ccff",
                False,
                [
                    (round(x), round(y))
                    for x, y in screen_points
                ],
                width=2,
            )

        # Mark the zombie's current position.
        zombie_screen_pos = camera.syncworld_to_screen(
            zombie.pos,
            zoom,
        )
        pygame.draw.circle(
            screen,
            "#ffffff",
            (
                round(zombie_screen_pos[0]),
                round(zombie_screen_pos[1]),
            ),
            3,
        )
def generate_forest(count):

    #Pre-optimization

    trees = []
    min_distance = game_conf["tree minimum distance"]

    cell_size = min_distance
    spatial_grid = {}



    center_exclusion_radius = game_conf["tree center exclusion radius"]
    max_attempts = count * 50
    attempts = 0

    center_x, center_y = m_w // 2, m_h // 2
    center_exclusion_radius_squared = center_exclusion_radius ** 2
    min_distance_squared = min_distance ** 2
    clearance_size = game_conf["center clearance size"]

    while len(trees) < count and attempts < max_attempts:
        attempts += 1
        
        
        x,y = random.randint(40, m_w- 40), random.randint(55, m_h -55)

        #calc edging distance...    
        edge_distance = min(x,m_w-x, y,m_h-y)
        
        #edge maxxing?!?!?
        max_edge_distance = min(m_w,m_h)/2

        density = 0.15 + 0.85 * (
            1 - edge_distance / max_edge_distance
        )

        if random.random() > density:
            continue
        


        if (
            abs(x-center_x) < clearance_size
            and abs(y-center_y) < clearance_size
        ):
            continue

        cell_x = int(x//cell_size)
        cell_y = int(y //cell_size)


        too_close = False

        for offset_x in (-1, 0, 1):
            for offset_y in (-1,0,1):
                neighbor_key = (
                    cell_x + offset_x,
                    cell_y + offset_y,

                )

                for tree in spatial_grid.get(neighbor_key, []):
                    dx = x - tree.leaves_pos[0]
                    dy = y - tree.leaves_pos[1]

                    if dx * dx + dy *dy < min_distance_squared:
                        too_close = True
                        break
                
                if too_close:
                    break
            if too_close:
                break


        if not too_close:
            tree=gen_Tree(
                (x, y),
                tree_scale = game_conf["tree scale"]
            )

            trees.append(tree)

            cell_key = (cell_x, cell_y)

            if cell_key not in spatial_grid:
                spatial_grid[cell_key] = []

            spatial_grid[cell_key].append(tree)

    return trees




def main():
    

    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    screen = pygame.display.set_mode((w, h))
    menu = MainMenu(screen)
    screen_state = ScreenState.MAIN_MENU
    game = None
    pygame.display.set_caption("10 Days in a forest")

    font = pygame.font.Font(None, 36)


    clock = pygame.time.Clock()
    running = True

    transition = squarewipetransition(
        dur=0.8,grid=40
    )
    tween_service = TweenService()





    escape_presses = 0
    escape_sequence_start = None
    escape_windows_ms = 1000




    
    rounds = RoundManager(total_days=10)
    zoms = []
    weapon = HitscanWeapon()
    

    zombie_target = 0

    #delay between zombies to replace them thingy
    spawn_retry_timer = 0.0
    next_spawn_delay = random.uniform(3.0,15.0)
    min_spawn_delay = 3.0
    max_spawn_delay = 15.0


    


    
    shake_out_tween = None
    shake_return_tween = None
    shake_phase = None

    def trigger_camera_shake():
        nonlocal shake_out_tween, shake_return_tween, shake_phase ##non local?

        if shake_out_tween is not None:
            shake_out_tween.cancel()
        
        if shake_return_tween is not None:
            shake_return_tween.cancel()
        
        camera.shake_x = 0.0
        camera.shake_y = 0.0

        shake_out_tween = tween_service.create(
            camera,
            TweenInfo(
                0.06,
                EasingStyle.QUAD,
                EasingDirection.OUT
            ),
            {
                "shake_x": random.uniform(-2,2),
                "shake_y": random.uniform(-2,2),
            }
        )

        shake_out_tween.play()
        shake_return_tween = None
        shake_phase = "out"



    
    ## Quit handler
    def quit():
        pygame.quit()
        sys.exit()


    def start_game():

        
        #the tree algo seems to slow down the start of the game BUT NOT ANYMORE!!
        tree_start = time.perf_counter()

        trees = generate_forest(game_conf["tree count"])

        tree_end = time.perf_counter()
        
        print(f"Forest generation:  {tree_end - tree_start:.2f} seconds")
        print(f"Trees generated: {len(trees)}")
        camera = Camera(offset=(m_w // 2 - w // 2, m_h // 2 - h // 2))

        #This also holds it up since the tree trunks collides


        #SOLID IDOL!! pinoy humor
        solid_obs = []


        obstacle_start = time.perf_counter()


        for tree in trees:
            tree_rect = pygame.Rect(
                round(tree.trunk_pos[0]),
                round(tree.trunk_pos[1]),
                tree.trunk_size[0],
                tree.trunk_size[1]
            )
            solid_obs.append(
                Obstacle(tree_rect, name="tree trunk")
            )

        obstacle_end = time.perf_counter()

        print(f"Obstacle making: {obstacle_end - obstacle_start:.2f} seconds")



        tower = Tower((m_w//2, m_h //2))

        tower_pos = tower.pos
        print(f"tower position:", tower_pos)
        tower_size = tower.size

        tower_collision_rect = pygame.Rect(
            round(tower_pos.x - tower_size / 2),
            round(tower_pos.y - tower_size /2),
            tower_size,
            tower_size,
        )

        solid_obs.append(
            Obstacle(tower_collision_rect, name="radio tower", blocks_shots=False)
        )


        workbench_world_pos = tower.pos + pygame.Vector2(
            game_conf["workbench"]["pos from tower offset"]
        )

        workbench_w, workbench_h = (game_conf["workbench"]["width"] * game_conf["workbench"]["size"]), (game_conf["workbench"]["height"] * game_conf["workbench"]["size"])

        workbench_collision_rect = pygame.Rect(
            round(workbench_world_pos.x - workbench_w/2),
            round(workbench_world_pos.y - workbench_h / 2),
            workbench_w,
            workbench_h,
        )

        solid_obs.append(
            Obstacle(
                workbench_collision_rect,
                name="workbench",
                blocks_movement=True,
                blocks_shots=False #by design

            )
        )


        obstacle_grid = SpatialGrid(cell_size=64)

        for obstacle in solid_obs:
            obstacle_grid.insert(obstacle)
        

        workbench_world_pos = tower.pos + pygame.Vector2(
            game_conf["workbench"]["pos from tower offset"]
        )

        workbench_prompt = ProximityPrompt(
            target_pos=workbench_world_pos,
            tween_service=tween_service,
            interact_distance=60,
            context="Workbench",
            action="Craft"
        )



        pathfinding_start=time.perf_counter() #for logs i think
        flowfield, goalcell = build_world_flow_field(
            obstacle_grid=obstacle_grid,
            world_size=(m_w,m_h),
            target_world=tower_pos,
            cell_size=64,
            zombie_radius=15,
            goal_radius=128
        )

        pathfinding_end = time.perf_counter()

        reachable_cells = sum(
            distance is not None
            for row in flowfield
            for distance in row
        )


        # for logssss!!
        print(f"Flow-field build: {pathfinding_end - pathfinding_start:.2} seconds")
        if not goalcell:
            raise RuntimeError("Note to dev: Could not find a valid goal cell near the tower for some reason")
        print(f"flowfield goal: {len(goalcell)}")

        print(f"Tower position: {tower_pos}")

        print(f"Reachable cells: {reachable_cells}")




        
        player = Player((m_w // 2, m_h // 2 +70), )
        hotbar = Inventory(slot_count=3)
        hotbar.set_item(
            0,
            InventoryItem("pistol", amount=1)
        )

        hotbar.set_item(
            1,
            InventoryItem("wood", amount=12)
        )

        backpack = Inventory(slot_count=3*9)
        equipment = {
            "helmet": None,
            "armor": None,
            "accessory": None,
        }


        return{
            "trees": trees,
            "solid_obs": solid_obs,
            "tower": tower,
            "obstacle_grid": obstacle_grid,
            "workbench_prompt": workbench_prompt,
            "flowfield": flowfield,
            "player": player,
            "camera": camera,
            "plrinventory_hotbar": hotbar
        }

    hit_sound = pygame.mixer.Sound(
                        str(
                            resource_path("Assets/Audio/Woof(1).wav")
                        )
                    )
    main_sound = pygame.mixer.Sound(
        str(resource_path("Assets/Audio/main.mp3"))
    )
    main_sound.play(loops=-1)
    game_sound = pygame.mixer.Sound(
        str(resource_path("Assets/Audio/game.mp3"))
    )
    zap_sound = pygame.mixer.Sound(
        str(
            resource_path("Assets/Audio/zap.wav")
        )
    )
    
    ## Game loop
    while running:
        # Keybinds
        for event in pygame.event.get():

            if screen_state == ScreenState.MAIN_MENU:
                action = menu.handle_event(event)

                if action == "start":
                    game = start_game()
                    
                    trees = game["trees"]
                    solid_obs = game["solid_obs"]
                    tower = game["tower"]
                    obstacle_grid = game["obstacle_grid"]
                    workbench_prompt = game["workbench_prompt"]
                    flowfield = game["flowfield"]
                    player = game["player"]
                    camera = game["camera"]
                    hotbar = game["plrinventory_hotbar"]
                    
                    
                    screen_state = ScreenState.PLAYING
                    main_sound.fadeout(1500)
                    
                elif action == "quit":
                    running = False
                
                continue


            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                hotbar.handle_event(event)
                if event.key == pygame.K_ESCAPE:

                    now = pygame.time.get_ticks()

                    if (
                        escape_sequence_start is None
                        or now - escape_sequence_start > escape_windows_ms
                    ):
                        escape_presses = 1
                        escape_sequence_start = now
                    else: 
                        escape_presses += 1

                    if escape_presses >= game_conf["exittap"]:
                        quit()
                
                if event.key == pygame.K_SPACE and rounds.phase==RoundPhase.PREP:
                    rounds.start_wave()
                    spawn_retry_timer = 0.0

                    next_spawn_delay = random.uniform(min_spawn_delay,max_spawn_delay)

                    
                    
                    rounds.start_wave()
                    zombie_target = 5+rounds.day * 5
                    spawn_retry_timer = 0.0

                    zoms = spawn_shamblers(
                        amount=zombie_target,
                        world_size=(m_w, m_h),
                        obstacles=solid_obs,
                        center=tower.pos,
                        min_spawn_distance=game_conf["zombie_min_spawn"],
                        max_spawn_distance=game_conf["zombie_max_spawn"]
                    )


                if event.key == pygame.K_c and rounds.phase == RoundPhase.ACTIVE_WAVE:
                    rounds.clear_wave()
                
                if event.key == pygame.K_n and rounds.phase == RoundPhase.WAVE_CLEARED:
                    rounds.advance_day()



            if event.type == pygame.MOUSEWHEEL:
                zoom = game_conf["zoom"] + event.y * game_conf["zoom_speed"]
                zoom = max(game_conf["min_zoom"], min(zoom, game_conf["max_zoom"]))
                game_conf["zoom"] = zoom

                camera.offset = (
                    max(0,
                    min(
                        player.pos.x - w / (2 * zoom), m_w - w / zoom, m_w - w/zoom
                    )
                    ),
                    max(0,
                    min(
                        player.pos.y - h / (2 *zoom), m_h - h / zoom
                    )
                    
                    )
                )


        dt = clock.tick(game_conf["fps"]) /1000
        if screen_state == ScreenState.MAIN_MENU:
            #clock.tick(game_conf["fps"])
            menu.draw()
            pygame.display.flip()
            continue
        tower.update_health_bar(dt)
        player.update(dt)

        

        weapon.update(dt)
        tween_service.update(dt)

        if (
            shake_phase == "out"
            and shake_out_tween is not None
            and shake_out_tween.completed
        ): 
            shake_return_tween = tween_service.create(
                camera,
                TweenInfo(
                    0.12,
                    EasingStyle.QUAD,
                    EasingDirection.OUT,
                ),
                {
                    "shake_x":0.0,
                    "shake_y":0.0,
                },
            )
            shake_return_tween.play()
            shake_phase = "return"
        

        elif (
            shake_phase == "return"
            and shake_return_tween is not None
            and shake_return_tween.completed
        ):
            shake_phase = "None"



        night_finished = rounds.update(dt)
        if night_finished:
            zoms.clear()
        keys = pygame.key.get_pressed()
        

        if rounds.phase != RoundPhase.DEFEAT:
            player.move(keys, dt, (m_w, m_h), screen, obstacle_grid)
            workbench_prompt.update(player.pos)
            if hotbar.selected_is_weapon() and pygame.mouse.get_pressed()[0] and weapon.is_bro_disabled():
                mouse_screen = pygame.mouse.get_pos()
                mouse_world = pygame.Vector2(
                    mouse_screen[0] / zoom + camera.offset[0],
                    mouse_screen[1] / zoom + camera.offset[1],
                )

                weapon.PEWPEW(
                    player.pos,
                    mouse_world,
                    zoms,
                    obstacle_grid,
                    tween_service,
                    zap_sound
                )
                trigger_camera_shake()


        zoom = game_conf["zoom"]
        camera.follow(player.pos, (m_w, m_h), (w / zoom, h / zoom), dt )
        

      


        # Draw the world
        screen.fill(game_conf["grass"])

        
        center_world = (m_w // 2, m_h // 2)
        center_screen = camera.syncworld_to_screen(center_world, zoom)
        

        tower_rect, wb_rect = draw_center(screen, center_screen, game_conf["tower color"], game_conf["antenna color"],game_conf["workbench"], game_conf["grass"], zoom, game_conf["dirt_size"])

        
        
        for tree in trees:
            trunk_screen_pos = camera.syncworld_to_screen(
                tree.trunk_pos,
                zoom,
            )
            tree.draw_trunk(
                screen,
                trunk_screen_pos,
                zoom
            )

        player_screen_pos = camera.syncworld_to_screen(player.pos,zoom)
        player.aimlook(pygame.mouse.get_pos(), camera, zoom)
        player.draw(screen, player_screen_pos, zoom)

        if rounds.phase == RoundPhase.ACTIVE_WAVE:
            
            #NOTE: dis means the round is currently active :DD


            tower_contact_dist = tower.size / 2 + 15
            player_contact_dist = 15+player.size    
            
            zoms = [zombie for zombie in zoms if not zombie.dead]


            spawn_retry_timer += dt

            if(
                len(zoms) < zombie_target
                and spawn_retry_timer >= next_spawn_delay
            ): 
                missing_zombies = zombie_target - len(zoms)

                new_zombies = spawn_shamblers(
                    amount = missing_zombies,
                    world_size=(m_w, m_h),
                    obstacles=solid_obs,
                    center=tower.pos,
                )

                zoms.extend(new_zombies)
                spawn_retry_timer=0.0

                next_spawn_delay = random.uniform(min_spawn_delay,max_spawn_delay)
        




            for zombie in zoms: 
                zombie.update(game["tower"].pos, dt, obstacle_grid, flow_field=flowfield, cell_size=64)


                tower_dist = zombie.pos.distance_to(tower.pos)
                player_dist = zombie.pos.distance_to(player.pos)

                #tower attack! finally

                if (
                    tower_dist <= tower_contact_dist
                    and zombie.can_attack(dt, "tower")
                ):
                    damage_dealth = tower.take_damage(
                        zombie.damage_to_tower
                    )
                    #print(f"Tower got attacked! -{damage_dealth}")
                
                #player attacked
                if (
                    player_dist <= player_contact_dist
                    and zombie.can_attack(dt, "player")
                ):
                    health_lost = player.take_damage(
                        zombie.damage_to_player
                    )
                    if health_lost >0:
                        hit_sound.play()
                        #print(f"owch -{health_lost}")


            if player.is_dead or tower.is_ded_or_destroyed:
                rounds.end_game()
                zoms.clear()

            for zombie in zoms:
                zombie.draw(screen, camera,zoom)
        

        for tree in trees:
            screen_pos = camera.syncworld_to_screen(
                tree.leaves_pos,zoom
            )

            distance_squared = player.pos.distance_squared_to(
                pygame.Vector2(tree.leaves_pos)
            )
            canopy_radius = tree.leaves_size + player.size
            player_under_canopy = distance_squared <= canopy_radius ** 2
            tree.draw_leaves(
                screen,
                screen_pos,
                zoom,
                transparent=player_under_canopy
            )

        workbench_prompt.draw_prompt(
            screen, camera, zoom
        )
        
        
        if game_conf["debug paths"] and rounds.phase == RoundPhase.ACTIVE_WAVE:
            draw_zombies_paths(
                    screen,
                    zoms,
                    camera,
                    zoom,
                    flowfield,
                    cell_size=64,
            )

        weapon.draw(screen, camera,zoom)

        day_text = font.render(
            f"Day: {rounds.day}",
            True,
            (255, 255, 255)
        )

        phase_text = font.render(
            f"Phase: {rounds.phase.name}",
            True,
            (255, 255, 255)
        )
        screen.blit(day_text, (10,10))
        screen.blit(phase_text, (10, 50))

        if rounds.is_morning:
            time_text = "Daytime"
        else:
            mins = int(rounds.night_remaining) // 60
            secs = int(rounds.night_remaining) % 60
            time_text = f"Night: {mins:02}:{secs:02}"
        
        time_surface = font.render(
            time_text,
            True,
            (255,255,255)
        )
        screen.blit(time_surface, (10, 90))


        # Deprecated: player.update_healthbar(dt)
        player.healthui(screen)
        tower.healthui(screen, font)
        game["plrinventory_hotbar"].draw(screen)


        if rounds.phase == RoundPhase.DEFEAT:
            draw_defeat(screen, font)


        pygame.display.flip()
       

    pygame.quit()


if __name__ == "__main__":
    main()
