import pygame
import sys
from classes.tree import gen_Tree
from functions.center import draw_center
import random

##-- GAME CONFIG --##
w, h = 1200, 800

game_conf = {
    "background color": "#365F1A",
    "exittap": 3,
    "fps": 60,

    # Forest generation settings
    "tree count": 40,  # How many trees to try to generate
    "tree scale": 0.2,  # 0.0 to 1.0; larger values make trees bigger
    "tree minimum distance": 50,  # Minimum distance between tree centers
    "tree center exclusion radius": 150,  # Keep this area around the map center clear

    "tower color": "#96a09b",
    "antenna color": "#d2372d",
}

exittap: int = 0


def generate_forest(count):
    trees = []
    min_distance = game_conf["tree minimum distance"]
    center_exclusion_radius = game_conf["tree center exclusion radius"]
    max_attempts = count * 50
    attempts = 0

    center_x, center_y = w // 2, h // 2
    center_exclusion_radius_squared = center_exclusion_radius ** 2
    min_distance_squared = min_distance ** 2

    while len(trees) < count and attempts < max_attempts:
        attempts += 1
        x, y = random.randint(40, w - 40), random.randint(55, h - 55)

        # Leave an open clearing around the radio tower.
        if (x - center_x) ** 2 + (y - center_y) ** 2 < center_exclusion_radius_squared:
            continue

        # Keep generated trees from crowding one another.
        too_close = any(
            (x - tree.leaves_pos[0]) ** 2 + (y - tree.leaves_pos[1]) ** 2
            < min_distance_squared
            for tree in trees
        )

        if not too_close:
            trees.append(gen_Tree((x, y), tree_scale=game_conf["tree scale"]))

    return trees


def main():
    pygame.init()

    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("10 Days in a forest")

    clock = pygame.time.Clock()
    running = True

    trees = generate_forest(game_conf["tree count"])

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
        screen.fill(game_conf["background color"])

        for tree in trees:
            tree.draw_trunk(screen)

        for tree in trees:
            tree.draw_leaves(screen)

        draw_center(screen, (w, h), game_conf["tower color"], game_conf["antenna color"])

        pygame.display.flip()
        clock.tick(game_conf["fps"])

    pygame.quit()


if __name__ == "__main__":
    main()
