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
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

        self.last_collision_time = 0  # Initialize collision timer
        self.collision_cooldown = 1000  # Cooldown in milliseconds

        # Gameplay variables
        self.speed = 5
        self.bullet_cooldown = 0


    def update(self):
        """
        Update the position of the player based on keyboard input
        :return:
        """

        keys = pygame.key.get_pressed()
        # Moving upwards
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed

        # Moving downwards
        if keys[pygame.K_s] and self.rect.bottom < height:
            self.rect.y += self.speed

        # Moving left
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed

        # Moving right
        if keys[pygame.K_d] and self.rect.right < width:
            self.rect.x += self.speed

    def take_damage(self):
        """
        Pass damage to the health bar.
        """
        current_time = pygame.time.get_ticks()
        return current_time - self.last_collision_time > self.collision_cooldown

    def register_collision(self):
        self.last_collision_time = pygame.time.get_ticks()

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
            self.bullet_cooldown = fps # Frames until the next shot

        # If you not
        self.bullet_cooldown -= 1