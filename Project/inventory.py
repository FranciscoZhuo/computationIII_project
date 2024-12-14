import pygame
from config import *

class Inventory:
    def __init__(self):
        self.items = []  # List to store items in the inventory
        self.max_slots = 10  # Define the number of slots available in the inventory
        self.bar_image = pygame.image.load("assets/ItemBar.png")  # Load the inventory bar image
        self.visible = True  # Visibility of the inventory bar
        self.selected_slot = 0  # Track the currently selected slot (default is 0)

    def toggle_visibility(self):
        """Toggle the visibility of the inventory bar."""
        self.visible = not self.visible

    def change_slot(self, slot_index):
        """Change the selected slot."""
        if 0 <= slot_index < self.max_slots:
            self.selected_slot = slot_index

    def add_item(self, item):
        """Add an item to the inventory if there's space."""
        if len(self.items) < self.max_slots:
            self.items.append(item)
            return True  # Indicate success
        return False  # Indicate failure (inventory full)

    def render(self, screen):
        if not self.visible:
            return

        # Draw the inventory bar
        screen.blit(self.bar_image, (197, 690))  # Adjust the position (82, 634) to match your UI

        # Calculate slot dimensions
        bar_x, bar_y = 197, 690  # Top-left position of the bar
        slot_width = self.bar_image.get_width() // self.max_slots
        slot_height = self.bar_image.get_height()

        # Highlight the selected slot
        highlight_rect = pygame.Rect(
            bar_x + self.selected_slot * slot_width,  # X position based on the selected slot
            bar_y,  # Y position (matches the bar)
            slot_width,  # Width of a slot
            slot_height,  # Height of a slot
        )
        pygame.draw.rect(screen, (255, 255, 0), highlight_rect, 3)  # Yellow border

        # Draw items in the inventory
        for index, item in enumerate(self.items):
            item_icon = pygame.image.load(item['icon']).convert_alpha()
            item_icon = pygame.transform.scale(item_icon, (40, 40))  # Ensure icons fit within slots
            screen.blit(
                item_icon,
                (bar_x + index * slot_width + (slot_width - 40) // 2, bar_y + (slot_height - 40) // 2),
            )


class Item(pygame.sprite.Sprite):
    def __init__(self, name, icon_path, x, y):
        super().__init__()
        self.name = name
        self.icon_path = icon_path
        self.image = pygame.image.load(icon_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))  # Adjust size
        self.rect = self.image.get_rect(topleft=(x, y))




