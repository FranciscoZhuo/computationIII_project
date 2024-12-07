#A base Class called PowerUps that will be enherited  for specific types of Power-Ups.
from abc import abstractmethod, ABC
import pygame
import random

class PowerUp(ABC, pygame.sprite.Sprite):
    def __init__(self, x, y, effect_duration):
        """
        Base class for all power_ups

        Args:
            x(int):X-coordinate of the power-up
            y(int):Y-coordinate of the power-up
            effect_duration(int): The duration of the power-up in milliseconds.

        """
        super().__init__()
        self.image = None
        self.rect = pygame.Rect(x, y, 40, 40)
        self.effect_duration = effect_duration #the amount of time the power-up will appear in the screen
        self.spawn_time = pygame.time.get_ticks() #pygame.time.get_ticks() returns the number of milliseconds since the programme has started
        #spawn_time keeps the moment that the power-up was created/initialized

    @abstractmethod
    def apply_powerup(self,player):
        """
        Applies the effect of the power-up on the player.

        Args:
            player(Player): The player object.
        """
        pass

    def end_powerup(self):
        """
        Check if the power up is over.
        Returns:
             bool: True if the power-up expired, False if it is valid.
        """
        return pygame.time.get_ticks() - self.spawn_time > self.effect_duration  #the player has 15 seconds to get the power up, else it desappears

class LifePowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x,y,effect_duration=15000) #the power-up for receiving more 20% of life
        self.image = pygame.image.load("heart.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(40, 40))
        self.rect = self.image.get_rect(topleft = (x,y))

    def apply_powerup(self,player):
        player.health = min(player.health + player.max_health * 0.2, player.max_health)

class SlowZombiesPowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x,y,effect_duration=15000)
        self.image = pygame.image.load("assets/snail.png")
        self.image = pygame.transform.scale(self.image,(40, 40))
        self.rect = self.image.get_rect(topleft = (x,y))

    def apply_powerup(self,player, zombies = None):
        """
        Applies the effect on the zombies.

        Args:
            player(Player): Player object
            zombies(list): List of zombie objects

        """
        for zombie in zombies:
            zombie.speed = max(1, zombie.speed // 2)

#It´s important now to create a class, called PowerUpController, because we will implement more than the 2 power-ups that are mandatory
#which makes the code more easy to expand but also makes the code more organized and separated by responsabilities.

class PowerUpController:
    def __init__(self):
        self.power_ups = pygame.sprite.Group()
        self.interval_spawn = 1000 #10 sec
        self.last_spawn = pygame.time.get_ticks() #keeps tracking of the last time that a power-up appeared

    def update(self, player, zombies):
        """
        Aims to update the state of all power-ups

        Args:
            player(Player): Player object
            zombies(list): List of zombie objects
        """
        current_time = pygame.time.get_ticks()

        #Spawn power-ups at intervals
        if current_time - self.last_spawn > self.interval_spawn:
            self.spawn_power_up()
            self.last_spawn = current_time

        #Colisions between player and power-ups
        for power_up in self.power_ups:
            if pygame.sprite.collide_rect(player, power_up):
                power_up.apply_powerup(player, zombies)
                self.power_ups.remove(power_up)

        #Remove power-ups after apears for 15 seconds
        for power_up in self.power_ups:
            if power_up.end_powerup():
                self.power_ups.remove(power_up)


    def spawn_powerup(self):
        """
        We want the power-up to spawns on a random place in the screen
        """
        x = random.randint (50, 750)
        y = random.randint(50, 550)

        type_powerup = random.choice([LifePowerUp, SlowZombiesPowerUp]) #basically, we want the power-up to spawn randomly
        power_up = type_powerup(x,y)
        self.power_ups.add(power_up)

    def draw(self, screen):
        """
        Active power-ups

        Args:
            screen(Surface): Game screen
        """
        self.power_ups.draw(screen)