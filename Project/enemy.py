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



    def update(self, player, dt):
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
        self.speed = 1
        self.health = 30  # Much higher health

        # Load animation frames
        self.animations = {
            # Adjust range as needed
            "run_right": [pygame.image.load(f"assets/Tank Zombie/Walk/walk{i}.png").convert_alpha() for i in range(3)],
            "attack": [pygame.image.load(f"assets/Tank Zombie/Attack/Attack{i}.png").convert_alpha() for i in range(4)],
        }

        self.animations["run_left"] = [pygame.transform.flip(image, True, False) for image in self.animations["run_right"]]

        # Scale all frames in self.animations
        scale_animations(self.animations, 100, 120)  # Scales all loaded animations

        # Set initial animation state
        self.current_animation = "run_right"
        self.current_frame = 0
        self.animation_speed = 0.1  # Adjust speed as needed
        self.frame_time = 0  # Tracks time for frame updates
        self.image = self.animations[self.current_animation][self.current_frame]  # Initial image

    def set_animation(self, animation_name):
        """
        Sets the current animation state.
        """
        if animation_name != self.current_animation:
            self.current_animation = animation_name
            self.current_frame = 0  # Reset to the first frame

    def animate(self, dt):
        """
        Updates the zombie's animation based on the current animation state.
        """
        self.frame_time += dt
        if self.frame_time > self.animation_speed:
            self.frame_time = 0
            self.current_frame += 1

            frames = self.animations[self.current_animation]
            if self.current_frame >= len(frames):
                self.current_frame = 0  # Loop the animation

            self.image = frames[self.current_frame]


    def update(self, player, dt):
        """
        Update the zombie's behavior and animation.
        """
        # Update position
        super().update(player, dt)

        # Change to attack animation if close to player
        if pygame.sprite.collide_rect(self, player):
            if self.current_animation != "attack":
                self.set_animation("attack")
        else:
            # Determine movement direction and set run animations
            if player.rect.x > self.rect.x:  # Player is to the right
                if self.current_animation != "run_right":
                    self.set_animation("run_right")
            else:  # Player is to the left
                if self.current_animation != "run_left":
                    self.set_animation("run_left")

        # Call parent update for movement logica
        self.animate(dt)

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



