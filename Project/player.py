from utils import scale_animations
import pygame
import math
from bullets import Bullet
from config import *
from weapons import Pistol, MachineGun, ShotGun, SniperRifle, Flamethrower
from health import *
from monetarysystem import MonetarySystem



class Player(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize a PLayer instance
        """
        super().__init__()
        self.image = pygame.Surface(player_size)
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(-20, -10)
        self.rect.center = (width // 2, height // 2)


        # Gameplay variables
        self.speed = 5
        self.health = 200
        self.max_health = 200
        self.bullet_cooldown = 0
        self.damage_cooldown = 500  # Cooldown in milliseconds
        self.last_damage_time = pygame.time.get_ticks()  # Track last damage time
        self.health_bar = HealthBar(self.health)  # Add health bar

        # Load animation frames
        self.animations = {
            "idle": [pygame.image.load(f"assets/MC Frames/idle/Ellie frame_idle_{i}.png").convert_alpha() for i in range(4)],
            "run_right": [pygame.image.load(f"assets/MC Frames/run/Ellie frame_run_{i}.png").convert_alpha() for i in range(14)],
            "shoot": [pygame.image.load(f"assets/MC Frames/shoot/Ellie frame_shoot_{i}.png").convert_alpha() for i in range(4)],
            "death": [pygame.image.load(f"assets/MC Frames/death/Ellie frame_death_{i}.png").convert_alpha() for i in range(8)]
        }

        self.animations["run_left"] = [pygame.transform.flip(image, True, False) for image in self.animations["run_right"]]

        # Scale all frames in self.animations
        scale_animations(self.animations, 100, 120)  # Scales all loaded animations

        self.current_animation = "idle"
        self.current_frame = 0
        self.image = self.animations[self.current_animation][self.current_frame]  # Start with the first frame
        self.animation_speed = 0.05
        self.animation_timer = 0
        self.moving = False  # Flag to track movement
        self.dead = False  # Flag for player death

        #Inventory system
        self.inventory = {"Pistol": Pistol()}
        self.weapon =self.inventory["Pistol"] #To make pistol the default weapon

        self.monetary_system = MonetarySystem(initial_balance=0)

    def update(self, dt, obstacles):
        keys = pygame.key.get_pressed()

        self.moving = False  # Reset moving flag at the start of each frame

        # Movement and animation updates
        if keys[pygame.K_w] and self.rect.top > 0: #UP
            self.rect.y -= self.speed
            self.moving = True

            for obstacle in obstacles:
                if self.rect.colliderect(obstacle):
                    if self.rect.top < obstacle.rect.bottom and self.rect.centery > obstacle.rect.centery:
                        self.rect.top = obstacle.rect.bottom

        elif keys[pygame.K_s] and self.rect.bottom < height: #DOWN
            self.rect.y += self.speed
            self.moving = True
            for obstacle in obstacles:
                if self.rect.colliderect(obstacle):
                    if self.rect.bottom > obstacle.rect.top and self.rect.centery < obstacle.rect.centery:
                        self.rect.bottom = obstacle.rect.top

        if keys[pygame.K_a] and self.rect.left > 0: #LEFT
            self.rect.x -= self.speed
            self.current_animation = "run_left"
            self.moving = True
            # Collision from the right
            for obstacle in obstacles:
                if self.rect.colliderect(obstacle):
                    if self.rect.left < obstacle.rect.right and self.rect.centerx > obstacle.rect.centerx:
                        self.rect.left = obstacle.rect.right

        elif keys[pygame.K_d] and self.rect.right < width: #RIGHT
            self.rect.x += self.speed
            self.current_animation = "run_right"
            self.moving = True
            # Collision from the left
            for obstacle in obstacles:
                if self.rect.colliderect(obstacle):
                    if self.rect.right > obstacle.rect.left and self.rect.centerx < obstacle.rect.centerx:
                        self.rect.right = obstacle.rect.left

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

        #Weapon
        self.weapon.update(dt)

    def take_damage(self, amount):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time >= self.damage_cooldown:
            self.health = max(self.health - amount, 0)  # Apply damage
            self.health_bar.update(self.health)  # Update health bar
            self.last_damage_time = current_time
            if self.health <= 0:
                self.dead = True

    def shoot(self, bullets: pygame.sprite.Group, zombies: pygame.sprite.Group):
        """
    Shoot one bullet towards the nearest zombie when the Enter key is pressed.

    Args
    ----
    bullets (pygame.sprite.Group): The bullet group to add the new bullet to.
    zombies (pygame.sprite.Group): The group of zombies to target.
    """
        keys = pygame.key.get_pressed()

        # Shoot only when the Enter key is pressed
        if keys[pygame.K_SPACE] and self.bullet_cooldown <= 0:
            if zombies:
                # Find the nearest zombie
                nearest_zombie = min(zombies, key=lambda z: self.distance_to(z))

                # Calculate the angle to the nearest zombie
                dx = nearest_zombie.rect.centerx - self.rect.centerx


                dy = nearest_zombie.rect.centery - self.rect.centery
                angle = math.atan2(dy, dx)

                # Spawn a bullet in the direction of the zombie
                bullet = Bullet(self.rect.centerx, self.rect.centery, angle, self.weapon.damage)
                bullets.add(bullet)

                # Set cooldown
                self.bullet_cooldown = fps // 5 # Cooldown for 1 second

        # Reduce cooldown
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1

    def distance_to(self, zombie):
        """
    Calculate the distance to a zombie.

    Args
    ----
    zombie (pygame.sprite.Sprite): The zombie to calculate the distance to.

    Returns
    -------
    float: The distance to the zombie.
    """
        dx = zombie.rect.centerx - self.rect.centerx
        dy = zombie.rect.centery - self.rect.centery
        return math.sqrt(dx ** 2 + dy ** 2)

    def weapon_switching(self, name_weapon):
        """
        When the player is fighing, it´s possible to switch the weapons he has

        Args:
            name_weapon(str): The name of the weapon we want to switch to
        """
        if name_weapon in self.inventory:
            self.weapon = self.inventory[name_weapon]

    def draw_debug_rect(self, screen):
        """
        Draw a red outline around the player's rect for debugging.
        """
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Red color, width=2



