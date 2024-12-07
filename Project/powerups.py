#A base Class called PowerUps that will be enherited  for specific types of Power-Ups.
from abc import abstractmethod, ABC
import pygame
import random

class PowerUp(ABC, pygame.sprite.Sprite):
    def __init__(self, x, y, effect_duration):
        """

        """
        super().__init__()
        self.image = None
        self.rect = pygame.Rect(x, y, 40, 40)
        self.effect_duration = effect_duration #the amount of time the power-up will appear in the screen
        self.spawn_time =
    def apply_effect(self,player):
        """
        applys the effect of the power-up on the player
        """
        pass

class LifePowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x,y,effect_duration=15000) #the power-up for receiving more 20% of life
        self.image = pygame.image.load("heart.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))
        self.image = pygame.transform.scale(self.image,(40, 40))

    def apply_effect(self,player):
        player.health = min(player.health + player.max_health * 0.2, player.max_health)