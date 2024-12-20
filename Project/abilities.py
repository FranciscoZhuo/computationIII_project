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
        #self.image = pygame.image.load("assets/heart.png").convert_alpha()
        #self.image = pygame.transform.scale(self.image, (40, 40))
        #self.rect = self.image.get_rect(topleft=(x, y))

    def apply_ability(self, player):
        self.active = True
        player.shield_active = True
        self.start_time= pygame.time.get_ticks()
        #Activates the shield for the player

    def end_ability(self, player):
        if self.active and pygame.time.get_ticks() - self.start_time >= self.duration:
            self.active = False
            player.shield_active = False
            # Deactivates the shield for the player

class ExtraSpeed(Ability):
    def __init__(self):
        super().__init__(name="Extra Speed", duration=20000, image="assets/rocket.png")
        self.start_time = None
        # self.image = pygame.image.load("assets/heart.png").convert_alpha()
        # self.image = pygame.transform.scale(self.image, (40, 40))
        # self.rect = self.image.get_rect(topleft=(x, y))

    def apply_ability(self, player):
        self.active = True
        player.speed *= 2
        self.start_time= pygame.time.get_ticks()
        # Activates the Extra Speed for the player

    def end_ability(self, player):
        if self.active and pygame.time.get_ticks() - self.start_time >= self.duration:
            self.active = False
            player.speed /= 2
            # Deactivates the Extra Speed for the player

#This ability will regenerate by 100% the player´s life
class NewLife(Ability):
    def __init__(self):
        super().__init__(name="New Life", duration=0, image="assets/health_pack.png")

    def apply_ability(self, player):
        """
        REstores 100% of the player´s health.
        """
        self.active = True
        player.health_bar.update(player.health_bar.max_health)
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
        player.damage *= 2
        self.start_time = pygame.time.get_ticks()

    def end_ability(self, player):
        if self.active and pygame.time.get_ticks() - self.start_time >= self.duration:
            self.active=False
            player.damage /= 2



