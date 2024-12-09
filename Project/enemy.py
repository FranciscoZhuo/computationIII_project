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

        # Animations
        self.animations = {}  # Initialize an empty dictionary for animations
        self.current_animation = None  # Holds the current animation playing
        self.current_frame = 0
        self.animation_speed = 0.01  # Adjust as needed
        self.animation_timer = 0

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

        if self.current_animation:  # Check if animation is defined
            # Increment frame counter
            self.current_frame += 1

            # Animation update (frame-rate dependent):
            if self.current_frame >= len(
                    self.animations[self.current_animation]):  # Reset current_frame if it reaches end of animation
                self.current_frame = 0

            self.image = self.animations[self.current_animation][
                self.current_frame
            ]


class FastZombie(Enemy):
    def __init__(self):
        super().__init__()
        self.image.fill(green)  # Green for fast zombies
        self.speed = random.randint(4, 6)  # Faster than normal enemies
        self.health = 5  # Lower health since they're faster

class TankZombie(Enemy):
    def __init__(self):
        super().__init__()


        # Load animation frames
        self.animations = {
            "walk": [
                pygame.image.load("assets/Tank Zombie/Walk/walk_0.png").convert_alpha(),
                pygame.image.load("assets/Tank Zombie/Walk/walk_1.png").convert_alpha(),
                pygame.image.load("assets/Tank Zombie/Walk/walk_2.png").convert_alpha()
            ],
            "attack": [  # Animation for attack
                pygame.image.load("assets/Tank Zombie/Attack/Attack_0.png").convert_alpha(),
                pygame.image.load("assets/Tank Zombie/Attack/Attack_1.png").convert_alpha(),
                pygame.image.load("assets/Tank Zombie/Attack/Attack_2.png").convert_alpha(),
                pygame.image.load("assets/Tank Zombie/Attack/Attack_3.png").convert_alpha()
            ],
            "die": [  # Animation for dying
                pygame.image.load("assets/Tank Zombie/Death/Death_00.png").convert_alpha(),
                pygame.image.load("assets/Tank Zombie/Death/Death_01.png").convert_alpha(),
                pygame.image.load("assets/Tank Zombie/Death/Death_02.png").convert_alpha(),
                pygame.image.load("assets/Tank Zombie/Death/Death_03.png").convert_alpha(),
                pygame.image.load("assets/Tank Zombie/Death/Death_04.png").convert_alpha(),
                pygame.image.load("assets/Tank Zombie/Death/Death_05.png").convert_alpha()
            ]

        }
        self.current_animation = "walk"  # Set default animation
        self.image = self.animations[self.current_animation][0]  # Start with first frame
        self.rect = self.image.get_rect()

        self.speed = random.randint(1, 2)  # Slower than normal enemies
        self.health = 20  # Much higher health

    def update(self, player):
        super().update(player)  # Call base class update for animation and movement

        # Example: Switch to attack animation if close to player
        distance_to_player = math.hypot(self.rect.centerx - player.rect.centerx,
                                        self.rect.centery - player.rect.centery)
        if distance_to_player < 50:  # Adjust attack range as needed
            self.current_animation = "attack"
        else:
            self.current_animation = "walk"

        # Example: start death animation if dead
        if self.health <= 0:
            self.current_animation = 'die'



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



