import pygame

class HealthBar:
    def __init__(self):
        """
        Initialize the HealthBar.

        Args:
        ----
        max_health (int): Maximum health the player can have.
        """
        self.health = 6
        # Load health bar images
        self.health_bar_images = [pygame.image.load(f"assets/healthbar/bar{i}.png") for i in range(1, 7)]
        # Resize images
        self.health_bar_images = [
            pygame.transform.scale(img, (160, 50)) for img in self.health_bar_images
        ]


    def draw(self, screen,player_rect):
        """
        Draw the current health bar on the screen at the given position.
        """


        # Adjust position relative to player's rect
        bar_x = player_rect.centerx - 75
        bar_y = player_rect.top - 50

        # Display the correct health bar image
        index = 6-self.health  # Calculate the correct image index
        current_image = self.health_bar_images[index]
        # Draw the health bar image
        screen.blit(current_image, (bar_x, bar_y))

    def decrease_health(self):
        if self.health > 0:
            self.health -= 1

    def is_empty(self):
        return self.health <= 0