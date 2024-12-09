from config import *
import pygame
import math
from bullets import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize a PLayer instance
        """
        super().__init__()
        self.image = pygame.Surface(player_size)
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

        # Gameplay variables
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.bullet_cooldown = 0

        # Load animation frames
        self.animations = {
            "idle": [pygame.image.load(f"assets/MC Frames/idle/Ellie frame_idle_{i}.png").convert_alpha() for i in range(3)],
            "run_right": [pygame.image.load(f"assets/MC Frames/run/Ellie frame_run_{i}.png").convert_alpha() for i in range(13)],
            "shoot": [pygame.image.load(f"assets/MC Frames/shoot/Ellie frame_shoot_{i}.png").convert_alpha() for i in range(3)],  # Example, change as necessary
            "death": [pygame.image.load(f"assets/MC Frames/death/Ellie frame_death_{i}.png").convert_alpha() for i in range(7)]  # Example, change as necessary
        }

        self.animations["run_left"] = [pygame.transform.flip(image, True, False) for image in self.animations["run_right"]]

        # Scale all frames in self.animations
        self.scale_animations(100,120)  # Scales all loaded animations

        self.current_animation = "idle"
        self.current_frame = 0
        self.image = self.animations[self.current_animation][self.current_frame]  # Start with the first frame
        self.animation_speed = 0.15  # Adjust as needed
        self.animation_timer = 0
        self.moving = False  # Flag to track movement
        self.dead = False  # Flag for player death

    def update(self, dt):
        keys = pygame.key.get_pressed()

        self.moving = False  # Reset moving flag at the start of each frame

        # Movement and animation updates
        if keys[pygame.K_w] and self.rect.top > 0: #UP
            self.rect.y -= self.speed
            self.moving = True
        elif keys[pygame.K_s] and self.rect.bottom < height: #DOWN
            self.rect.y += self.speed
            self.moving = True

        if keys[pygame.K_a] and self.rect.left > 0: #LEFT
            self.rect.x -= self.speed
            self.current_animation = "run_left"
            self.moving = True
        elif keys[pygame.K_d] and self.rect.right < width: #RIGHT
            self.rect.x += self.speed
            self.current_animation = "run_right"
            self.moving = True

        # Set to idle if not moving
        if not self.moving and not self.dead:  #Check if dead, so it doesn't switch to idle animation
            self.current_animation = "idle"



        #Animation Update
        if not self.dead: #Animate only if not dead
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])
                self.image = self.animations[self.current_animation][self.current_frame]


        # Shooting animation
        if self.bullet_cooldown > 0 and not self.dead:
            self.current_animation = "shoot"


        #Death Animation
        if self.health <= 0:
            self.current_animation = "death"
            self.dead = True

        if self.dead and self.current_frame == len(self.animations["death"]) - 1:
            self.kill()



    def shoot(self, bullets: pygame.sprite.Group):
        """
        Shoot bullets in 4 direction depending on cooldown.

        Args
        ----
        bullets (pygame.spirite.Group):
            The bullet group that we will add the news ones to
        """
        # If you shooting
        if self.bullet_cooldown <= 0:
            for angle in [0, math.pi / 2, math.pi, 3 * math.pi / 2]:
                bullet = Bullet(
                    self.rect.center[0], self.rect.center[1], angle
                )
                bullets.add(bullet)
            self.bullet_cooldown = fps # MC Frames until the next shot

        # If you not
        self.bullet_cooldown -= 1

    def scale_animations(self, width, height):
        """Scales all animation frames to the desired dimensions."""

        for animation_name, frames in self.animations.items():
            self.animations[animation_name] = [pygame.transform.scale(frame, (width, height)) for frame in frames]
