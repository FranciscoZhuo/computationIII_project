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
    def apply_powerup(self, player, zombies = None):
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
        self.image = pygame.image.load("assets/heart.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(40, 40))
        self.rect = self.image.get_rect(topleft = (x,y))

    def apply_powerup(self,player, zombies = None):
        """
        Increases the player´s life by 20%
        """
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

class InvisibilityPowerUP(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, effect_duration=15000)
        self.image = pygame.image.load("assets/potion.png")
        self.image = pygame.transform.scale(self.image,(40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))

    def apply_powerup(self, player, zombies=None):
        """
        Applies invisibility effect to the player.
        """
        player.invisible = True
        player.invisibility_start = pygame.time.get_ticks()
        print("Player is now invisible!")


#It´s important now to create a class, called PowerUpController, because we will implement more than the 2 power-ups that are mandatory
#which makes the code more easy to expand but also makes the code more organized and separated by responsabilities.

class PowerUpController:
    def __init__(self):
        self.power_ups = pygame.sprite.Group()
        self.interval_spawn = 10000 #10 sec
        self.last_spawn = pygame.time.get_ticks() #keeps tracking of the last time that a power-up appeared

    def update(self, player, zombies):
        """
        Aims to update the state of all power-ups

        Args:
            player(Player): Player object
            zombies(list): List of zombie objects
        """
        self.spawn_powerup()
        self.collisions(player, zombies)
        self.remove_powerups()


    def spawn_powerup(self):
        """
        We want the power-up to spawns on a random place in the screen
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn > self.interval_spawn:
            x = random.randint (50, 750)
            y = random.randint(50, 550)
            type_powerup = random.choice([LifePowerUp, SlowZombiesPowerUp, InvisibilityPowerUP]) #basically, we want the power-up to spawn randomly
            power_up = type_powerup(x,y)
            self.power_ups.add(power_up)
            self.last_spawn = current_time

    def collisions(self, player, zombies):
        """
        Checks colisions between player and power-ups

        Args:
            player(Player): player object
            zombies(list): list of zombies
        """
        for power_up in list(self.power_ups): #It´s suposed to create a copy to avoid redundancy
            if pygame.sprite.collide_rect(player, power_up):
                power_up.apply_powerup(player, zombies)
                self.power_ups.remove(power_up)

    def remove_powerups(self):
        """
        Removes power-ups after appears for 15 seconds
        """
        for power_up in self.power_ups:
            if power_up.end_powerup():
                self.power_ups.remove(power_up)

    def draw(self, screen):
        """
        Active power-ups

        Args:
            screen(Surface): Game screen
        """
        self.power_ups.draw(screen)