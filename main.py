import pygame
import sys
import random

from classes.tree import gen_Tree
from functions.center import draw_center
from classes.camera import Camera


##-- GAME CONFIG --##   
w, h = 1200, 800

# Map config
m_w,m_h = 2400, 1600

game_conf = {
    "grass": "#365F1A",
    "exittap": 3,
    "fps": 60,

    # Forest generation settings
    "tree count": 175,  # How many trees to try to generate
    "tree scale": 0.7,  # 0.0 to 1.0; larger values make trees bigger
    "tree minimum distance": 600,  # Minimum distance between tree centers
    "tree center exclusion radius": 300,  # Keep this area around the map center clear

    "tower color": "#96a09b",
    "antenna color": "#d2372d",

    "center clearance size": 250,

}



exittap: int = 0



def generate_forest(count):
    trees = []
    min_distance = game_conf["tree minimum distance"]
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

        too_close = any(
            (x - tree.leaves_pos[0]) ** 2 + (y-tree.leaves_pos[1]) ** 2
            < min_distance_squared
            for tree in trees
        )

        if not too_close:
            trees.append(
                gen_Tree((x,y),
                tree_scale=game_conf["tree scale"]
                )
            )

    return trees




def main():
    pygame.init()

    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("10 Days in a forest")

    clock = pygame.time.Clock()
    running = True

    trees = generate_forest(game_conf["tree count"])
    camera = Camera(offset=(m_w // 2 - w // 2, m_h // 2 - h // 2))
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

        # Draw the world
        screen.fill(game_conf["grass"])

        # for tree in trees:
        #     tree.draw_trunk(screen)
        # Since its bird's eye view, trunks werent never meant to be seen
        draw_center(screen, (w, h), game_conf["tower color"], game_conf["antenna color"], game_conf["grass"])

        for tree in trees:
            screen_pos = camera.syncworld_to_screen(tree.leaves_pos)
            tree.draw_leaves(screen, screen_pos)

        
        pygame.display.flip()
        clock.tick(game_conf["fps"])

    pygame.quit()


if __name__ == "__main__":
    main()
