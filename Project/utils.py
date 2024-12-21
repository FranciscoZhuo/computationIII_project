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


def get_repo_root():
    return os.path.dirname(os.path.abspath(__file__))

def save_game(player, current_state, filename="savegame.pkl"):
    repo_root = get_repo_root()
    file_path = os.path.join(repo_root, filename)  # Save in the repository root
    print(f"Saving game to {file_path}...")
    game_state = {
        "player": {
            "health": player.health,
            "max_health": player.max_health,
            "position": (player.rect.x, player.rect.y),
            "inventory": [item.name for item in player.inventory.items],
            "monetary_balance": player.monetary_system.balance,
        },
        "current_state": current_state,
    }
    with open(file_path, "wb") as file:
        pickle.dump(game_state, file)
    print(f"Game saved to {file_path}.")

def load_game(player, filename="savegame.pkl"):
    repo_root = get_repo_root()
    file_path = os.path.join(repo_root, filename)  # Load from the repository root
    print(f"Trying to load save file from {file_path}...")
    try:
        with open(file_path, "rb") as file:
            game_state = pickle.load(file)

        # Restore player state
        player.health = game_state["player"]["health"]
        player.max_health = game_state["player"]["max_health"]
        player.rect.x, player.rect.y = game_state["player"]["position"]
        player.monetary_system.balance = game_state["player"]["monetary_balance"]

        # Rebuild inventory
        player.inventory.items = [
            Item(name, f"assets/{name.lower()}_icon.png", 0, 0, player)
            for name in game_state["player"]["inventory"]
        ]

        print("Game loaded successfully.")
        return game_state["current_state"]
    except FileNotFoundError:
        print(f"Save file {file_path} not found.")
        return None