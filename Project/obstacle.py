import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        """
        Initialize an invisible obstacle.

        Args:
        - x (int): The x-coordinate of the obstacle.
        - y (int): The y-coordinate of the obstacle.
        - width (int): The width of the obstacle.
        - height (int): The height of the obstacle.
        """
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)

