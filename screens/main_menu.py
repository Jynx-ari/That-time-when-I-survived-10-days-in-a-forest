import pygame


class MainMenu:
    def __init__(self,screen):
        self.screen = screen
        self.title_font = pygame.font.Font(None, 64)
        self.option_font = pygame.font.Font(None, 32)
    
    def handle_event(self, event):
        if event.type !=pygame.KEYDOWN:
            return None
        
        if event.key == pygame.K_RETURN:
            return "start"
        
        if event.key == pygame.K_ESCAPE:
            return "quit"
        
        return None
    
    def draw(self):
        self.screen.fill("#17221b")

        title = self.title_font.render(
            "That Time I Got Stranded in a Forest and Had to Defend a Radio Tower for Ten Nights!",
            True,
            "white"
        )

        start = self.option_font.render(
            "Press ENTER to start",
            True,
            "white"
        ) 
        quit_text = self.option_font.render(
            "Press ESC to quit",
            True,
            "white"
        )

        center_x = self.screen.get_width() // 2

        self.screen.blit(title, title.get_rect(center=(center_x, 220)))
        self.screen.blit(start, start.get_rect(center=(center_x, 360)))
        self.screen.blit(quit_text, quit_text.get_rect(center=(center_x, 410)))
        