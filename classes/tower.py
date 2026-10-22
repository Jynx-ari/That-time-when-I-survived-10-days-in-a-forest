import pygame

#im starting to have a habit to make a class just for everything at this point :/

class Tower:
    def __init__(self, pos, max_health=1000):
        self.pos = pygame.Vector2(pos)

        self.max_hp = max_health
        self.curr_hp = self.max_hp
        self.display_hp = self.max_hp

        self.size = 42
    
    #Its this decorator again :0
    @property
    def is_ded_or_destroyed(self):
        return self.curr_hp <= 0
    
    def take_damage(self, damage):
        old_hp = self.curr_hp
        self.curr_hp = max(
            0,
            self.curr_hp - max(0, damage)
        )

        return old_hp - self.curr_hp

    def update_health_bar(self, deltatime):
        transition_speed = 80

        if self.display_hp > self.curr_hp:
            self.display_hp = max(
                self.curr_hp,
                self.display_hp - transition_speed * deltatime
            )
        else:
            self.display_hp = self.curr_hp

    def healthui(self, screen, font):
        bar_w = 300
        bar_h = 24
        x,y = (screen.get_width() - bar_w) // 2, 20

        health_ratio = max(0, min(1, self.curr_hp / self.max_hp))
        display_ratio = max(0, min(1, self.display_hp / self.max_hp))

        pygame.draw.rect(
            screen,
            "#301515",
            (x,y,bar_w,bar_h)
        )

        pygame.draw.rect(
            screen,
            "#f4e8c1",
            (x,y,round(bar_w * display_ratio), bar_h)
        )

        pygame.draw.rect(
            screen,
            "#77ec55",
            (x,y,round(bar_w * health_ratio), bar_h)
        )

        pygame.draw.rect(
            screen,
            "#f4e8c1",
            (x,y,bar_w,bar_h),
            width=2
        )
        health_font = pygame.font.Font(None, 20)
        health_text = health_font.render(
            f"{int(self.curr_hp)} / {int(self.max_hp)}",
            True,
            "#000000"
        )

        screen.blit(
            health_text,
            health_text.get_rect(
                center=(screen.get_width() // 2, y + bar_h // 2)
            )
        )