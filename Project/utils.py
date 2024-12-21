import pygame
import os
import pickle
from inventory import *


def scale_animations(animations, width, height):
    """
    Scales all animation frames to the desired dimensions.
    """

    for animation_name, frames in animations.items():
        animations[animation_name] = [pygame.transform.scale(frame, (width, height)) for frame in frames]

def show_coins(screen, player, x = 135, y = 40):
    """
    Render the UI elements such as the player's balance.

    Args:
        screen (pygame.Surface): The game screen to draw on.
        player (Player): The player object containing the monetary system.
        x(int): Coordinate x to show the balance
        y(int): Coordinate y to show the balance
    """
    font = pygame.font.Font("assets/Creepster-Regular.ttf", 25)
    player.monetary_system.show_balance(screen, font, x, y)  # Display in top-left corner

