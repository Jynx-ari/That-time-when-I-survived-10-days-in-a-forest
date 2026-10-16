import time
import pygame
import sys
import random

from classes.tree import gen_Tree
from functions.center import draw_center
from classes.camera import Camera
from classes.player import Player
from classes.obstacle import Obstacle
from classes.round_manager import RoundManager, RoundPhase



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


}



exittap: int = 0



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

        #calc edging distance...~ heh :>
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

    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("10 Days in a forest")

    clock = pygame.time.Clock()
    running = True
    
    rounds = RoundManager(total_days=10)
    

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




    tower_x, tower_y = m_w // 2, m_h // 2

    tower_rect = pygame.Rect(
        tower_x - 21,
        tower_y - 21,
        42,
        42,
    )

    solid_obs.append(
        Obstacle(tower_rect, name="radio tower")
    )

    
    player = Player((m_w // 2, m_h // 2 +70), )


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
                    global exittap
                    exittap += 1
                    if exittap >= game_conf["exittap"]:
                        quit()
                
                if event.key == pygame.K_SPACE:
                    if rounds.phase == RoundPhase.PREP:
                        rounds.start_wave()
                if event.key == pygame.K_c:
                    if rounds.phase == RoundPhase.ACTIVE_WAVE:
                        rounds.clear_wave()
                
                if event.key == pygame.K_n:
                    if rounds.phase == RoundPhase.WAVE_CLEARED:
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
        keys = pygame.key.get_pressed()
        
        player.move(keys, dt, (m_w, m_h), solid_obs)
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
        
        pygame.display.flip()
       

    pygame.quit()


if __name__ == "__main__":
    main()
