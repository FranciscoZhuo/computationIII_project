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

class FastZombie(Enemy):
    def __init__(self):
        super().__init__()
        self.image.fill(green)  # Green for fast zombies
        self.speed = random.randint(4, 6)  # Faster than normal enemies
        self.health = 5  # Lower health since they're faster

class TankZombie(Enemy):
    def __init__(self):
        super().__init__()
        self.image.fill(grey)  # Grey for tank zombies
        self.speed = random.randint(1, 2)  # Slower than normal enemies
        self.health = 20  # Much higher health


class ExplodingZombie(Enemy):
    def __init__(self):
        super().__init__()
        self.image.fill(yellow)  # yellow for exploding zombies
        self.speed = random.randint(2, 3)
        self.health = 8  # Normal health

    def explode(self, player):
        """
        Causes the zombie to explode and deal damage to the player.
        """
        # Example of an explosion effect (reduce player health or spawn particles)
        if pygame.sprite.collide_rect(self, player):
            player.health -= 10  # Assume player has a health attribute
            self.kill()  # Remove this zombie from the game



