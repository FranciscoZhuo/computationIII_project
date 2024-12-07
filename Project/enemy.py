from utils import *
from config import *
import pygame
import random
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initializes an enemy instance
        """
        super().__init__()
        self.image = pygame.Surface((enemy_size, enemy_size))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        # Positioning
        self.rect.x = random.randint(0, width - enemy_size)
        self.rect.y = random.randint(0, width - enemy_size)

        # Random speed
        self.speed = random.randint(2, 3)

        # Health
        self.health = 10

    def update(self, player):
        """
        Update the enemy's position according to the player's.

        Args
        ---
        player (Player):
            The player to move towards.
        """

        # Calculation the direction in which the player is (angle)
        direction = math.atan2(
            player.rect.y - self.rect.y, player.rect.x - self.rect.x
        )

        # Coordinate update
        self.rect.x += self.speed * math.cos(direction)
        self.rect.y += self.speed * math.sin(direction)

        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)


