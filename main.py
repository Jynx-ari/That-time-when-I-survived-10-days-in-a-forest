import pygame
import sys
##-- GAME CONFIG --##
w,h = 1200,800

fps=60


game_conf = {
    "background color": (25,45,30),
}

def main():
    pygame.init()

    screen = pygame.display.set_mode((w,h))
    pygame.display.set_caption("10 Days in a forest")

    clock  = pygame.time.Clock()
    running = True

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
                    quit()

        #game
        screen.fill(game_conf["background color"])
        
        #pygame update screen
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()