import pygame
import math
from bullets import Bullet

class Weapon:
    def __init__(self, damage, fire_rate, name, icon):
        """
        Initialize the Weapon class.

        Args:
        ----
        damage (int): The damage dealt by each shot.
        fire_rate (float): Time between consecutive shots.
        """
        self.damage = damage
        self.fire_rate = fire_rate
        self.cooldown = 0
        self.name = name
        self.icon = icon

        # Load the icon as an image
        self.image = pygame.image.load(icon).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))  # Scale to fit inventory slots

    def shoot(self, player, bullets, target):
        """
        Shoot a bullet towards the specified target.

        Args:
        ----
        player (Player): The player shooting the weapon.
        bullets (pygame.sprite.Group): The group to add the bullet to.
        target (pygame.sprite.Sprite): The target to aim at (e.g., nearest zombie).
        """
        if self.cooldown <= 0 and target:
            dx = target.rect.centerx - player.rect.centerx
            dy = target.rect.centery - player.rect.centery
            angle = math.atan2(dy, dx)

            # Spawn bullet
            bullet = Bullet(player.rect.centerx, player.rect.centery, angle, self.damage)
            bullets.add(bullet)

            self.cooldown = self.fire_rate

    def update(self, dt):
        """
        Update the weapon's state, such as cooldown.

        Args:
        ----
        dt (float): Delta time (time since the last frame).
        """
        if self.cooldown > 0:
            self.cooldown -= dt

#Subclasses for the weapons
class Pistol(Weapon):
    def __init__(self):
        super().__init__(damage=10, fire_rate=0.5, name="Pistol", icon="assets/pistol.png")
        #more weak/standard damage and shooting time

class MachineGun(Weapon):
    def __init__(self):
        super().__init__(damage=30, fire_rate=0.1, name="Machine Gun", icon="assets/machinegun.png")
        #strong damage but slower fire rate

class ShotGun(Weapon):
    def __init__(self):
        super().__init__(damage=50, fire_rate=1.5, name="Shot Gun", icon="assets/shotgun.png")
