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

# ==== NORMAL ZOMBIE ====

class NormalZombie(Enemy):
    def __init__(self):
        super().__init__()

        self.speed = random.randint(2, 3)  # Same speed as Enemy
        self.health = 10  # Same health as Enemy

        # Load animation frames
        self.animations = {
            # Adjust range as needed
            "run_right": [pygame.image.load(f"assets/NormalZombie/run/run{i}.png").convert_alpha() for i in range(8)],
            "attack": [pygame.image.load(f"assets/NormalZombie/attack/attack{i}.png").convert_alpha() for i in range(7)],
        }

        self.animations["run_left"] = [pygame.transform.flip(image, True, False) for image in
                                       self.animations["run_right"]]

        # Scale all frames in self.animations
        scale_animations(self.animations, 80, 80)  # Scales all loaded animations

        # Set initial animation state
        self.current_animation = "run_right"
        self.current_frame = 0
        self.animation_speed = 0.1
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


# ==== FAST ZOMBIE ====

class FastZombie(Enemy):
    def __init__(self):
        super().__init__()
        self.speed = random.randint(4, 6)  # Faster than normal enemies
        self.health = 5  # Lower health since they're faster

        # Load animation frames
        self.animations = {
            # Adjust range as needed
            "run_right": [pygame.image.load(f"assets/Fast Zombie/run/run{i}.png").convert_alpha() for i in range(8)],
            "attack": [pygame.image.load(f"assets/Fast Zombie/attack/attack{i}.png").convert_alpha() for i in range(6)],
        }

        self.animations["run_left"] = [pygame.transform.flip(image, True, False) for image in
                                       self.animations["run_right"]]

        # Scale all frames in self.animations
        scale_animations(self.animations, 80, 80)  # Scales all loaded animations

        # Set initial animation state
        self.current_animation = "run_right"
        self.current_frame = 0
        self.animation_speed = 0.1
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


# ==== TANK ZOMBIE =====

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
        scale_animations(self.animations, 100, 100)  # Scales all loaded animations

        # Set initial animation state
        self.current_animation = "run_right"
        self.current_frame = 0
        self.animation_speed = 0.1
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



# ==== EXPLODING ZOMBIE ====

class ExplodingZombie(Enemy):
    def __init__(self):
        super().__init__()

        self.speed = random.randint(2, 3)
        self.health = 8  # Normal health
        self.exploding = False

        # Load animation frames
        self.animations = {
            "run_left": [pygame.image.load(f"assets/Exploding Zombie/run/run{i}.png").convert_alpha() for i in range(4)],
            "attack": [pygame.image.load(f"assets/Exploding Zombie/attack/attack{i}.png").convert_alpha() for i in range(8)],
            "explosion": [pygame.image.load(f"assets/Explosion/frame_{i}.png").convert_alpha() for i in range(10)],  # Explosion frames
        }

        self.animations["run_right"] = [pygame.transform.flip(image, True, False) for image in self.animations["run_left"]]

        # Scale all frames in self.animations
        scale_animations(self.animations, 80, 80)  # Scales all loaded animations

        # Set initial animation state
        self.current_animation = "run_right"
        self.current_frame = 0
        self.animation_speed = 0.1
        self.frame_time = 0  # Tracks time for frame updates
        self.image = self.animations[self.current_animation][self.current_frame]  # Initial image

        self.damage_radius = 50  # Explosion damage radius

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
                if self.current_animation == "explosion":
                    self.kill()  # Remove zombie after explosion animation
                    return
                else:
                    self.current_frame = 0  # Loop non-explosion animations

            self.image = frames[self.current_frame]

    def explode(self, player):
        """
        Triggers the explosion animation and deals damage to the player if in range.
        """
        self.exploding = True
        self.set_animation("explosion")

        # Apply damage if within range
        if pygame.sprite.collide_rect(self, player):
            player.health -= 10  # Adjust damage value as needed

    def update(self, player, dt):
        """
        Update the zombie's behavior and animation.
        """
        if self.exploding:
            # Handle explosion animation
            self.animate(dt)
        else:
            # Update position and behavior
            super().update(player, dt)

            # Trigger explosion if directly above the player
            if abs(self.rect.centerx - player.rect.centerx) < self.rect.width // 2 and self.rect.centery < player.rect.centery:
                self.explode(player)
            else:
                # Determine movement direction and set run animations
                if player.rect.x > self.rect.x:  # Player is to the right
                    self.set_animation("run_right")
                else:  # Player is to the left
                    self.set_animation("run_left")

            # Animate movement or attack
            self.animate(dt)
