import pygame
from config import *

class Inventory:
    def __init__(self):
        self.items = []  # List to store items in the inventory
        self.max_slots = 5  # Define the number of slots available in the inventory
        self.bar_image = pygame.image.load("assets/Barra Inventory.png")  # Load the inventory bar image

    def add_item(self, item):
        """Add an item to the inventory if there's space."""
        if len(self.items) < self.max_slots:
            self.items.append(item)

    def render(self, screen):
        """Render the inventory bar and items on the screen."""
        # Draw the inventory bar
        screen.blit(self.bar_image, (0, 634))  # Adjust position as needed

        # Draw items in the inventory
        slot_width = self.bar_image.get_width() // self.max_slots
        for index, item in enumerate(self.items):
            # Draw the item icon in the appropriate slot
            item_icon = pygame.image.load(item['icon']).convert_alpha()
            item_icon = pygame.transform.scale(item_icon, (40, 40))  # Adjust size
            screen.blit(item_icon, (25 + index * slot_width, 25))  # Adjust positioning


class Item(pygame.sprite.Sprite):
    def __init__(self, name, icon_path, x, y):
        super().__init__()
        self.name = name
        self.icon_path = icon_path
        self.image = pygame.image.load(icon_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))  # Adjust size
        self.rect = self.image.get_rect(topleft=(x, y))




