from config import *
import math
import pygame
from enemy import *
from player import Player
from powerups import PowerUpController
from monetarysystem import MonetarySystem
from shed import *
from inventory import *
from obstacle import *
from health import *


def game_loop():
    player = Player()
    pygame.mixer.music.stop()
    current_state = "main"

    while True:
        if current_state == "main":
            current_state = execute_game(player)
        elif current_state == "shop":
            current_state = shop_ui()

def game_over_screen(screen):
    """
    Display a game over screen.
    """
    bloodcrowfont = pygame.font.Font("assets/bloodcrow.ttf", 35)
    text = bloodcrowfont.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=(width // 2, height // 2))

    screen.fill((0, 0, 0))  # Fill the screen with black
    screen.blit(text, text_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Return to main menu on Enter key
                    from interface import interface
                    interface()
                    return
                elif event.key == pygame.K_ESCAPE:  # Quit game on Escape key
                    pygame.quit()
                    return

        pygame.display.flip()

def execute_game(player: Player):
    """
    Main function to execute the game loop

    """

    # Clock for controlling the frame rate
    clock = pygame.time.Clock()



    # ==== SETTING UP THE GAME ====

    # Setting up the background
    screen = pygame.display.set_mode(resolution)
    background = pygame.image.load("assets/lvl2.jpg").convert()
    background = pygame.transform.scale(background, (width, height))

    # Setting up Background Music
    #pygame.mixer.music.load('assets/BGMusic.mp3')
    #pygame.mixer.music.play(-1)

    # Timer Setup
    level_duration = 300  # Level duration in seconds (e.g., 5 minutes)
    start_time = pygame.time.get_ticks()  # Record the start time

    # Screen setup
    pygame.display.set_caption("Surge of the Silence")

    # Player Setup
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # Initialize the bullet group
    bullets = pygame.sprite.Group()

    # Initialize the obstacle group
    obstacles = pygame.sprite.Group()

    # Initialize the enemy group
    zombies = pygame.sprite.Group()
    zombies_spawn_timer = 0

    #Initialize the item group
    items_group = pygame.sprite.Group()
    item_spawn_timer = 0

    # Initialize Inventory
    inventory = Inventory()
    for weapon in player.inventory.values():
        inventory.add_item(weapon) # adding weapons to the inventory

    #Initialize the PowerUpController
    power_up_controller = PowerUpController()

    #Initialize Monetary System
    monetary_system = MonetarySystem() #we can put inside of the MonetarySystem() the initial_balance = amount,
    # for example initial_balance = 50, which means the player will always start the game with 50€.

    # Initialize House obstacle
    house_main = Obstacle(550, 140, 230, 285)
    house_side = Obstacle(780, 247, 203, 178)
    obstacles.add(house_main)
    obstacles.add(house_side)


    # ==== GAME LOOP ====
    running = True
    while running:
        # Control frame rate
        clock.tick(fps)

        # Set tup the background
        screen.blit(background, (0,0))

        # Calculate dt (delta time: time between frames)
        dt = clock.tick(fps) / 1000.0  # dt is in seconds

        # Calculate elapsed time
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Convert to seconds
        remaining_time = max(level_duration - elapsed_time, 0)  # Remaining time in seconds

        # End the level when time runs out
        if remaining_time <= 0:
            print("Level Complete!")
            return "main"  # Return to main menu or next level

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    inventory.toggle_visibility()  # Toggle the inventory visibility

                # Check number key presses (1 to 0)
                if pygame.K_1 <= event.key <= pygame.K_9:
                    slot_index = event.key - pygame.K_1  # 1 maps to slot 0, 2 to slot 1, etc.
                    inventory.change_slot(slot_index)
                    selected_weapon = inventory.get_selected_item()
                    if selected_weapon:
                        player.weapon_switching(selected_weapon.name)
        # Shooting
        player.shoot(bullets, zombies)

        # Handle item pickups
        for item in items_group:  # Assuming items_group contains spawnable items
            if pygame.sprite.collide_rect(player, item):
                inventory.add_item({"name": item.name, "icon": item.icon_path})  # Add item with its details
                item.kill()  # Remove the item from the game


        # ==== SPAWN ====

        # Spawn timer
        if zombies_spawn_timer > 0:
            zombies_spawn_timer -= 1

        # Weighted random selection
        zombie_type = random.choices(
                [FastZombie, TankZombie, ExplodingZombie, Enemy],
                weights=[0.2, 0.2, 0.1, 0.5],  # 20% Fast, 20% Tank, 10% Exploding, 50% Normal Enemy
                k=1
            )[0]

        # Spawning the enemies
        if zombies_spawn_timer <= 0:
            # Randomly select a zombie type
            zombie_type = random.choice([FastZombie, TankZombie, ExplodingZombie, NormalZombie])
            new_enemy = zombie_type()  # Instantiate the selected zombie type
            zombies.add(new_enemy)
            zombies_spawn_timer = fps  # Every two seconds




        # ==== CHECKERS ====

        # Checking for collisions between enemies and bullets
        for bullet in bullets:
            collided_zombies = pygame.sprite.spritecollide(bullet, zombies, False)
            for zombie in collided_zombies:
                zombie.take_damage(bullet.damage)
                bullet.kill()  # Destroy the bullet
                if zombie.health <= 0:
                    zombie.kill()  # Destroy the enemy
                    monetary_system.money_earned(10) #Ganha 10€ por zombie derrotado



        # ==== UPDATES ====

        # Update positions
        player_group.update(dt, obstacles)
        bullets.update()
        # Update zombies with animation
        for zombie in zombies:
            zombie.update(player, dt)


        # Update the draw power-ups
        power_up_controller.update(player,zombies)
        power_up_controller.draw(screen)



        # ==== DRAWS ====

        # Drawing the object
        player_group.draw(screen)
        player.draw(screen)
        player.draw_debug_rect(screen)
        zombies.draw(screen)
        for zombie in zombies:
            zombie.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)


        # Shows monetary balance
        font = pygame.font.SysFont("assets/Creepster-Regular.ttf)", 30)
        monetary_system.show_balance(screen,font)

        # Draw timer on the screen
        timer_text = font.render(f"Time Left: {int(remaining_time)}s", True, (128, 0, 128))
        screen.blit(timer_text, (10, 30))

        inventory.render(screen)

        pygame.display.flip()