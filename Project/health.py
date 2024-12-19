import pygame
from config import *

class HealthBar:
    def __init__(self, max_health):
        """
        Initialize the HealthBar.

        Args:
        ----
        max_health (int): Maximum health of the entity.
        """
        self.health = max_health
        self.max_health = max_health

    def draw(self, screen, rect):
        """
        Draw the health bar above the entity.

        Args:
        ----
        screen (Surface): Pygame screen to draw the health bar on.
        rect (Rect): The entity's rectangle for positioning.
        """
        # Dimensions for the health bar
        bar_width = 50
        bar_height = 5
        x = rect.centerx - bar_width // 2
        y = rect.top - 10

        # Draw the background of the health bar (grey)
        pygame.draw.rect(screen, grey, (x, y, bar_width, bar_height))

        # Calculate the current red bar width based on health percentage
        health_percentage = self.health / self.max_health
        current_width = max(0, int(bar_width * health_percentage))
        
        pygame.draw.rect(screen, red, (x, y, current_width, bar_height))

    def draw_in_profile(self, screen, profile_surface):
        """
        Draw the health bar inside the player's profile.

        Args:
        ----
        screen (Surface): Pygame screen to draw the health bar on.
        profile_surface (Surface): The surface of the profile image.
        """
        # Get the rect from the profile surface
        rect = profile_surface.get_rect(topleft=(55, -87))  # Ensure proper positioning if not provided

        # Dimensions for the larger health bar
        bar_width = rect.width - 150  # Slight padding from the profile's edges
        bar_height = 15  # Taller health bar

        # Position within the profile
        x = rect.x + (rect.width - bar_width) // 2
        y = rect.bottom - bar_height - 10  # Near the bottom of the profile

        # Draw the background of the health bar (grey)
        pygame.draw.rect(screen, grey, (x, y, bar_width, bar_height))

        # Calculate the current red bar width based on health percentage
        health_percentage = self.health / self.max_health
        current_width = max(0, int(bar_width * health_percentage))

        pygame.draw.rect(screen, red, (x, y, current_width, bar_height))

    def update(self, new_health):
        """
        Update the health bar based on the new health.

        Args:
        ----
        new_health (int): Current health of the entity.
        """
        self.health = max(new_health, 0)  # Ensure health never goes below zero

    def decrease_health(self, amount):
        """
        Decrease health by a specified amount.
        """
        self.health = max(self.health - amount, 0)

    def is_empty(self):
        return self.health <= 0