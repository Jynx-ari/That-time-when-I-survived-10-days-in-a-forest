import time
import pygame
import sys
import random


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

    "center clearance size": 500,
    "debug paths": True,


}




exittap: int = 0



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

                print(
                    f"The path for some reason ended at cell: {current_cell}"
                    f"its distance is: {distance}"
                )
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
    pygame.display.set_caption("10 Days in a forest")

    font = pygame.font.Font(None, 36)


    clock = pygame.time.Clock()
    running = True


    hit_sound = pygame.mixer.Sound("Assets/Audio/Woof(1).wav")



    escape_presses = 0
    escape_sequence_start = None
    escape_windows_ms = 1000




    
    rounds = RoundManager(total_days=10)
    zoms = []

    #the tree algo seems to slow down the start of the game
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
    tower_size = tower.size

    tower_rect = pygame.Rect(
        round(tower_pos.x - tower_size / 2),
        round(tower_pos.y - tower_size /2),
        tower_size,
        tower_size,
    )

    solid_obs.append(
        Obstacle(tower_rect, name="radio tower")
    )

    obstacle_grid = SpatialGrid(cell_size=64)

    for obstacle in solid_obs:
        obstacle_grid.insert(obstacle)
    





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
    print(f"flowfield goal: {goalcell}")
    goal_center = pygame.Vector2(
        goalcell[0] * 64 + 32,
        goalcell[1] * 64 + 32
    )
    print(f"Tower position: {tower_pos}")
    print(f"goal center: {goal_center}")
    print(f"goal to tower distance: {goal_center.distance_to(tower_pos):.1f}")
    print(f"Reachable cells: {reachable_cells}")




    
    player = Player((m_w // 2, m_h // 2 +70), )



    tween_service = TweenService()
    
    
    ## Quit handler
    def quit():
        pygame.quit()
        sys.exit()



    

    ## Game loop
    while running:
        # Keybinds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
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

                    center = pygame.Vector2(m_w // 2, m_h // 2)
                    zoms = spawn_shamblers(
                        amount=5 + rounds.day * 5,
                        center=center,
                        min_radius=900,
                        max_radius=1400,
                        world_size=(m_w, m_h),
                        obstacles=solid_obs
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
        tower.update_health_bar(dt)
        player.update(dt)


        night_finished = rounds.update(dt)
        if night_finished:
            zoms.clear()
        keys = pygame.key.get_pressed()
        

        if rounds.phase != RoundPhase.DEFEAT:
            player.move(keys, dt, (m_w, m_h), screen, obstacle_grid)


        zoom = game_conf["zoom"]
        camera.follow(player.pos, (m_w, m_h), (w / zoom, h / zoom), dt )
        


        # Draw the world
        screen.fill(game_conf["grass"])

        
        center_world = (m_w // 2, m_h // 2)
        center_screen = camera.syncworld_to_screen(center_world, zoom)
        

        draw_center(screen, center_screen, game_conf["tower color"], game_conf["antenna color"], game_conf["grass"], zoom)

        
        
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
            
            tower_contact_dist = tower.size / 2 + 15
            player_contact_dist = 15+player.size    

            for zombie in zoms:
                zombie.update(tower_pos, dt, obstacle_grid, flow_field=flowfield, cell_size=64)


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
                    print(f"Tower got attacked! -{damage_dealth}")
                
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
                        print(f"owch -{health_lost}")


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
        
        if game_conf["debug paths"] and rounds.phase == RoundPhase.ACTIVE_WAVE:
            draw_zombies_paths(
                    screen,
                    zoms,
                    camera,
                    zoom,
                    flowfield,
                    cell_size=64,
            )

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



        if rounds.phase == RoundPhase.DEFEAT:
            draw_defeat(screen, font)


        pygame.display.flip()
       

    pygame.quit()


if __name__ == "__main__":
    main()
