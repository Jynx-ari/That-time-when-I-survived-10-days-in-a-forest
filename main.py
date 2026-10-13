import pygame
import sys
from classes.tree import gen_Tree
from functions.center import draw_center
import random

##-- GAME CONFIG --##
w,h = 1200,800


game_conf = {
    "background color": "#365F1A",
    "exittap": 3,
    "fps": 60,
    "tree count": 40,
    "tree scale": 0.2,  # 0.0 to 1.0
    "tree minimum distance": 50,
    "tower color": "#96a09b",
    "antenna color": "#d2372d"
}

exittap: int = 0



def generate_forest(count):
    trees = []
    min_distance = game_conf["tree minimum distance"]
    max_attempts = count * 50
    attempts = 0

    while len(trees) <  count and attempts < max_attempts:
        attempts += 1
        x, y = random.randint(40, w-40), random.randint(55, h-55)
        
        too_close = any(
            (x-tree.leaves_pos[0]) ** 2 + (y - tree.leaves_pos[1]) ** 2 < min_distance ** 2 for tree in trees
        )

        if not too_close:
            trees.append(gen_Tree((x, y), tree_scale=game_conf["tree scale"]))
    return trees

def main():
    pygame.init()

    screen = pygame.display.set_mode((w,h))
    pygame.display.set_caption("10 Days in a forest")

    clock  = pygame.time.Clock()
    running = True


    #the_tree = gen_Tree(tree_pos)
    trees = generate_forest(game_conf["tree count"])

    # Centerpiece: square radio tower with a smaller square antenna on top.
    

    ##Quit handler
    def quit():
        pygame.quit()
        sys.exit()
        return True



    ##Game loop


    while running:
        #Keybinds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    global exittap
                    exittap += 1
                    if exittap >= game_conf["exittap"]:
                        
                        quit()

        #game
        screen.fill(game_conf["background color"])

        # the_tree.draw(screen)
        for tree in trees:
            tree.draw_trunk(screen)

        for tree in trees:
            tree.draw_leaves(screen)

        # Draw the tower first, then the antenna on top of it.
        draw_center(screen, (w,h), game_conf["tower color"], game_conf["antenna color"])
        #pygame update screen
        pygame.display.flip()
        clock.tick(game_conf["fps"])
    pygame.quit()

if __name__ == "__main__":
    main()