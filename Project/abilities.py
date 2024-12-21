import pygame
from abc import abstractmethod, ABC

class Ability(ABC, pygame.sprite.Sprite):
    def __init__(self, name, duration, image):
        """
        Base class for abiliies.

        Args:
            name: The name of the ability
            duration: time in seconds the habiity last
            icon: the image of the ability

        """
        self.name=name
        self.duration = duration
        self.image= pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image,(32,32))
        self.active=False
    @abstractmethod
    def apply_ability(self, player):   #pretty much the same from powerups.py
        """
        Applies the effect of the ability on the player.
        """
        pass

    def end_ability(self, player):
        """
        Checks if the ability is over.
        """
        pass

class Shield(Ability):
    def __init__(self):
        super().__init__(name="Shield", duration=20000, image="assets/shield.png")
        self.start_time = None

    def apply_ability(self, player):
        """
        Receives no damage.
        """
        self.active = True
        player.shield_active = True
        player.active_abilities[self] = pygame.time.get_ticks()

    def end_ability(self, player):
        """
        Deactivates the shield.
        """
        if self.active:
            self.active = False
            player.shield_active = False

class ExtraSpeed(Ability):
    def __init__(self):
        super().__init__(name="Extra Speed", duration=20000, image="assets/rocket.png")
        self.start_time = None

    def apply_ability(self, player):
        """
        Dubles the velocity of the player
        """
        self.active = True
        player.speed *= 2
        player.active_abilities[self] = pygame.time.get_ticks()

    def end_ability(self, player):
        """
        Brings the velocity back to normal
        """
        if self.active:
            self.active = False
            player.speed /= 2

class NewLife(Ability):
    def __init__(self):
        super().__init__(name="New Life", duration=0, image="assets/health_pack.png")

    def apply_ability(self, player):
        """
        Restores 100% of the player´s health.
        """
        self.active = True
        player.health = player.max_health
        self.active = False

    def end_ability(self, player):
        pass #no need
    
class DoubleDamage(Ability):
    def __init__(self):
        super().__init__(name="Double Damage", duration= 20000, image="assets/bullet.png")
        self.start_time = None

    def apply_ability(self, player):
        """
        Double damage on the zombies
        """
        self.active=True
        if player.weapon:
            player.weapon.damage *= 2
        player.active_abilities[self] = pygame.time.get_ticks()  # to garantee that the effect expires correctly, we need to know when the ability was activated

    def end_ability(self, player):
        """
        Removes the effect
        """
        if self.active:
            self.active=False
            if player.weapon:
                player.weapon.damage //= 2



