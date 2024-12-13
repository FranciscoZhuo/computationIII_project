import pygame
import math
from bullets import Bullet

class Weapon:
    def __init__(self, damage, fire_rate):
        """
        Initialize the Weapon class.

        Args:
        ----
        damage (int): The damage dealt by each shot.
        fire_rate (float): Time (in seconds) between consecutive shots.
        """
        self.damage = damage
        self.fire_rate = fire_rate
        self.cooldown = 0

    def shoot(self, player, bullets, target):
        """
        Shoot a bullet towards the specified target.

        Args:
        ----
        player (Player): The player shooting the weapon.
        bullets (pygame.sprite.Group): The group to add the bullet to.
        target (pygame.sprite.Sprite): The target to aim at (e.g., nearest zombie).
        """
        if self.cooldown <= 0:
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
