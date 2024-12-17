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

    def get_selected_item(self):
        """
        returns the current selected item
        """
        if self.selected_slot < len(self.items):
            return self.items[self.selected_slot]
        return None

    def render(self, screen):
        if not self.visible:
            return

        # Draw the inventory bar
        bar_x, bar_y = 197, 690
        screen.blit(self.bar_image, (bar_x, bar_y))

        # Slot dimensions
        slot_width = 60
        slot_height = 61
        base_slot_spacing = 60  # Default spacing
        first_slot_gap = 30  # Extra gap before the second slot

        # Calculate slot position with gap correction
        def calculate_slot_x(index):
            if index == 0:
                return bar_x  # First slot at base position
            return bar_x + first_slot_gap + index * base_slot_spacing  # Add gap after first slot

        # Highlight the selected slot
        highlight_x = calculate_slot_x(self.selected_slot)
        highlight_rect = pygame.Rect(
            highlight_x,  # Corrected X position
            bar_y,
            slot_width,
            slot_height
        )
        pygame.draw.rect(screen, light_grey, highlight_rect, 3)  # Draw the yellow outline

        # Draw items in the inventory
        for index, item in enumerate(self.items):
            item_icon = pygame.image.load(item.icon).convert_alpha()
            item_icon = pygame.transform.scale(item_icon, (32, 32))  # Fit the item into the slot
            icon_x = calculate_slot_x(index) + (slot_width - 32) // 2
            icon_y = bar_y + (slot_height - 32) // 2
            screen.blit(item_icon, (icon_x, icon_y))


class Item(pygame.sprite.Sprite):
    def __init__(self, name, icon_path, x, y):
        super().__init__()
        self.name = name
        self.icon_path = icon_path
        self.image = pygame.image.load(icon_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))  # Adjust size
        self.rect = self.image.get_rect(topleft=(x, y))




