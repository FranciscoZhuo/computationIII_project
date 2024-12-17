import pygame

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

        # Health bar background
        pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height))

        # Health bar foreground (red)
        current_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(screen, (255, 0, 0), (x, y, current_width, bar_height))

    def decrease_health(self, amount):
        """
        Decrease health by a specified amount.
        """
        self.health = max(self.health - amount, 0)

    def is_empty(self):
        return self.health <= 0