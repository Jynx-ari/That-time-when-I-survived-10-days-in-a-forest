import pygame
import sys
from classes.tree import gen_Tree
import random

##-- GAME CONFIG --##
w,h = 1200,800


game_conf = {
    "background color": "#365F1A",
    "exittap": 3,
    "fps": 60,
    "tree count": 100,
    "tower color": "#96a09b",
    "antenna color": "#d2372d"
}

exittap: int = 0

# tree_pos = (300, 200)




# def generate_forest(count, margin, nono_zones):
#     trees = []

#     for _ in range(count):
#         attempts = 0
#         while attepts < 100:
#             x = random.randint(margin, w - margin)
#             y = random.randint(margin, h - margin)
#             tree_rect = pygame.Rect(x -27, y - 27, 54, 54)
#             if any(tree_rect.collidrect(area) for  area in nono_zones):
#                 attempts+=1
#                 continue
            


def generate_forest(count):
    trees = []
    for _ in range(count):
        x, y = random.randint(40, w-40), random.randint(40, h-40)
        tree = gen_Tree((x,y))
        trees.append(tree)
        return trees



def main():
    pygame.init()

    screen = pygame.display.set_mode((w,h))
    pygame.display.set_caption("10 Days in a forest")

    clock  = pygame.time.Clock()
    running = True


    #the_tree = gen_Tree(tree_pos)
    trees = generate_forest(game_conf["tree count"])

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
            tree.draw(screen)


        #pygame update screen
        pygame.display.flip()
        clock.tick(game_conf["fps"])
    pygame.quit()

if __name__ == "__main__":
    main()