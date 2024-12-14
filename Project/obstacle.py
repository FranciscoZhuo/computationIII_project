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
        - debug (bool): Whether to draw the obstacle for debugging purposes.
        """
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        """
        Draw the obstacle only if debug mode is enabled.

        Args:
        - screen (pygame.Surface): The screen surface to draw on.
        """

        pygame.draw.rect(screen, self.rect)

    def collides_with(self, sprite):
        """
        Check if the obstacle collides with another sprite.

        Args:
        - sprite (pygame.sprite.Sprite): The other sprite.

        Returns:
        - bool: True if a collision occurs, False otherwise.
        """
        return self.rect.colliderect(sprite.rect)
