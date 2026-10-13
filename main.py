import pygame
import sys
from classes.tree import gen_Tree
##-- GAME CONFIG --##
w,h = 1200,800


game_conf = {
    "background color": "#365F1A",
    "exittap": 3,
    "fps": 60
}

exittap: int = 0

tree_pos = (300, 200)

def main():
    pygame.init()

    screen = pygame.display.set_mode((w,h))
    pygame.display.set_caption("10 Days in a forest")

    clock  = pygame.time.Clock()
    running = True


    the_tree = gen_Tree(tree_pos)
    

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

        the_tree.draw(screen)



        #pygame update screen
        pygame.display.flip()
        clock.tick(game_conf["fps"])
    pygame.quit()

if __name__ == "__main__":
    main()