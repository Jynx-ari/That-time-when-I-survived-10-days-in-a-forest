import pygame
from functions.easing_styles import EasingStyle, EasingDirection
from functions.tween_service import TweenService, TweenInfo

#yeah this ones also inspired by roblox

default_conf = {
    "KeyBG": {
        "color1": (25,25,25),
        "color2": (255,255,255),
        "width": 2,
        "border_radius": 5
    }
}

class ProximityPrompt:
    def __init__(self, target_pos, tween_service, interact_distance=100, Key=pygame.K_e, hold=300, context="Something", action="Interact"): #100 dist by default | 300ms hold?
        self.target_pos = pygame.Vector2(target_pos)
        self.interact_dist = interact_distance
        self.is_visible = False
        self.Key = Key
        self.hold = hold
        self.context = context
        self.action = action

        self.tween_service = tween_service
        self.alpha = 0.0
        self.pop_offset = 12.0
        self._was_near = False
        self.tween_dur = 0.25
        self.tween_dur2 = 0.18
        self.height=30

    def update(self, plr_pos):
        plr_pos = pygame.Vector2(plr_pos)
        
        distance = plr_pos.distance_to(self.target_pos)
        is_near = distance <= self.interact_dist

        if is_near and not self._was_near:
            self.is_visible = True

            self.tween_service.create(
                self,
                TweenInfo(
                    self.tween_dur,
                    EasingStyle.QUAD,
                    EasingDirection.OUT,
                ),
                {
                    "alpha": 255.0,
                    "pop_offset": 0.0,
                },
            ).play()
        
        elif not is_near and self._was_near:
            self.tween_service.create(
                self,
                TweenInfo(
                    self.tween_dur2,
                    EasingStyle.QUAD,
                    EasingDirection.IN
                ),
                {
                    "alpha": 0.0,
                    "pop_offset": 12.0,
                }
            ).play()
        
        self._was_near = is_near

    
    def draw_prompt(self, screen, camera, zoom):
        prompt_scale = zoom
        prompt_font = pygame.font.Font(None, max(1, round(21 * prompt_scale)))
        small_font = pygame.font.Font(None, max(1, round(17 * prompt_scale)))
        
        #prompt_y_offset = round(60 *prompt_scale)
        padding_X = round(20*prompt_scale)
        padding_Y = round(12 * prompt_scale)

        if self.alpha <= 0:
            return
        
        screen_pos = camera.syncworld_to_screen(
            self.target_pos,
            zoom
        )

        alpha = round(self.alpha)

        #KEY
        key_surface = prompt_font.render(
            pygame.key.name(self.Key).upper(),
            True,
            (255,255,255)
        )

        #ACTION

        action_surface = small_font.render(
            self.action,
            True,
            (255,255,255)
        )

        #context
        context_surface = small_font.render(
            self.context,
            True,
            (255,255,255)
        )
        
        key_rect = key_surface.get_rect(
            center=(
                round(screen_pos[0]),
                round(screen_pos[1] - self.height * zoom + self.pop_offset*zoom),
            )
        )

        action_rect = action_surface.get_rect(
            midtop = (
                key_rect.centerx,
                key_rect.bottom + 8 * zoom,

            )
        )

        context_rect = context_surface.get_rect(
            midbottom=(
                key_rect.centerx,
                key_rect.top - 8*zoom,
            )
        )

        prompt_surface = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA,
        )

        pygame.draw.rect(
            prompt_surface,
            (*default_conf["KeyBG"]["color1"], alpha),
            key_rect.inflate(padding_X, padding_Y),
            border_radius=default_conf["KeyBG"]["border_radius"]
        )   
        pygame.draw.rect(
            prompt_surface,
            (*default_conf["KeyBG"]["color2"], alpha),
            key_rect.inflate(padding_X, padding_Y),
            width=default_conf["KeyBG"]["width"],
            border_radius=default_conf["KeyBG"]["border_radius"]
        )   

        key_surface.set_alpha(alpha)
        action_surface.set_alpha(alpha)
        context_surface.set_alpha(alpha)

        prompt_surface.blit(key_surface, key_rect)
        prompt_surface.blit(action_surface, action_rect)
        prompt_surface.blit(context_surface, context_rect)

        screen.blit(prompt_surface, (0,0))